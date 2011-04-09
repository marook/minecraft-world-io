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
from generic_parser import readString, readInt, readByte, readWord, readList, ListParser, readDoubleTuple3, readFloatTuple2

class SkeletonParser(object):

    ENTITY_DEF = {
        'id': readString,
        'Pos': readDoubleTuple3,
        'AttackTime': readWord,
        'Motion': readDoubleTuple3,
        'HurtTime': readWord,
        'OnGround': readByte,
        'Fire': readWord,
        'Health': readWord,
        'FallDistance': readInt,
        'Air': readWord,
        'Rotation': readFloatTuple2,
        'DeathTime': readWord
        }

    def readEntity(self, f):
        obj = readList(f, SkeletonParser.ENTITY_DEF)

        return Skeleton()
        
class Skeleton(object):
    pass

class SheepParser(object):

    ENTITY_DEF = {
        'id': readString,
        'Pos': readDoubleTuple3,
        'AttackTime': readWord,
        'Motion': readDoubleTuple3,
        'HurtTime': readWord,
        'OnGround': readByte,
        'Fire': readWord,
        'Health': readWord,
        'FallDistance': readInt,
        'Air': readWord,
        'Rotation': readFloatTuple2,
        'DeathTime': readWord,
        'Sheared': readByte,
        'Color': readByte
        }

    def readEntity(self, f):
        obj = readList(f, SheepParser.ENTITY_DEF)

        return Sheep()

class Sheep(object):
    pass

class EntitiesParser(ListParser):

    def __init__(self):
        super(EntitiesParser, self).__init__({
                0x08: SkeletonParser(),
                0x09: SheepParser()
                })
