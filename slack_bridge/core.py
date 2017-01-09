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
import time
import threading
from . import irc, slack

event = threading.Event()

def shutdown(loop, bridge):
    event.wait()
    loop.stop()
    while loop.is_running():
        time.sleep(0.1)
    loop.close()
    bridge.client.irc.shutdown()


def init(directory: str):
    slack_bridge = slack.SlackBridge(directory)
    slack_bridge.get_usermap()
    slack_bridge.get_channels()
    irc_bridge = irc.IrcBridge(event)
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    thread = threading.Thread(target=shutdown, args=[loop, irc_bridge]).start()
    loop.run_forever()
