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
import logging
import random
import time
import threading
from . import config, irc, slack


# TODO(pefoley): This is terrible, we shouldn't have to do this.
class Proxy(object):
    def __init__(self, bridge):
        self.bridge = bridge

    def from_irc(self, channel, nick, msg):
        # TODO(pefoley): Make this back-and-forth less hacky.
        if nick.strip('_slack') == self.bridge.masters[channel[1:]]:
            logging.debug(msg)
            self.bridge.slack.send(channel, msg.prefix.nick, msg.args[1])

    def from_slack(self, channel, nick, msg):
        self.bridge.event.wait()
        logging.debug(msg)
        self.bridge.irc[channel][nick].send(msg)

    def schedule(self, func):
        asyncio.run_coroutine_threadsafe(func, self.bridge.loop).result()

class Bridge(object):

    def __init__(self, directory):
        self.event = threading.Event()
        self.config = config.get_config(os.path.join(directory, 'config.cfg'))
        self.channels = self.config['core']['channels'].split(',')
        self.proxy = Proxy(self)
        self.slack = slack.SlackBridge(self.proxy, self.config['api']['token'])
        self.irc = collections.defaultdict(dict)
        self.masters = {}
        self.loop = asyncio.get_event_loop()

    def slack_connect(self):
        for channel in self.channels:
            members = self.slack.channels.get(channel, None)
            if members is None:
                slack_chans = ','.join(self.slack.channels.keys())
                raise Exception("{} not in {}".format(channel, slack_chans))
            # TODO(pefoley): Is this really the best way?
            self.masters[channel] = random.choice(members)[0]
            for nick, name in members:
                self.irc[channel][nick]= irc.IrcBridge(self.proxy, '#{}'.format(channel), '{}_slack'.format(nick), name)

    def irc_connect(self):
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
    bridge.slack_connect()
    # TODO(pefoley): Port to asyncio?
    threading.Thread(target=bridge.slack.message_loop).start()
    threading.Thread(target=bridge.shutdown).start()
    bridge.irc_connect()
