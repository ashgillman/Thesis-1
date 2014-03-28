#!/bin/sh

# Initialise all the folder locations
OPERATING_DIR="$HOME/Dropbox/Thesis"
DATA_DIR="$OPERATING_DIR/Data/Restructure"
TRAINING_DIR="$DATA_DIR/Training Data"
TEST_DIR="$DATA_DIR/Test Data"

# Specify the ouput file name
OUTPUT_FILE="AudioFiles.scp"

# Find all .wav files in the training data and store them in a training output
# file
find "$TRAINING_DIR" | egrep -i -e "\.wav" > "$DATA_DIR/Training$OUTPUT_FILE"

# Find all .wav files in the testing data and store them in a testing output file
find "$TEST_DIR" | egrep -i -e "\.wav" > "$DATA_DIR/Testing$OUTPUT_FILE"
