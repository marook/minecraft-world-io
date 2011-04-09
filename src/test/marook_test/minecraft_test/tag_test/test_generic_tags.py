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

from marook.minecraft.tag.generic_tags import CompositeTag
import unittest

class CompositeTagTest(unittest.TestCase):

    def testKWArgsConstructor(self):
        t = CompositeTag(Value = 0, AValue = 1)

        self.assertEqual(0, t.value)
        self.assertEqual(1, t.aValue)

    def testDictArgsConstructor(self):
        # this more a test whether i understand the ** operator

        attrs = {
            'Value': 0,
            'AValue': 1
            }

        t = CompositeTag(**attrs)

        self.assertEqual(0, t.value)
        self.assertEqual(1, t.aValue)
