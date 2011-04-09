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
from marook.minecraft.world import Offsets

class TestOffsetsOperations(TestCase):

    def setUp(self):
        super(TestOffsetsOperations, self).setUp()

        self.offsets = Offsets([0x00000201, ])

    def testGetSectorNumber(self):
        self.assertEqual(2, self.offsets.getSectorNumber(0, 0))

    def testGetNumberOfSectors(self):
        self.assertEqual(1, self.offsets.getNumberOfSectors(0, 0))

    def testGetSectorFilePosition(self):
        self.assertEqual(2 * 4096, self.offsets.getSectorFilePosition(0, 0))
