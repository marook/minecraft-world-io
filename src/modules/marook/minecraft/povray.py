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
from marook.minecraft.block import getMinecraftBlocksById
from marook.minecraft.block import Block as BlockDef
from marook.minecraft.chunk import ChunkGenerator

def render(f, world, extents = None):
    if extents is None:
        actualExtents = world.extents
    else:
        actualExtents = extents

    blockDefs = getMinecraftBlocksById()

    def getBlockDef(blockId):
        if blockId in blockDefs:
            return blockDefs[blockId]
        else:
            return BlockDef(blockId, 'Default')

    def getCombineOperator(blockDef):
        if blockDef.transparent:
            return 'merge'
        else:
            return 'union'

    def writeBoundedBy(chunk):
        # for the question: why do we generate bounding boxes?
        #
        # from the povray documentation: 'Unbounded unions are always split
        # into their component parts so that automatic bounding works better.'
        #
        # http://www.povray.org/documentation/view/3.6.1/223/#s02_01_02_08_03

        cExtents = chunk.extents

        if cExtents is None:
            return

        # TODO use sphere bounding when we got cubic shapes
        # i guess spheres are faster than boxes?

        f.write('bounded_by { box { <%s, %s, %s>, <%s, %s, %s> } } \n' % (-cExtents[1][0] + 1, cExtents[0][1], cExtents[0][2], -cExtents[0][0] + 1, cExtents[1][1], cExtents[1][2]))


    def writeChunk(chunk, combineOperator, blockId):
        # write chunk subchunks
        for subChunk in chunk.chunks:
            chunksLen = len(subChunk.chunks)
            blocksLen = len(subChunk.blocks)

            if chunksLen == 0 and blocksLen == 0:
                continue

            requireBlock = not ((chunksLen == 0 and blocksLen == 1) or (chunksLen == 1 and blocksLen == 0))

            if requireBlock:
                f.write('%s {\n' % combineOperator)

            writeChunk(subChunk, combineOperator, blockId)

            if requireBlock:
                writeBoundedBy(subChunk)
                f.write('}\n')

        # write chunk blocks
        for blockPos in chunk.blocks:
            f.write('object{ Block%sObject translate <%s, %s, %s>}\n' % (blockId, -blockPos[0], blockPos[1], blockPos[2]))
    
    for blockId, chunk in ChunkGenerator(6).generateChunks(world, actualExtents):
        blockDef = getBlockDef(blockId)
        combineOperator = getCombineOperator(blockDef)

        f.write('// Block%s\n' % blockId)
        f.write('%s {\n' % combineOperator)

        writeChunk(chunk, combineOperator, blockId)
        writeBoundedBy(chunk)
        
        f.write('\tmaterial { Block%sMaterial }\n' % blockId)

        f.write('}\n')
