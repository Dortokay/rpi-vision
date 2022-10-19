# SPDX-FileCopyrightText: 2019 Leigh Johnson
# SPDX-FileCopyrightText: 2022 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The setup script.'''

import subprocess
import platform
from setuptools import setup, find_packages, Command
from distutils.command.build import build as _build


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

common_requirements = []

trainer_requirements = [
    'ansible==2.8.1',
    'tensorflow>=2.1.0',
    'tensorflow-datasets==1.0.2',
    'tensorflow-hub==0.5.0'
]
trainer_requirements = list(map(
    lambda x: x + ';platform_machine=="x86_64"', trainer_requirements
))

rpi32_requirements = [
    'picamera==1.13.0',
    'Pillow==6.0.0',
    'numpy==1.17.1',
    'pygame==1.9.6'
]
rpi32_requirements = list(map(
    lambda x: x + ';platform_machine=="armv7l"', rpi32_requirements))

rpi64_requirements = [
    'picamera2>=0.3.3',
    'Pillow>=8.1.2',
    'numpy>=1.23.3',
    'pygame>=2.1.2'
]
rpi64_requirements = list(map(
    lambda x: x + ';platform_machine=="aarch64"', rpi64_requirements))

requirements = common_requirements + trainer_requirements + rpi32_requirements + rpi64_requirements

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

RPI_LIBS = ['python3-dev', 'cmake']
RPI_CUSTOM_COMMANDS = [['sudo', 'apt-get', 'update'],
                       ['sudo', 'apt-get', 'install', '-y'] + RPI_LIBS
                       ]

TRAINER_DEBIAN_LIBS = ['python3-dev cmake zlib1g-dev']

TRAINER_DEBIAN_CUSTOM_COMMANDS = [['apt-get', 'update'],
                                  ['apt-get', 'install', '-y'] + TRAINER_DEBIAN_LIBS]

TRAINER_DARWIN_LIBS = ['cmake']
TRAINER_DARWIN_CUSTOM_COMMANDS = [['brew', 'update'],
                                  ['brew', 'install'] + TRAINER_DARWIN_LIBS
                                  ]


class CustomCommands(Command):
    '''A setuptools Command class able to run arbitrary commands.'''

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def RunCustomCommand(self, command_list):
        print('Running command: %s' % command_list)
        p = subprocess.Popen(
            command_list,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        # Can use communicate(input='y\n'.encode()) if the command run requires
        # some confirmation.
        stdout_data, _ = p.communicate()
        print('Command output: %s' % stdout_data)
        if p.returncode != 0:
            raise RuntimeError(
                'Command %s failed: exit code: %s' % (
                    command_list, p.returncode)
            )

    def run(self):
        system = platform.system()
        machine = platform.machine()
        distro = platform.linux_distribution()

        if 'x86' in machine and system == 'Linux' and 'debian' in distro:
            if 'debian' in distro:
                for command in TRAINER_DEBIAN_CUSTOM_COMMANDS:
                    self.RunCustomCommand(command)
        elif 'arm' in machine and system == 'Linux' and 'debian' in distro:
            for command in TRAINER_DEBIAN_CUSTOM_COMMANDS:
                self.RunCustomCommand(command)
        elif system == 'Darwin':
            for command in TRAINER_DARWIN_CUSTOM_COMMANDS:
                self.RunCustomCommand(command)
        else:
            raise NotImplementedError(
                'Unsupported Platform: {}. Supported platforms are Debian-derived Linux and Darwin (OS X)'.format(system))


setup(
    author='Leigh Johnson',
    author_email='leigh@data-literate.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='Examples and utilities for getting started with computer vision on a Raspberry Pi usingng Tensorflow',
    install_requires=requirements,
    license='MIT license',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='rpi_vision',
    name='rpi-vision',
    packages=find_packages(include=['rpi_vision']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/adafruit/rpi-vision',
    version='1.0.0',
    zip_safe=False,
)
