from subprocess import call, check_output, check_call
from os import environ
from platform import system as checkOS

HOME = environ['HOME']

# Check whether this is running on my mac or windows machine
if checkOS() == "Darwin":
    THESIS_DIR = "/Dropbox/Thesis/Audio"
else:
    THESIS_DIR = ""

OPERATING_DIR = str.format("{0}{1}", HOME, THESIS_DIR)

CLEAN_AUDIO_DIR = "/Default"
CONVERT_OUTPUT_DIR = "/Converted"

results = check_output(["ls", OPERATING_DIR + CLEAN_AUDIO_DIR])

results = "/" + results.decode("UTF-8").strip("\n")


result2 = check_output(["mv",
                        OPERATING_DIR + CLEAN_AUDIO_DIR + results,
                        OPERATING_DIR + CONVERT_OUTPUT_DIR + results])
