# Copyright 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
'''                       
Python package setup (used by Dockerfile).
'''

import os
import subprocess

from setuptools import setup, find_packages

data_files = []

setup(
    name='agritrace-cli',
    version='1.0',
    description='Sawtooth AgriTrace Example',
    author='askmish',
    url='https://github.com/askmish/sawtooth-simplewallet',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'colorlog',
        'protobuf',
        'sawtooth-sdk',
        'sawtooth-signing',
        'PyYAML',
    ],
    data_files=data_files,
    entry_points={
        'console_scripts': [
            'agritrace = agritrace_cli:main_wrapper',
        ]
    })

