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

import struct
from generic_parser import readString, readInt, readByte, readWord, readList, ListParser

class SignParser(object):

    ENTITY_DEF = {
        'x': readInt,
        'y': readInt,
        'z': readInt,
        'Text1': readString,
        'Text2': readString,
        'Text3': readString,
        'Text4': readString,
        'id': readString
        }

    def readEntity(self, f):
        obj = readList(f, SignParser.ENTITY_DEF)

        return Sign(obj['x'], obj['y'], obj['z'], [obj['Text1'], obj['Text2'], obj['Text3'], obj['Text4']])

class Sign(object):

    def __init__(self, x, y, z, text):
        self.x = x
        self.y = y
        self.z = z
        self.text = text

class ChestParser(object):

    CHEST_ITEM_DEF = {
        'Damage': readWord,
        'Slot': readByte,
        'Count': readByte,
        'id': readWord
        }

    CHEST_ATTR_DEF = {
        'x': readInt,
        'y': readInt,
        'z': readInt,
        'id': readString
        }

    def readEntity(self, f):
        assert readString(f) == 'Items'
        # TODO validate checksum
        readByte(f)

        itemCount = readInt(f)

        # TODO validate checksum
        readByte(f)

        for i in range(itemCount):
            # TODO store parsed items in chest
            readList(f, ChestParser.CHEST_ITEM_DEF)

            readByte(f)

        # TODO store parsed chest attributes in chest
        readList(f, ChestParser.CHEST_ATTR_DEF)
        
        return Chest()

class Chest(object):

    pass

class TileEntitiesParser(ListParser):

    def __init__(self):
        super(TileEntitiesParser, self).__init__({
            0x03: SignParser(),
            0x09: ChestParser()
            })
