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
from marook.minecraft.debug import isDebugMode

def readString(f):
    # TODO write test case
    # TODO replace all manual unpacks with this function call
    # TODO compile struct pattern
    len, = struct.unpack('>h', f.read(2))

    return f.read(len)

def readInt(f):
    # TODO write test case
    # TODO replace all manual unpacks with this function call
    # TODO compile struct pattern
    return struct.unpack('>i', f.read(4))[0]

def readByte(f):
    # TODO write test case
    # TODO replace all manual unpacks with this function call
    # TODO compile struct pattern
    return struct.unpack('>b', f.read(1))[0]

def readWord(f):
    # TODO write test case
    # TODO replace all manual unpacks with this function call
    # TODO compile struct pattern
    return struct.unpack('>h', f.read(2))[0]

def readDoubleTuple3(f):
    # TODO write test case
    # TODO implement me
    return f.read(29)

def readFloatTuple2(f):
    # TODO write test case
    # TODO implement me
    return f.read(13)

def readList(f, defs):
    values = {}

    for i in range(len(defs)):
        key = readString(f)

        value = defs[key](f)

        values[key] = value

        # TODO validate checksum
        readByte(f)

    assert sorted(defs.keys()) == sorted(values.keys()), 'Expected %s but was %s' % (sorted(defs.keys()), values)

    return values

class SkipParser(object):

    def readTag(self, f):
        dataLength, = struct.unpack('>i', f.read(4))

        # TODO use seek insteaf of read?
        f.read(dataLength)

        return self._createTag()

class IntParser(object):

    def readTag(self, f):
        # TODO compile struct in __init__
        v = struct.unpack('>i', f.read(4))

        return self._createTag(v)

class LongParser(object):

    def readTag(self, f):
        # TODO compile struct in __init__
        v = struct.unpack('>q', f.read(8))

        return self._createTag(v)

class ListParser(object):

    def __init__(self, itemParsers):
        self.itemParsers = itemParsers

    def readTag(self, f):
        # TODO interpret this byte... maybe it's a version number?
        f.read(1)

        # TODO interpret this integer
        # i guess it's one of the two following:
        # - the length of the tag's data in bytes
        # - the number of entities
        numberOfEntities = readInt(f)

        entities = []
        for i in range(numberOfEntities):
            entityId, = struct.unpack('>b', f.read(1))

            if not entityId in self.itemParsers and isDebugMode():
                with open('entities_dump_%s__%s_of_%s' % (entityId, i, numberOfEntities), 'w') as f2:
                    f2.write(f.read(1000))

            entityParser = self.itemParsers[entityId]

            entities.append(entityParser.readEntity(f))

        return List(entities)

class List(object):

    def __init__(self, items):
        self.items = items
