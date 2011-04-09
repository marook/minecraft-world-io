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

BLOCK_START_INDEX = 0
BLOCK_END_INDEX = 255
OUT_DIR_PATH = 'blocks'

import os.path

def getBlockIndices():
    return range(BLOCK_START_INDEX, BLOCK_END_INDEX + 1)

def getBlockPovFilePath(blockIndex):
    return 'block%s.pov' % blockIndex

def generateBlockPov(blockIndex):
    with open(os.path.join(OUT_DIR_PATH, getBlockPovFilePath(blockIndex)),'w') as f:
        f.write('#include "../demo_blocks_scene.inc"\n')
        f.write('#include "textures/block%s.inc"\n' % blockIndex)
        f.write('object{ Block%sObject material {Block%sMaterial } }\n' % (blockIndex, blockIndex))

def generateBlockPovs():
    for i in getBlockIndices():
        generateBlockPov(i)

def generateMakefile():
    with open(os.path.join(OUT_DIR_PATH, 'Makefile'), 'w') as f:
        f.write('all:')
        for i in getBlockIndices():
            f.write(' block%s.png' % i)
        f.write('\n')

        for i in getBlockIndices():
            blockPovFilePath = getBlockPovFilePath(i)

            f.write('block%s.png: %s ../demo_blocks_scene.inc ../demo_blocks_scene.ini' % (i, blockPovFilePath))

            if(os.path.exists(os.path.join('..', 'textures', 'block%s.inc' % i))):
                f.write(' ../../textures/block%s.inc' % i)
            
            f.write('\n')

            f.write('\tpovray ../demo_blocks_scene.ini %s\n' % blockPovFilePath)

if __name__ == '__main__':
    generateBlockPovs()
    generateMakefile()
