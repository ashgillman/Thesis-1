#!/bin/sh

OPERATING_DIR="$HOME/Dropbox/Thesis/"
CONFIG_FILE="Configs/MFCConfig.mfc"
CLASSIFIER_DIR="Code/ClassifierOutput/"
AUDIO_DIR="$HOME/Dropbox/Thesis/Audio"
lengthVariableCauseWindowsIsFucked=${#AUDIO_DIR}
AUDIO_DIR=${$AUDIO_DIR:0:$lengthVariableCauseWindowsIsFucked-6}

# Size of the standard operating directory structure
OPERATING_SIZE=${#OPERATING_DIR}

# Length of the default filename + ext (/C*******.ext)
FILE_AND_EXT_LENGTH=13

audioFiles="$AUDIO_DIR/*"

echo $HOME
echo $OPERATING_DIR
echo $AUDIO_DIR
echo $audioFiles

for f in $audioFiles
do
    # Grab the underlying directory structure for the data
    dirStruct=${f:$OPERATING_SIZE}
    length=${#dirStruct}
    length=$((length-FILE_AND_EXT_LENGTH))
    dirStruct=${dirStruct:0:length}

    # Find all files within the FILES directory that end with .wv1/2
    name=$(find "$f" | egrep -i -o -e .*\.wav)

    # Determine the length of the found string
    size=${#name}

    # Subtract 4 from the length of the string (extension .wv*)
    size=$((size-4))

    # Check whether or not the length is > 0
    # Length < 0 represents no .wv* extension
    # Copy all the pheonetic/word data into the conversion folders
    if [ $size -gt 0 ]
    then
        echo $name
        continue
        HCopy -T 1 -C $CONFIG_FILE "$AUDIO_DIR/$name.wav"
    continue
    fi

    # Strip the file extension off the name string
    name=${name:0:$size}

    # Strip the abitrary OPERATING_DIR directories from the string
    name=${name:$OPERATING_SIZE}

done

exit 0