#!/bin/sh

# Initialise all the folder locations
OPERATING_DIR="$HOME/Dropbox/Thesis"
DATA_DIR="$OPERATING_DIR/Data/Restructure"
FOLDERS="$OPERATING_DIR/Code/Scripts/FoldersToFix"
OUTPUT_DIR="$DATA_DIR/Test Data"

# Specify the length of the filename + extension
FILENAME_EXTENSION_LENGTH=12

# Get the length of the DATA_DIR string, to help strip redundant
# directory information later
DATA_DIR_LENGTH=${#DATA_DIR}

# Loop through all the specified folders (ones that correspond to the testing data)
for f in $( cat $FOLDERS )
do
    # Loop through all the files that match the folder requirements
    for file in $( find "$DATA_DIR" | egrep -i -e "$f" )
    do
        # Strip all the directory structure from the files
        # Leaves just filename.ext
        strippedName=${file:$DATA_DIR_LENGTH:$FILENAME_EXTENSION_LENGTH}

        # Move the files from the bulk data directory to the training directory
        mv "$file" "$OUTPUT_DIR/$strippedName"
    done
done

exit 0