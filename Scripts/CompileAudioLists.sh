#!/bin/sh

# Initialise all the folder locations
OPERATING_DIR="$HOME/Dropbox/Thesis"
DATA_DIR="$OPERATING_DIR/Data/Restructure"
TRAINING_DIR="$DATA_DIR/Audio/TrainingData"
TEST_DIR="$DATA_DIR/Audio/TestData"
MFC_DIR="$DATA_DIR/MFCData"

EXTENSION_LENGTH=4

WAV_EXTENSION="\.wav"
MFC_EXTENSION=".mfc"

# Specify the ouput file names
WAV_TEXT_FILE="AudioFiles.txt"
MFC_OUTPUT="MFCData.scp"

cd $DATA_DIR

# Find all .wav files in the training data and store them in a training output
# file
find "$TRAINING_DIR" | egrep -i -e "$WAV_EXTENSION" > "Training$WAV_TEXT_FILE"

# Find all .wav files in the testing data and store them in a testing output file
find "$TEST_DIR" | egrep -i -e "$WAV_EXTENSION" > "Testing$WAV_TEXT_FILE"

# Compile a input/output list for the mfc conversion for the Training data
for line in $(cat "Training$WAV_TEXT_FILE")
do
    # Get length of directory path
    length=${#TRAINING_DIR}

    # Strip the extension off the line
    newFile=${line:$length:9}

    # Append new extension
    newFile="$MFC_DIR/Training$newFile$MFC_EXTENSION"

    # Write the input/output to new file
    echo "$line $newFile" >> "$MFC_DIR/Training$MFC_OUTPUT"

done

# Compile a input/output list for the mfc conversion for the Testing Data
for line in $(cat "Testing$WAV_TEXT_FILE")
do
# Get length of directory path
length=${#TEST_DIR}

# Strip the extension off the line
newFile=${line:$length:9}

# Append new extension
newFile="$MFC_DIR/Testing$newFile$MFC_EXTENSION"

# Write the input/output to new file
echo "$line $newFile" >> "$MFC_DIR/Testing$MFC_OUTPUT"

done

exit 0