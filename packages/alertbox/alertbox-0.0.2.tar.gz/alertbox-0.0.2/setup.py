from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='alertbox', 
    version='0.0.2',
    url='https://github.com/HajMasterX/alertbox',
    author='HajMasterX',
    author_email='masterxq22@gmail.com',
    description='Simple MessageBox Builder',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
)