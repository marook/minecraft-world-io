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
from marook.minecraft.cache import TransientCache

class TransientCacheTest(TestCase):

    def testCacheHit(self):
        cache = TransientCache(1)

        cache['key'] = 'value'

        self.assertTrue('key' in cache)
        self.assertEqual('value', cache['key'])

    def testCacheMissBecauseItemNotInCache(self):
        cache = TransientCache(1)

        self.assertFalse('key' in cache)
        self.assertRaises(KeyError, cache.__getitem__, 'key')

    def testCacheMissBecauseOfCacheCleanup(self):
        cache = TransientCache(1)

        cache['keyOld'] = 'valueOld'
        cache['keyNew'] = 'valueNew'

        self.assertFalse('keyOld' in cache)
        self.assertTrue('keyNew' in cache)

    def testGetItemKeepsItemLongerInCache(self):
        cache = TransientCache(2)

        cache['keyOldOftenAccess'] = 'valueOld'
        cache['keyOldRareAccess'] = 'valueOld'
        
        cache['keyOldOftenAccess']

        cache['keyNew'] = 'valueNew'

        self.assertTrue('keyOldOftenAccess' in cache)

    def testExceptionOnSettingEntryAfterCleanup(self):
        cache = TransientCache(1)

        cache['keyOld'] = 'valueOld'
        cache['keyMid'] = 'valueMid'
        cache['keyNew'] = 'valueNew'

        self.assertFalse('keyOld' in cache)
        self.assertFalse('keyMid' in cache)
        self.assertTrue('keyNew' in cache)
