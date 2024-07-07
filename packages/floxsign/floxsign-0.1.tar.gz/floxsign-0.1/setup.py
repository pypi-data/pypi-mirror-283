# setup.py

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='floxsign',
    version='0.1',
    packages=find_packages(),
    description='A package to helps with symbols in python like gettingn the name of a symbol.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Florian Ratgers',
    author_email='flox@ratgers.nl',
    url='https://github.com/Flox-Company/floxsign',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
