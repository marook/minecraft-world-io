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
from generic_parser import readString

def getSuperSmartTagDetectingParser():
    """Returns a TagDetectingParser which should know all minecraft tags.
    """

    from level import LevelParser
    from terrain_populated import TerrainPopulatedParser
    from height_map import HeightMapParser
    from blocks import BlocksParser
    from z_pos import ZPosParser
    from data import DataParser
    from sky_light import SkyLightParser
    from tile_entities import TileEntitiesParser
    from entities import EntitiesParser
    from block_light import BlockLightParser
    from last_update import LastUpdateParser
    from x_pos import XPosParser

    p = TagDetectingParser()
    p.tagParser['Level'] = LevelParser(p)
    p.tagParser['TerrainPopulated'] = TerrainPopulatedParser()
    p.tagParser['HeightMap'] = HeightMapParser()
    p.tagParser['Blocks'] = BlocksParser()
    p.tagParser['zPos'] = ZPosParser()
    p.tagParser['Data'] = DataParser()
    p.tagParser['SkyLight'] = SkyLightParser()
    p.tagParser['TileEntities'] = TileEntitiesParser()
    p.tagParser['Entities'] = EntitiesParser()
    p.tagParser['BlockLight'] = BlockLightParser()
    p.tagParser['LastUpdate'] = LastUpdateParser()
    p.tagParser['xPos'] = XPosParser()

    return p


class TagDetectingParser(object):

    def __init__(self, tagParser = {}):
        self.tagParser = tagParser
    
    def readTag(self, f):
        chunkTypeName = readString(f)

        t = self.tagParser[chunkTypeName].readTag(f)

        t.chunkTypeName = chunkTypeName

        # TODO there's a magic byte after every tag... value seems to be 
        # very often 0x07!?!
        # maybe it's a CRC value?
        f.read(1)

        return t
