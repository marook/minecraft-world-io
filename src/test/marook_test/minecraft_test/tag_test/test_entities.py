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
from marook.minecraft.tag.entities import SkeletonParser
from marook.minecraft.tag.entities import SheepParser

class SkeletonParserTest(unittest.TestCase):
    
    def testParseSkeleton(self):
        with open(os.path.join('etc', 'dumps', 'skeleton.dump'), 'r') as f:
            p = SkeletonParser()

            s = p.readEntity(f)

            # TODO check skeleton attributes

class SheepParserTest(unittest.TestCase):
    
    def testParseSheep(self):
        with open(os.path.join('etc', 'dumps', 'sheep.dump'), 'r') as f:
            p = SheepParser()

            s = p.readEntity(f)

            # TODO check sheep attributes
