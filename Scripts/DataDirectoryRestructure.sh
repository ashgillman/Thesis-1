#!/bin/sh

# Initialise all the folder locations
OPERATING_DIR="$HOME/Dropbox/Thesis/Data"
FILES=$OPERATING_DIR/*/*/*/*/*
OUTPUT_DIR="$OPERATING_DIR/Restructure/Audio"

# Specify the length of the filename + extension
FILENAME_EXTENSION_LENGTH=12

# Loop through every file contained within the $FILES directory structure
for f in $FILES
do
    # Determine the length of the directory path
    length=${#f}

    # Strip the directory path from the file, leaving only filename.ext
    filename=${f:((length-FILENAME_EXTENSION_LENGTH)):FILENAME_EXTENSION_LENGTH}

    # Move the data from old location to new location
    mv "$f" "$OUTPUT_DIR/$filename"

done