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

from unittest import TestCase
from marook.minecraft.chunk import ChunkGenerator
from marook.minecraft.block import getBlockByName

class WorldMock(object):

    def __init__(self):
        self.blocks = {}

    def append(self, blocks):
        for blockId, blockPos in blocks:
            self.blocks[blockPos] = blockId

    def getBlock(self, x, y, z):
        pos = (x, y, z)

        if pos in self.blocks:
            return self.blocks[pos]
            
        return None

class AbstractChunkGeneratorTest(TestCase):

    def _mapChunksToBlockIds(self, chunkIterator):
        chunks = {}

        for blockId, chunk in chunkIterator:
            # make sure there are no duplicate chunks
            self.assertTrue(not blockId in chunks)

            chunks[blockId] = chunk

        return chunks

class ChunkGeneratorConstructorTest(TestCase):
    
    def testConstructor(self):
        chunkAxisLen = 4

        cg = ChunkGenerator(chunkAxisLen)
        self.assertEqual(chunkAxisLen, cg.chunkAxisLen)

class OneChunkWorldChunkGeneratorTest(AbstractChunkGeneratorTest):

    def setUp(self):
        super(OneChunkWorldChunkGeneratorTest, self).setUp()

        self.chunkGenerator = ChunkGenerator(4)

    def _generateChunks(self, world):
        chunks = self.chunkGenerator.generateChunks(world, ((0, 0, 0), (self.chunkGenerator.chunkAxisLen, self.chunkGenerator.chunkAxisLen, self.chunkGenerator.chunkAxisLen)))

        return self._mapChunksToBlockIds(chunks)

    def testOneChunkForSmallWorld(self):
        stoneBlockId = 1
        stoneBlockPos = [
            (0, 0, 0),
            (self.chunkGenerator.chunkAxisLen - 1, self.chunkGenerator.chunkAxisLen - 1, self.chunkGenerator.chunkAxisLen - 1)
            ]

        world = WorldMock()
        world.append([(stoneBlockId, pos) for pos in stoneBlockPos])

        chunks = self._generateChunks(world)

        self.assertEqual(1, len(chunks))

        self.assertTrue(stoneBlockId in chunks)

        chunk = chunks[stoneBlockId]

        self.assertEqual(0, len(chunk.chunks))

        self.assertEqual(2, len(chunk.blocks))
        for pos in stoneBlockPos:
            self.assertTrue(pos in chunk.blocks)

    def _validateChunk(self, chunks, expectedBlockId, expectedBlockPos):
        self.assertTrue(expectedBlockId in chunks)

        chunk = chunks[expectedBlockId]

        self.assertEqual(0, len(chunk.chunks))

        self.assertEqual(1, len(chunk.blocks))
        self.assertEqual(expectedBlockPos, chunk.blocks[0])

    def testMultipleBlockTypesChunksForSmallWorld(self):
        stoneBlockId = 1
        stoneBlockPos = (1, 1, 1)

        grassBlockId = 2
        grassBlockPos = (0, 1, 2)

        world = WorldMock()
        world.append([(stoneBlockId, stoneBlockPos), (grassBlockId, grassBlockPos)])

        chunks = self._generateChunks(world)

        self.assertEqual(2, len(chunks))

        self._validateChunk(chunks, stoneBlockId, stoneBlockPos)

        self._validateChunk(chunks, grassBlockId, grassBlockPos)

class MultipleChunksWorldChunkGeneratorTest(AbstractChunkGeneratorTest):

    def setUp(self):
        super(MultipleChunksWorldChunkGeneratorTest, self).setUp()

        self.chunkGenerator = ChunkGenerator(6)

    def _generateChunks(self, world):
        chunks = self.chunkGenerator.generateChunks(world, ((0, 0, 0), (12, 12, 12)))

        return self._mapChunksToBlockIds(chunks)


    def _createWorld(self, blockId, blockPos):
        world = WorldMock()
        world.append([(blockId, p) for p in blockPos])

        return world

    def _createChunk(self, blockId, blockPos):
        world = self._createWorld(blockId, blockPos)

        chunks = self._generateChunks(world)

        self.assertTrue(1, len(chunks))
        self.assertTrue(blockId in chunks)

        return chunks[blockId]

    def _isBlockPosInChunk(self, chunk, blockPos):
        for b in chunk.blocks:
            if b == blockPos:
                return True

        return False

    def _validateBlockPosInChunk(self, chunk, blockPos):
        chunkBlockPos = set()
        for c in chunk.chunks:
            self.assertEqual([], c.chunks)

            blocks = c.blocks

            self.assertEqual(1, len(blocks))

            for b in blocks:
                chunkBlockPos.add(b)

        for bp in blockPos:
            self.assertTrue(bp in chunkBlockPos)
        

    def testCubicChunkDistribution(self):
        blockId = 1
        blockPos = [(0, 0, 0), (8, 8, 8)]

        chunk = self._createChunk(blockId, blockPos)

        self.assertEqual([], chunk.blocks)

        self.assertEqual(2, len(chunk.chunks))

        self._validateBlockPosInChunk(chunk, blockPos)

    def testNonCubicChunkDistribution(self):
        blockId = 1
        blockPos = [(0, 0, 0), (8, 0, 8)]

        chunk = self._createChunk(blockId, blockPos)

        self.assertEqual([], chunk.blocks)

        self.assertEqual(2, len(chunk.chunks))

        self._validateBlockPosInChunk(chunk, blockPos)

    def _isCenterBlockRemaining(self, blockDef): 
        # this is something like a '3D cross'
        blockPos = [(1, 0, 1), (0, 1, 1), (1, 1, 0), (2, 1, 1), (1, 1, 2), (1, 2, 1), (1, 1, 1)]

        chunk = self._createChunk(blockDef.id, blockPos)

        # i admit... right now i don't really know why this is necessary
        # maybe it's a bug?
        chunk = chunk.chunks[0]

        return self._isBlockPosInChunk(chunk, (1, 1, 1))
       

    def testDropBlocksWhichAreSurroundedBySolidBlocks(self):
        blockDef = getBlockByName('Stone')
        
        # make sure our block got the expected attributes
        self.assertTrue(blockDef.cube)
        self.assertFalse(blockDef.transparent)
        self.assertFalse(blockDef.invisible)

        self.assertFalse(self._isCenterBlockRemaining(blockDef))

    def testRemainBlocksWhichAreSurroundedByTransparentBlocks(self):
        blockDef = getBlockByName('Water')
        
        # make sure our block got the expected attributes
        self.assertTrue(blockDef.cube)
        self.assertTrue(blockDef.transparent)
        self.assertFalse(blockDef.invisible)

        self.assertTrue(self._isCenterBlockRemaining(blockDef))
