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

import functools
import logging

def cache(f):
    """This annotation is used to cache the result of a method call.
    
    @param f: This is the wrapped function which's return value will be cached.
    @attention: The cache is never deleted. The first call initializes the
    cache. The method's parameters just passed to the called method. The cache
    is not evaluating the parameters.
    """
    
    @functools.wraps(f)
    def cacher(*args, **kwargs):
        obj = args[0]
        
        cacheMemberName = '__' + f.__name__ + 'Cache'
        
        if (not hasattr(obj, cacheMemberName)):
            value = f(*args, **kwargs)
            
            setattr(obj, cacheMemberName, value)
            
            return value
            
        return getattr(obj, cacheMemberName)
    
    return cacher

class TransientCacheEntry(object):

    def __init__(self, value, revision):
        self.value = value
        self.revision = revision

class TransientCache(object):

    def __init__(self, cacheSize):
        assert cacheSize > 0

        self.revision = 0
        self.cacheSize = cacheSize
        self.cache = {}
        self.formerKeys = set()

    def _nextRevision(self):
        self.revision += 1

        assert self.revision > 0

        return self.revision

    def _removeOldestEntry(self):
        oldestEntryKey = None
        oldestEntryRevision = None

        for key, entry in self.cache.iteritems():
            if oldestEntryKey is None or oldestEntryRevision > entry.revision:
                oldestEntryKey = key
                oldestEntryRevision = entry.revision

        if not oldestEntryKey is None:
            del self.cache[oldestEntryKey]

    def __contains__(self, key):
        if not key in self.cache:
            if key in self.formerKeys:
                logging.warn('Formerly cached value for key %s requested.' % key)

            return False

        entry = self.cache[key]

        return True

    def __getitem__(self, key):
        entry = self.cache[key]

        entry.revision = self._nextRevision()
        
        return entry.value

    def __setitem__(self, key, value):
        # None keys are not supported right now as _removeOldestEntry
        # method relys on it.
        assert not key is None

        if len(self.cache) + 1 > self.cacheSize:
            self._removeOldestEntry()

        entry = TransientCacheEntry(value, self._nextRevision())

        self.cache[key] = entry
        self.formerKeys.add(key)
