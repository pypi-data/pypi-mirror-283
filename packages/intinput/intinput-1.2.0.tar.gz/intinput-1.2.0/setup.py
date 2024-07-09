from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='intinput', # name of packe which will be package dir below project
    version='1.2.0',
    url='https://github.com/Sisigoks/IntInput_Module',
    author='Sibi Gokul',
    author_email='Sisi.goks2008@gmail.com',
    description='A intput function that only reads intergers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[]
)