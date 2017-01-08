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

import configparser
import os
import sys
import json
import slackclient


def get_config(path: str) -> configparser.ConfigParser:
    config_obj = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    with open(path) as f:
        config_obj.read_file(f)
    return config_obj


def init(directory: str):
    config = get_config(os.path.join(directory, 'config.cfg'))
    client = slackclient.SlackClient(config['api']['token'])
    channels = client.api_call('channels.list')
    json.dump(channels, sys.stdout, indent=True)
    sys.stdout.write('\n')
