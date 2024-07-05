from setuptools import setup, find_packages
import os

def read_readme():
    with open(os.path.join('..', 'README.md'), 'r') as f:
        return f.read()
setup(
name='pythonipc',
version='1.2.0',
author='itsmrmonday',
author_email='zackary.live8@gmail.com',
description='Inter-process communication library for Python3 to interact with JS renderer',
long_description=read_readme(),
long_description_content_type='text/markdown',
url='https://github.com/its-mr-monday/pyipc',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
install_requires=[
    'flask',
    'flask_cors',
    'flask_socketio'
]
)