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

    def __init__(self, proxy, channel, nick, name) -> None:
        config = client.IRCClientConfig("chat.freenode.net", 6697)
        config.register(nick, nick, name)
        config.join(channel)
        self.nick = nick
        self.channel = channel
        self.proxy = proxy
        self.client = config.configure()
        self.client.subscribe(parser.Message(), self.on_message)

    def send(self, msg):
        import logging
        logging.error(msg)
        self.proxy.schedule(self.client.say(self.channel, msg))

    async def on_message(self, msg):
        # ENDOFNAMES, i.e. we've joined successfully.
        if msg.verb == 366:
            print("Joined {}".format(msg))
        elif msg.verb == "PRIVMSG":
            self.proxy.from_irc(self.channel, self.nick, msg)
