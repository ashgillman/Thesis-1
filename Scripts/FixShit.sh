#!/bin/sh

OPERATING_DIR="$HOME/Dropbox/Thesis"
DATA_DIR="$OPERATING_DIR/Data/Restructure"
FOLDERS="$OPERATING_DIR/Code/Scripts/FoldersToFix"
OUTPUT_DIR="$DATA_DIR/Test Data"

DATA_DIR_LENGTH=${#DATA_DIR}

for f in $( cat $FOLDERS )
do
    for file in $( find "$DATA_DIR" | egrep -i -e "$f" )
    do
        strippedName=${file:$DATA_DIR_LENGTH:13}
        mv "$file" "$OUTPUT_DIR$strippedName"
    done
done

exit 0