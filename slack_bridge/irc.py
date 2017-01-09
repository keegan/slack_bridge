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

from irc2 import client, parser


class IrcBridge(object):

    def __init__(self, event) -> None:
        config = client.IRCClientConfig("chat.freenode.net", 6697)
        config.register("msbob_slack", "msbob_slack", "Microsoft Bob")
        config.join('#msbob')
        self.event = event
        self.client = config.configure()
        # ENDOFNAMES, i.e. we've joined successfully.
        self.client.subscribe(parser.Message(verb=366), self.on_message)

    async def on_message(self, line):
        print(line)
        self.event.set()
