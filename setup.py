# setup.py
from setuptools import setup, find_packages

setup(
    name='docpipe',
    version='0.1.0',
    packages=['docpipe'],
    include_package_data=True,
    package_data={
        'docpipe':['style.sty'],
    },
    install_requires=[
        'fire',
        'pypandoc',
        'termcolor',
        'setuptools'
    ],
)