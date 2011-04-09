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
from marook.minecraft.povray import render
from marook.minecraft.world import World

class TestPovRay(unittest.TestCase):

    def test(self):
        return # currently disabled to save battery

        worldPath = os.path.join('worlds', 'mc2')
        world = World(worldPath)

        for i in range(1024):
            povPath = 'objects_%s.pov' % i

            if os.path.exists(povPath):
                continue

            with open(povPath, 'w') as f:
                render(f, world)

            break
