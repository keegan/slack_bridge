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

import warnings
import logging
import os
import sys

warnings.simplefilter('default')
logging.basicConfig(level=logging.DEBUG)

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, _CURRENT_DIR)

from slack_bridge import core  # noqa

if __name__ == '__main__':
    core.init(_CURRENT_DIR)
