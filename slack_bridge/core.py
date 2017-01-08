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

def dump_response(obj: str):
        json.dump(obj, sys.stdout, indent=True)
        sys.stdout.write('\n')

def init(directory: str):
    bridge = Bridge(directory)
    bridge.get_usermap()
    bridge.get_channels()

class Bridge(object):
    def __init__(self, directory: str) -> None:
        self.config = get_config(os.path.join(directory, 'config.cfg'))
        self.client = slackclient.SlackClient(self.config['api']['token'])
        self.usermap = self.get_usermap()

    def get_usermap(self):
        usermap = {}
        users = self.client.api_call('users.list')
        for user in users['members']:
            usermap[user['id']] = user['name']
        return usermap

    def get_channels(self):
        channels = self.client.api_call('channels.list')
        for channel in channels['channels']:
            members = [self.usermap[member] for member in channel['members']]
            print('{}: {}'.format(channel['name'], ', '.join(members)))
