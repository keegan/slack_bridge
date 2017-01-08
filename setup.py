#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2017 Peter Foley
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from setuptools import find_packages, setup

setup_requires = ['setuptools', 'setuptools_git']

setup(
    name="SlackBridge",
    description="An irc->slack bridge.",
    author="The TJHSST Computer Systems Lab",
    author_email="cslbot@pefoley.com",
    url="https://github.com/tjcsl/slack_bridge",
    version="0.1",
    license="GPL",
    zip_safe=False,
    packages=find_packages(),
    setup_requires=setup_requires,
    install_requires=setup_requires + ['slackclient'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ],
    keywords=['csl', 'tjhsst', 'tj', 'irc', 'bot'],
    entry_points={'console_scripts': ['bridge = slack_bridge.core:init']})
