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
from marook.minecraft.world import RegionFileNameMatcher

class RegionFileNameMatcherTest(TestCase):

    def validateRegionFileNameMatch(self, regionFileName, expectedX, expectedZ):
        m = RegionFileNameMatcher(regionFileName)

        self.assertTrue(m.matches)
        self.assertEqual(expectedX, m.x)
        self.assertEqual(expectedZ, m.z)

    def testWithMatchingFileNames(self):
        self.validateRegionFileNameMatch('r.-2.0.mcr', -2, 0)
        self.validateRegionFileNameMatch('r.0.10.mcr', 0, 10)

    def testWithoutMatchingFileName(self):
        self.assertFalse(RegionFileNameMatcher('r..0.mcr').matches)
        self.assertFalse(RegionFileNameMatcher('r.0..mcr').matches)
        self.assertFalse(RegionFileNameMatcher('_r.0.0.mcr').matches)
        self.assertFalse(RegionFileNameMatcher('r.0.0.mcr_').matches)
        self.assertFalse(RegionFileNameMatcher('r_0.0.mcr').matches)
        self.assertFalse(RegionFileNameMatcher('r.0_0.mcr').matches)
        self.assertFalse(RegionFileNameMatcher('r.0.0_mcr').matches)
        self.assertFalse(RegionFileNameMatcher('r.x.x_mcr').matches)
