from setuptools import setup, find_packages

setup(
    name='identity-trace-python-agent',
    version='1.0.7',
    packages=["identity_trace"],
    description='Tracing agent for python.',
    author='Mamoon Ahmed',
    author_email='engineer.mamoonahmed@gmail.com',
    url='https://github.com/MamoonAhmad/identity-reporting/tree/main/identity-trace-python-agent',
    install_requires=[
        "jsonpickle",
        "requests"
    ],
)