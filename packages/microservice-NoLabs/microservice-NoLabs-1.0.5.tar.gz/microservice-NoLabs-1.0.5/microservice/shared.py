import json
from multiprocessing import shared_memory, Lock
from typing import Optional
from uuid import UUID

from .exceptions import MicroserviceException


class SharedMemoryManager:
    def __init__(self, name='job_dict', size=1024):
        try:
            self.shm = shared_memory.SharedMemory(name=name, create=True, size=size)
            self.shm.buf[:size] = bytearray(size)  # Initialize shared memory with zeros
        except FileExistsError:
            self.shm = shared_memory.SharedMemory(name=name)
        self.size = size
        self.lock = Lock()
        self._initialize_dict()

    def _initialize_dict(self):
        if self.shm.buf[:4].tobytes() == b'\x00\x00\x00\x00':
            self._write_dict({'job': None})

    def _read_dict(self):
        with self.lock:
            raw_data = self.shm.buf[:self.size].tobytes().rstrip(b'\x00')
            if raw_data:
                return json.loads(raw_data.decode())
            return {}

    def _write_dict(self, data):
        with self.lock:
            serialized_data = json.dumps(data).encode()
            self.shm.buf[:len(serialized_data)] = serialized_data
            self.shm.buf[len(serialized_data):] = b'\x00' * (self.size - len(serialized_data))

    def get_job_id(self) -> Optional[UUID]:
        data = self._read_dict()
        if not data['job']:
            return None
        return data['job']

    def set_job_running(self, job_id: str):
        data = self._read_dict()
        data['job'] = job_id
        self._write_dict(data)

    def set_job_stopped(self):
        self._write_dict({})

    def __del__(self):
        self.shm.close()
        self.shm.unlink()


memory_manager = SharedMemoryManager()


class AlreadyRunningException(MicroserviceException):
    ...
