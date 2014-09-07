import os
import platform

""" Define System Directory Constants """
if platform.system() == "Windows":
    FILE_START = "F:\\Thesis\\External\\"
    SEPARATOR = "\\"
else:
    FILE_START = "/Volumes/External/"
    SEPARATOR = "/"

# Directory Constants
TRAINING_DIR = str.format("{0}ClassifierTraining{1}", FILE_START, SEPARATOR)

AUDIO_DIR = str.format("{0}ConvertData{1}ThesisData{1}Desk{1}Testing{1}", FILE_START, SEPARATOR)
TRAINING_AUDIO_DIR = str.format("{0}Development{1}", AUDIO_DIR, SEPARATOR)
PHONEME_EXT = ".phn"

for root, subdirs, files in os.walk(TRAINING_AUDIO_DIR):
    for file in files:
        [name, ext] = file.split(".")
        phnFile = os.path.join(root, file)

        if phnFile.lower().endswith(PHONEME_EXT):
            fid = open(phnFile, 'r')
            lines = fid.readlines()
            fid.close()

            for line in lines:
                if "oh" in line:
                    test = 0
