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

import os.path
import struct
from marook.minecraft.cache import cache
from marook.minecraft.cache import TransientCache
from marook.minecraft.tag.parser import getSuperSmartTagDetectingParser
import logging
import re

SIZE_OF_INT = 4
BYTES_PER_SECTOR = 4096
INTS_PER_SECTOR = BYTES_PER_SECTOR / SIZE_OF_INT

BLOCKS_PER_REGION_X = 32
BLOCKS_PER_REGION_Z = 32

class Offsets(object):

    def __init__(self, offsets):
        self.offsets = offsets

    def get(self, x, z):
        return self.offsets[x + z * BLOCKS_PER_REGION_X]

    def getSectorNumber(self, x, z):
        o = self.get(x, z)

        return o >> 8

    def getNumberOfSectors(self, x, z):
        o = self.get(x, z)

        return o & 0xff

    def getSectorFilePosition(self, x, z):
        sn = self.getSectorNumber(x, z)

        return sn * BYTES_PER_SECTOR

class Sector(object):
    
    def __init__(self, regionPath, fileOffset):
        self.regionPath = regionPath
        self.fileOffset = fileOffset

        self._tag = None

    def getBlock(self, x, y, z):
        if(not self._tag is None):
            return self._tag.blocks.get(x, y, z)

        with open(self.regionPath, 'r') as f:
            f.seek(self.fileOffset)

            length = struct.unpack('>i', f.read(SIZE_OF_INT))[0]

            assert(length > 1)

            compressionVersion = struct.unpack('>b', f.read(1))[0]

            if(compressionVersion == 1):
                # TODO refactor to separate artifact which cares about gzip
                raise Exception('GZIP is not yet supported')
            elif(compressionVersion == 2):
                import zlib
                from StringIO import StringIO

                # TODO refactor to separate artifact which cares about deflate

                # TODO replace with some streaming api
                data = f.read(length - 1)

                # more infos about the deflate decompression
                # http://stackoverflow.com/questions/1089662/python-inflate-and-deflate-implementations
                chunk = StringIO(zlib.decompress(data)[4:-2])

                p = getSuperSmartTagDetectingParser()

                self._tag = p.readTag(chunk)

                return self._tag.blocks.get(x, y, z)
            else:
                raise ValueError('compression version was %s' % compressionVersion)

class Region(object):

    def __init__(self, regionPath):
        if(not os.path.isfile(regionPath)):
            raise ValueError()

        self.regionPath = regionPath

        self.sectorsCache = TransientCache(3 * 3 * 3)

    @property
    @cache
    def offsets(self):
        logging.debug('Parsing offsets for region %s' % self.regionPath)

        s = struct.Struct('>i')
            
        with open(self.regionPath, 'r') as f:
            offsets = []

            for i in range(0, INTS_PER_SECTOR):
                offsets.append(s.unpack(f.read(SIZE_OF_INT))[0])

            return Offsets(offsets)

    def getSector(self, x, y, z):
        assert((x >= 0) and (x < BLOCKS_PER_REGION_X)), 'x was %s' % x
        assert((z >= 0) and (z < BLOCKS_PER_REGION_Z)), 'z was %s' % z

        sectorFilePos = self.offsets.getSectorFilePosition(x, z)

        if sectorFilePos in self.sectorsCache:
            return self.sectorsCache[sectorFilePos]

        # TODO separate caching logic from sector creation
        s = Sector(self.regionPath, sectorFilePos)
        self.sectorsCache[sectorFilePos] = s

        return s

class RegionFileNameMatcher(object):

    PATTERN = re.compile('^r[.](-?[\\d]+)[.](-?[\\d]+)[.]mcr$')

    def __init__(self, regionFileName):
        self.matches = RegionFileNameMatcher.PATTERN.match(regionFileName)

        if self.matches:
            self.x = int(self.matches.group(1))
            self.z = int(self.matches.group(2))

class World(object):

    @property
    def _regionDirPath(self):
        return os.path.join(self.worldPath, 'region')

    def __init__(self, worldPath):
        if(not os.path.isdir(worldPath)):
            raise ValueError()

        self.worldPath = worldPath
        self.regionsCache = TransientCache(4)
        self.brokenPos = set()

    def _getRegionPath(self, x, z):
        regionFile = 'r.' + str(x / BLOCKS_PER_REGION_X) + '.' + str(z / BLOCKS_PER_REGION_Z) + '.mcr'

        return os.path.join(self._regionDirPath, regionFile)

    @property
    def extents(self):
        minX = None
        maxX = None

        minZ = None
        maxZ = None

        regionDirPath = self._regionDirPath
        for f in os.listdir(regionDirPath):
            if not os.path.isfile(os.path.join(regionDirPath, f)):
                continue

            m = RegionFileNameMatcher(f)
            if not m.matches:
                continue

            if minX is None or minX > m.x:
                minX = m.x

            if minZ is None or minZ > m.z:
                minZ = m.z

            if maxX is None or maxX < m.x:
                maxX = m.x

            if maxZ is None or maxZ < m.z:
                maxZ = m.z

        blocksPerRegion = (32 * 16, 0, 32 * 16)

        # TODO handle minX|maxX|minZ|maxZ is None
        return ((minX * blocksPerRegion[0], 0, minZ * blocksPerRegion[2]), ((maxX + 1) * blocksPerRegion[0], 128, (maxZ + 1) * blocksPerRegion[2]))

    def getBlock(self, x, y, z):
        # TODO change method signature: method should only take one position
        # argument

        # TODO rename method to getBlockId

        if (x, z) in self.brokenPos:
            return None

        try:
            regionPath = self._getRegionPath(x / 16, z / 16)

            # TODO separate caching logic from block determination
            if regionPath in self.regionsCache:
                r = self.regionsCache[regionPath]
            else:
                r = Region(regionPath)

                self.regionsCache[regionPath] = r

            s = r.getSector((x / 16) % BLOCKS_PER_REGION_X, y, (z / 16) % BLOCKS_PER_REGION_Z)

            return s.getBlock(x % 16, y, z % 16)

        except Exception as e:
            logging.exception('Can\'t read pos %s/%s/%s' % (x, y, z))

            self.brokenPos.add((x, z))

            return None
