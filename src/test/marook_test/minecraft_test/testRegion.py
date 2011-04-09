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

import os
import unittest
from marook.minecraft.world import Region

class TestRegionOffsets(unittest.TestCase):

    def testOffsets(self):
        r = Region(os.path.join('worlds', 'mc2', 'region', 'r.0.0.mcr'))

        offsets = r.offsets

        expectedOffsets = [
            [ 513, 5121, 11777, 178946],
            [ 2049, 21249]
            ]

        for z in range(len(expectedOffsets)):
            col = expectedOffsets[z]

            for x in range(len(col)):
                sectorFilePos = offsets.getSectorFilePosition(x, z)
                self.assertTrue((sectorFilePos >= 0x1000) and (sectorFilePos <= 0x308ffff), 'sectorFilePos was %s' % sectorFilePos)

                expectedOffset = col[x]
                offset = offsets.get(x, z)

                self.assertEqual(expectedOffset, offset, '%s != %s (x/z = %s/%s)' % (expectedOffset, offset, x, z))
