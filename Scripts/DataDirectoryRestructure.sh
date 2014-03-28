#!/bin/sh

OPERATING_DIR="$HOME/Dropbox/Thesis/Data"
FILES=$OPERATING_DIR/*/*/*/*/*
OUTPUT_DIR="$OPERATING_DIR/Restructure"
FILENAME_EXTENSION_LENGTH=12

for f in $FILES
do

    length=${#f}
    filename=${f:((length-FILENAME_EXTENSION_LENGTH)):FILENAME_EXTENSION_LENGTH}

    mv "$f" "$OUTPUT_DIR/$filename"

done