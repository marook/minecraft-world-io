#!/bin/bash

appendInclude()
{
    echo "#include \"textures/$1\"" >> 'all.inc'
}

echo "" > 'all.inc'
appendInclude "default.inc"

for f in block*.inc
do
    if [ "$f" == "all.inc" ]
    then
	continue
    fi

    appendInclude "$f"
done
