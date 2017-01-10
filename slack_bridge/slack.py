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

import json
import logging
import sys
import slackclient


class SlackException(Exception):
    pass


def dump_response(obj: str):
    json.dump(obj, sys.stdout, indent=True)
    sys.stdout.write('\n')


class SlackBridge(object):

    def __init__(self, token: str) -> None:
        self.client = slackclient.SlackClient(token)
        self.users = self.get_usermap()
        self.channels = self.get_channels()
        self.membership = {}

    def api(self, method, **kwargs):
        data = self.client.api_call(method, **kwargs)
        logging.debug(data)
        if not data['ok']:
            raise SlackException(data)
        return data

    def send(self, channel: str, username: str, text: str):
        self.api('chat.postMessage', channel=channel, username=username, text=text, as_user=False)

    def get_usermap(self):
        users = {}
        data = self.api('users.list')
        for user in data['members']:
            users[user['id']] = user['name']
        return users

    def get_channels(self):
        channels = {}
        data = self.api('channels.list')
        for channel in data['channels']:
            channels[channel['name']] = [self.users[member] for member in channel['members']]
        return channels
