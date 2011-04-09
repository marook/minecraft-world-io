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

def _toFirstLower(s):
    if(len(s) <= 1):
        return s.lower()

    return s[0:1].lower() + s[1:]

class CompositeTag(object):

    def __init__(self, *args, **kwargs):
        assert len(args) == 0

        for tagName, tagValue in kwargs.items():
            setattr(self, _toFirstLower(tagName), tagValue)
