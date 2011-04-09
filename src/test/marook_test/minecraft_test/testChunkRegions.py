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
from marook.minecraft.chunk import regions

class RegionsTest(TestCase):

    def _regions(self, *args):
        return [r for r in regions(*args)]

    def testOptimalRegionLength(self):
        r = self._regions(0, 4, 2, 10)

        self.assertEqual([(0, 2), (2, 4)], r)

    def testMaxRegionCount(self):
        r = self._regions(0, 4, 1, 2)
        
        self.assertEqual([(0, 2), (2, 4)], r)

    def testLastRegionIsShrinkedWhenNecessary(self):
        r = self._regions(0, 5, 3, 100)

        self.assertTrue(r == [(0, 3), (3, 5)] or r == [(0, 2), (2, 5)], 'r = %s' % r)

    def testRegionMinIndexIsNotZeroBug(self):
        r = self._regions(1, 2, 1, 100)

        self.assertEqual([(1, 2), ], r)

    def testNegativeRangeRegions(self):
        r = self._regions(-2, 2, 2, 100)

        self.assertEqual([(-2, 0), (0, 2)], r)
