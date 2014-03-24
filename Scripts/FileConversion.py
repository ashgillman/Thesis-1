from subprocess import call, check_output, check_call
from os import environ
from platform import system as checkOS

HOME = environ['HOME']
CLEAN_AUDIO_DIR = "/Default"
CONVERT_OUTPUT_DIR = "/Converted"

# Check whether this is running on my mac or windows machine
if checkOS() == "Darwin":
    THESIS_DIR = "/Dropbox/Thesis/Audio"
else:
    THESIS_DIR = ""

OPERATING_DIR = str.format("{0}{1}", HOME, THESIS_DIR)




