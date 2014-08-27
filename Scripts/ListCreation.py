import os
import platform

def listAllFiles(dir, ext):
    return [f for f in os.listdir(dir) if ext in f]


if platform.system() == "Windows":
    AUDIO_DIR = "J:\\ConvertData\\Thesis Data\\Desk\\Testing\\Development\\"
    OUTPUT_DIR = "J:\\ClassifierTraining\\Lists\\"
    CLASSIFIER_DIR = "J:\\ClassifierTraining\\Classifiers\\"
else:
    AUDIO_DIR = "\\Volumes\\External\\ConvertData\\Thesis Data\\Desk\\Testing\\Development\\"
    OUTPUT_DIR = "\\Volumes\\External\\ClassifierTraining\\Lists\\"
    CLASSIFIER_DIR ="\\Volumes\\External\\ClassifierTraining\\Classifiers\\"


MFC_EXT = ".mfc"
AUDIO_EXT = ".wav"
CLASSIFIER_EXTS = [".stft", ".lpc", ".mfc", ".nnmf"]

# Script File Extension
SCRIPT_EXT = ".scp"

# Master Label File Extension
MLF_EXT = ".mlf"

# Clear WAV -> MFC conversion file, to allow appending
convertFile = str.format("{0}{1}{2}", OUTPUT_DIR, "WAV_MFC_Conversion_List", SCRIPT_EXT)
open(convertFile, 'w').close()


""" Generate WAV -> MFC list """

for folder in os.listdir(AUDIO_DIR):

    dir = str.format("{0}{1}", AUDIO_DIR, folder)
    files = listAllFiles(dir, AUDIO_EXT)

    outputFile = str.format("{0}{1}{2}", OUTPUT_DIR, "WAV_MFC_Conversion_List", SCRIPT_EXT)

    fid = open(outputFile, 'a+')

    for file in files:
        [name, _] = file.split('.')

        output = str.format("{0}{1} {2}{3}{4}",
                    dir,
                    file,
                    CLASSIFIER_DIR,
                    name,
                    MFC_EXT)

        fid.write(output + "\n")

    fid.close()


""" Classifier Training Lists """

for ext in CLASSIFIER_EXTS:

    listFile = str.format("{0}{1}_Training_List.scp", OUTPUT_DIR, ext.lstrip('.'))

    files = listAllFiles(CLASSIFIER_DIR, ext)

    fid = open(listFile, 'w')

    for file in files:
        fid.write(str.format("{0}{1}\n", CLASSIFIER_DIR, file))

    fid.close()


""" Master Label File Creation """





