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
from marook.minecraft.chunk import Chunk

class ChunkTest(TestCase):

    def testExtentsChunkWithoutExtents(self):
        c = Chunk()

        self.assertEqual(None, c.extents)

    def testExtentsFromChildBlocks(self):
        c = Chunk()
        c.blocks.append((1, 2, 3))
        c.blocks.append((-2, 4, 1))

        self.assertEqual(((-2, 2, 1), (2, 5, 4)), c.extents)

    def testExtentsFromChildCunks(self):
        cChild = Chunk()
        cChild.blocks.append((1, 2, 3))
        cChild.blocks.append((-2, 4, 1))

        cParent = Chunk()
        cParent.chunks.append(cChild)

        self.assertEqual(((-2, 2, 1), (2, 5, 4)), cParent.extents)
