#!/usr/bin/env python
#
# Copyright 2011 Markus Pielmeier
#
# This file is part of minecraft-world-io.
#
# minecraft-world-io is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# minecraft-world-io is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with minecraft-world-io.  If not, see <http://www.gnu.org/licenses/>.
#

import unittest
from marook.minecraft.tag.blocks import BlocksParser

def _parseTagData(parser, data):
    from StringIO import StringIO

    stream = StringIO(data)

    return parser.readTag(stream)

class BlocksParserTest(unittest.TestCase):

    def setUp(self):
        super(BlocksParserTest, self).setUp()

        self.parser = BlocksParser()

    def testParse(self):
        # TODO the parsed data is not 100% valid. normally the data
        # block is always 0x8000 bytes long.
        tag = _parseTagData(self.parser, '\x00\x00\x00\x01\x07')

        self.assertEqual(7, tag.get(0, 0, 0))
