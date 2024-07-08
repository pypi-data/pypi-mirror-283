from typing import Dict, Type

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions import MicroserviceException
from .shared import AlreadyRunningException


def add_domain_exception_middleware(app: FastAPI, exception_code_mapping: Dict[Type[MicroserviceException], int]):
    exception_code_mapping[AlreadyRunningException] = 400

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except MicroserviceException as e:
            status_code = exception_code_mapping[type(e)] if type(e) in exception_code_mapping else 200

            return JSONResponse(content={
                'error': e.message
            }, headers={'Content-Type': 'application/problem+json'}, status_code=status_code)
        except Exception:
            raise
