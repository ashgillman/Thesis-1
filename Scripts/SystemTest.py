from subprocess import call, check_output, check_call
from os import environ
from platform import system as checkOS

HOME = environ['HOME']
CLEAN_AUDIO_DIR = "/Audio/Default"
CONVERT_OUTPUT_DIR = "/Audio/Converted"

# Check whether this is running on my mac or windows machine
if checkOS() == "Darwin":
    THESIS_DIR = "/Dropbox/Thesis"
else:
    THESIS_DIR = ""

OPERATING_DIR = str.format("{0}{1}", HOME, THESIS_DIR)

CLEAN_DIR = str.format("{0}{1}", OPERATING_DIR, CLEAN_AUDIO_DIR)
OUTPUT_DIR = str.format("{0}{1}", OPERATING_DIR, CONVERT_OUTPUT_DIR)

results = check_output(["ls", CLEAN_DIR])

results = results.decode("UTF-8").strip("\n").split("\n")

for file in results:

    file = "/" + file
    result2 = check_output(["cp",
                        CLEAN_DIR + file,
                        OUTPUT_DIR + file])

    print(result2)
