from distutils.core import setup

setup(
    packages=['microservice'],
    name='microservice-NoLabs',
    version='1.0.5',
    license='MIT',
    description='NoLabs microservice mixins',
    author='Igor Bruev',  # Type in your name
    author_email='jaktenstid1@gmail.com',  # Type in your E-Mail
    url='https://github.com/BasedLabs/microservice',  # Provide either the link to your github or to your website
    install_requires=[  # I get to this in a second
        'fastapi'
    ],
)
