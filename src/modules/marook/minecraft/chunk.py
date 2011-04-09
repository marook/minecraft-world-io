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

import logging
from marook.minecraft.cache import cache
from marook.minecraft.block import getMinecraftBlocksById, Block

def generatePosFromExtent(extent):
    min, max = extent

    for x in range(min[0], max[0]):
        for z in range(min[2], max[2]):
            for y in range(min[1], max[1]):
                yield (x, y, z)

class Chunk(object):
    
    def __init__(self):
        self._chunks = None
        self._blocks = None

    @property
    def chunks(self):
        if self._chunks is None:
            self._chunks = []

        return self._chunks

    @property
    def blocks(self):
        if self._blocks is None:
            self._blocks = []

        return self._blocks

    @property
    def empty(self):
        return (self._chunks is None or len(self._chunks) == 0) and (self._blocks is None or len(self._blocks) == 0)

    def strip(self):
        if self._chunks is None:
            return

        for c in self._chunks:
            c.strip()

        self._chunks = [c for c in self._chunks if not c.empty]

    @property
    @cache
    def extents(self):
        # TODO right now the extents are only calculated during the first
        # access. 

        eMin = [None,] * 3
        eMax = [None,] * 3

        if not self._chunks is None:
            for c in self._chunks:
                cExtents = c.extents

                if cExtents is None:
                    continue

                cMin, cMax = cExtents
            
                for ch in range(3):
                    if eMin[ch] is None or (not cMin[ch] is None and cMin[ch] < eMin[ch]):
                        eMin[ch] = cMin[ch]

                    if eMax[ch] is None or (not cMax[ch] is None and cMax[ch] > eMax[ch]):
                        eMax[ch] = cMax[ch]

        if not self._blocks is None:
            for pos in self._blocks:
                for ch in range(3):
                    if eMin[ch] is None or pos[ch] < eMin[ch]:
                        eMin[ch] = pos[ch]

                    if eMax[ch] is None or pos[ch] + 1 > eMax[ch]:
                        eMax[ch] = pos[ch] + 1
            
        if eMin[0] is None:
            # eMin[0] == None == eMin[1] == eMin[2] == eMax[0] == eMax[1] == eMax[2]

            return None

        return ((eMin[0], eMin[1], eMin[2]), (eMax[0], eMax[1], eMax[2]))
            

def regions(minIndex, maxIndex, optimalRegionLength, maxRegionCount):
    assert minIndex < maxIndex

    l = maxIndex - minIndex

    optimalRegionCount = int(l / optimalRegionLength)
    if l % optimalRegionLength != 0:
        optimalRegionCount += 1

    if optimalRegionCount < maxRegionCount:
        regionCount = optimalRegionCount
    else:
        regionCount = maxRegionCount

    regionStart = minIndex
    for i in range(regionCount):
        regionEnd = min(maxIndex, minIndex + ((i + 1) * l) / regionCount)

        yield (regionStart, regionEnd)

        regionStart = regionEnd

class ChunkGenerator(object):

    def __init__(self, chunkAxisLen):
        assert chunkAxisLen > 0

        self.chunkAxisLen = chunkAxisLen
        self._blockDefs = getMinecraftBlocksById()
        self._defaultBlockDef = Block(-1, 'Default')

    def _getBlockDef(self, blockId):
        blockDef = self._blockDefs[blockId]

        if blockDef is None:
            return self._defaultBlockDef

        return blockDef

    def _hasSubChunks(self, chunkLen):
        for l in chunkLen:
            if l > self.chunkAxisLen:
                return True

        return False

    def _createSubChunks(self, chunks, world, extent):
        min, max = extent

        for x0, x1 in regions(min[0], max[0], self.chunkAxisLen, self.chunkAxisLen):
            for z0, z1 in regions(min[2], max[2], self.chunkAxisLen, self.chunkAxisLen):
                for y0, y1 in regions(min[1], max[1], self.chunkAxisLen, self.chunkAxisLen):
                    subExtent = ((x0, y0, z0), (x1, y1, z1))

                    subChunks = [Chunk() for blockId in range(256)]
                    
                    for i in range(256):
                        chunks[i].chunks.append(subChunks[i])

                    self._feedChunks(subChunks, world, subExtent)

                    # stripping immediately after feeding to free memory
                    # objects (which are actually dicts) need 'a lot' of
                    # memory in python
                    for c in subChunks:
                        c.strip()

    def _isBlockHidden(self, world, blockPos):
        def isHidingOtherBlocks(pos):
            blockId = world.getBlock(pos[0], pos[1], pos[2])

            if blockId is None:
                return False
            
            blockDef = self._getBlockDef(blockId)

            return blockDef.cube and not blockDef.transparent and not blockDef.invisible

        bp = blockPos
            
        return isHidingOtherBlocks((bp[0] - 1, bp[1], bp[2])) and isHidingOtherBlocks((bp[0], bp[1] - 1, bp[2])) and isHidingOtherBlocks((bp[0], bp[1], bp[2] - 1)) and isHidingOtherBlocks((bp[0] + 1, bp[1], bp[2])) and isHidingOtherBlocks((bp[0], bp[1] + 1, bp[2])) and isHidingOtherBlocks((bp[0], bp[1], bp[2] + 1))

    def _feedChunks(self, chunks, world, extent):
        logging.debug('Feeding chunks for %s' % (extent,))

        min, max = extent

        chunkLen = [max[ch] - min[ch] for ch in range(3)]

        if self._hasSubChunks(chunkLen):
            self._createSubChunks(chunks, world, extent)
        else:
            for pos in generatePosFromExtent(extent):
                posBlockId = world.getBlock(pos[0], pos[1], pos[2])

                if posBlockId is None:
                    continue

                blockDef = self._getBlockDef(posBlockId)
                if blockDef.invisible:
                    continue

                if self._isBlockHidden(world, pos):
                    continue

                chunk = chunks[posBlockId]

                chunk.blocks.append(pos)

    def generateChunks(self, world, extent):
        assert not world is None

        chunks = [Chunk() for blockId in range(256)]

        self._feedChunks(chunks, world, extent)

        for blockId in range(256):
            chunk = chunks[blockId]

            chunk.strip()

            if chunk.empty:
                continue

            yield blockId, chunks[blockId]
