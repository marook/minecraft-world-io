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

import struct

CHUNK_BLOCK_X_LEN = 16
CHUNK_BLOCK_Y_LEN = 128
CHUNK_BLOCK_Z_LEN = 16

class BlocksParser(object):

    def readTag(self, f):
        numberOfBlocks, = struct.unpack('>i', f.read(4))

        blockIds = []
        for i in range(numberOfBlocks):
            blockId, = struct.unpack('>B', f.read(1))

            blockIds.append(blockId)

        return BlocksTag(blockIds)

class BlocksTag(object):

    def __init__(self, blockIds):
        self.blockIds = blockIds

    def get(self, x, y, z):
        """Returns the block ID for the specified position.

        A block ID reference can be found here:
        http://www.minecraftwiki.net/wiki/Data_values#Block_IDs
        """

        # TODO centralize this assertion
        assert((x >= 0) and (x <= CHUNK_BLOCK_X_LEN)), 'x is %s' % x
        assert((y >= 0) and (y <= CHUNK_BLOCK_Y_LEN)), 'y is %s' % y
        assert((z >= 0) and (z <= CHUNK_BLOCK_Z_LEN)), 'z is %s' % z

        #return self.blockIds[y + (z + (x) * CHUNK_BLOCK_Z_LEN) * CHUNK_BLOCK_Y_LEN]
        return self.blockIds[y + (z * CHUNK_BLOCK_Y_LEN + (x * CHUNK_BLOCK_Y_LEN * CHUNK_BLOCK_Z_LEN))]
