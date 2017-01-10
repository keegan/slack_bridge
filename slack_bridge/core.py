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

import asyncio
import collections
import os
import time
import threading
from . import config, irc, slack


class Bridge(object):

    def __init__(self, directory):
        self.event = threading.Event()
        self.config = config.get_config(os.path.join(directory, 'config.cfg'))
        self.channels = self.config['core']['channels'].split(',')
        self.slack = slack.SlackBridge(self.config['api']['token'])
        self.irc = collections.defaultdict(list)
        self.loop = asyncio.get_event_loop()
        for channel in self.channels:
            members = self.slack.channels.get(channel, None)
            if members is None:
                slack_chans = ','.join(self.slack.channels.keys())
                raise Exception("{} not in {}".format(channel, slack_chans))
            for nick in members:
                self.irc[nick].append(irc.IrcBridge(self.event, '#{}'.format(channel), '{}_slack'.format(nick)))

    def connect(self):
        self.loop.set_debug(True)
        self.loop.run_forever()

    def shutdown(self):
        # TODO(pefoley): There *has* to be a better way to do this...
        self.event.wait()
        self.loop.stop()
        while self.loop.is_running():
            time.sleep(0.1)
        self.loop.close()


def init(directory: str):
    bridge = Bridge(directory)
    threading.Thread(target=bridge.shutdown).start()
    bridge.connect()
