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

class Block(object):

    def __init__(self, id, name, transparent = False, invisible = False, scaleable = (True, True, True), cube = True):
        self.id = id
        self.name = name
        self.transparent = transparent
        self.invisible = invisible
        self.scaleable = scaleable
        self.cube = cube

MINECRAFT_BLOCKS = [
    Block(0, 'Air', invisible = True),
    Block(1, 'Stone'),
    Block(2, 'Grass'),
    Block(3, 'Dirt'),
    Block(4, 'Cobblestone'),
    Block(6, 'Sapling', invisible = True),
    Block(7, 'Bedrock'),
    Block(8, 'Water', transparent = True),
    Block(9, 'Stationary Water', transparent = True),
    Block(12, 'Sand'),
    Block(18, 'Leaves', cube = False),
    Block(20, 'Glass', transparent = True),
    Block(37, 'Yellow Flower', cube = False),
    Block(38, 'Red Rose', cube = False),
    Block(39, 'Brown Mushroom', invisible = True),
    Block(40, 'Red Mushroom', invisible = True),
    Block(50, 'Torch', cube = False, scaleable = (False, False, False)),
    Block(51, 'Fire', invisible = True),
    Block(63, 'Sign Post', invisible = True),
    Block(64, 'Wooden Door', invisible = True),
    Block(65, 'Ladder', invisible = True),
    Block(66, 'Rails', invisible = True),
    Block(67, 'Cobblestone Stairs', invisible = True),
    Block(68, 'Wall Sign', invisible = True),
    Block(78, 'Snow', cube = False),
    Block(79, 'Ice', transparent = True),
    Block(85, 'Fence', cube = False)
]

def getMinecraftBlocksById():
    # TODO cache the 'dict' list
    d = [None,] * 256

    for b in MINECRAFT_BLOCKS:
        d[b.id] = b

    return d

def getBlockByName(name):
    # TODO create a dict of all MINECRAFT_BLOCKS and cache the dict

    for b in MINECRAFT_BLOCKS:
        if b.name == name:
            return b

    return None
