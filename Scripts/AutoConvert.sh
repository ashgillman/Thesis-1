#!/bin/sh

OPERATING_DIR="$HOME/Dropbox/Thesis/Data"
FILES=$OPERATING_DIR/*/*/*/*/*
OUTPUT="$HOME/Documents/Data"

OPERATING_SIZE=${#OPERATING_DIR}

echo "Directory containing the audio data to be converted is \n$OPERATING_DIR"

for f in $FILES
do

    # Grab the underlying directory structure for the data
    dirStruct=${f:$OPERATING_SIZE}
    length=${#dirStruct}
    length=$((length-13))
    dirStruct=${dirStruct:0:length}

    # Create the directory structure for the output data
    mkdir -p "$OUTPUT$dirStruct"

    # Find all files within the FILES directory that end with .wv1/2
	name=$(find "$f" | egrep -i -o -e .*\.wv[1,2])

    # Determine the length of the found string
    size=${#name}

    # Subtract 4 from the length of the string (extension .wv*)
    size=$((size-4))

    # Check whether or not the length is > 0
    # Length < 0 represents no .wv* extension
    # Copy all the pheonetic/word data into the conversion folders
    if [ $size -le 0 ]
    then
        copyfile=${f:$OPERATING_SIZE}
        cp -f "$f" "$OUTPUT$copyfile"
        continue
    fi

    # Strip the file extension off the name string
    name=${name:0:$size}

    # Strip the abitrary OPERATING_DIR directories from the string
    name=${name:$OPERATING_SIZE}

    # Run the .wv* to .wav conversion
    sph2pipe -p -f rif "$f" "$OUTPUT$name.wav"

done

exit 0
