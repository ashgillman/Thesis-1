#!/bin/sh

OPERATING_DIR="$HOME/Dropbox/Thesis/Data"
files=$OPERATING_DIR/*/*/*/*

echo "Directory containing the audio data to be converted is \n$OPERATING_DIR"

cd $OPERATING_DIR

find . | egrep -i -o -e .*\.wv[0-9] > Audio_List.txt
# Extract just the file names
find . | egrep -i -o -e .{8}\.wv[0-9] > Audio_Name_List.txt



for f in $files
do
    name=$(find "$f" | egrep -i -o -e .{8}\.wv[0-9])
    echo "Filename is: $name"
done

exit 0
