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
from marook.minecraft.world import World
from marook.minecraft.block import getBlockByName
import os.path

class TestWorldLoadFails(TestCase):

    def testNoWorldDirectoryExistsFail(self):
        self.assertRaises(Exception, World.__init__, 'noSuchDirectoryForAWorldExists')

class TestWorldWithSuccessfullyLoadedWorld(TestCase):

    def setUp(self):
        super(TestWorldWithSuccessfullyLoadedWorld, self).setUp()

        self.worldPath = os.path.join('worlds', 'mc2')
        self.world = World(self.worldPath)

    def testGetExistingBlock(self):
        self.assertEqual(getBlockByName('Bedrock').id, self.world.getBlock(0, 0, 0))
        self.assertEqual(getBlockByName('Stone').id, self.world.getBlock(-1, 10, -1))

    def testExtents(self):
        self.assertEqual(((-2 * 32 * 16, 0, -1 * 32 * 16), ((1 + 1) * 32 * 16, 128, (2 + 1) * 32 * 16)), self.world.extents)
