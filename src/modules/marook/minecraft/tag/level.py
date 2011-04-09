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

from generic_tags import CompositeTag

class LevelParser(object):
    
    def __init__(self, tagDetectingParser):
        self.tagDetectingParser = tagDetectingParser

    def readTag(self, f):
        # TODO interpret this byte... maybe it's a version number?
        f.read(1)

        tags = {}
        for i in range(11):
            t = self.tagDetectingParser.readTag(f)

            tags[t.chunkTypeName] = t

        return LevelTag(**tags)

class LevelTag(CompositeTag):

    pass
