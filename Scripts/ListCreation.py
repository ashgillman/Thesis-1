import os
import platform
import shutil

""" Define System Directory Constants """
if platform.system() == "Windows":
    FILE_START = "J:\\"
else:
    FILE_START = "\\Volumes\\External\\"

# Directory Constants
TRAINING_AUDIO_DIR = FILE_START + "ConvertData\\Thesis Data\\Desk\\Testing\\Development\\"
OUTPUT_DIR = FILE_START + "ClassifierTraining\\Lists\\"
CLASSIFIER_DIR = FILE_START + "ClassifierTraining\\Classifiers\\"
DATA_DIR = FILE_START + "ConvertData\\"

# Extension Constants
MFC_EXT = ".mfc"
AUDIO_EXT = ".wav"
PHONEME_EXT = ".phn"
LAB_EXT = ".lab"
CLASSIFIER_EXTS = [".stft", ".lpc", ".mfc", ".nnmf"]

# Script File Extension
SCRIPT_EXT = ".scp"

# Master Label File Extension
MLF_EXT = ".mlf"

# Phoneme Constants
SILENCE_PHN = "sil"

def listAllFiles(dir, ext):
    return [name for name in [f for r,d,f in os.walk(dir)][0] if ext in name]

def createLabFiles():
    """
    Recursively traverses the entire audio data directory looking for .phn files and copies them into a .lab file if it
    doesn't already exist.
    """
    for root, subdirs, files in os.walk(DATA_DIR):
        for file in files:
            [name, ext] = file.split(".")
            phnFile = os.path.join(root, file)
            labFile = phnFile[0:-4] + LAB_EXT

            if phnFile.lower().endswith(PHONEME_EXT) and not os.path.isfile(labFile):
                shutil.copyfile(phnFile, labFile)


""" Generate WAV -> MFC list """

def generateConversionList():
    # Clear WAV -> MFC conversion file, to allow appending
    wavConvertFile = str.format("{0}{1}{2}", OUTPUT_DIR, "WAV_MFC_Conversion_List", SCRIPT_EXT)
    open(wavConvertFile, 'w').close()

    for folder in os.listdir(TRAINING_AUDIO_DIR):

        dir = str.format("{0}{1}\\", TRAINING_AUDIO_DIR, folder)
        files = listAllFiles(dir, AUDIO_EXT)

        fid = open(wavConvertFile, 'a+')

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
def generateClassifierLists():
    for ext in CLASSIFIER_EXTS:

        listFile = str.format("{0}{1}_Training_List.scp", OUTPUT_DIR, ext.lstrip('.'))

        files = listAllFiles(CLASSIFIER_DIR, ext)

        fid = open(listFile, 'w')

        for file in files:
            fid.write(str.format("{0}{1}\n", CLASSIFIER_DIR, file))

        fid.close()


""" Master Label File Creation """
def generateMLF():
    MLFFile = str.format("{0}{1}{2}", OUTPUT_DIR, "phones0", MLF_EXT)

    # Overwrite the MLF file
    fid = open(MLFFile, 'w')
    fid.write("#!MLF!#\n")
    fid.close()

    for folder in os.listdir(TRAINING_AUDIO_DIR):

        dir = str.format("{0}{1}\\", TRAINING_AUDIO_DIR, folder)
        files = listAllFiles(dir, PHONEME_EXT.upper())

        for file in files:

            label = str.format("\"*/{0}\"", file)

            phn = open(dir + file, 'r+')

            mlf = open(MLFFile, 'a+')

            mlf.write(label + "\n")

            for line in phn:
                mlf.write(line)

            mlf.write(".\n")

            phn.close()
            mlf.close()

def generateHMMDefs():
    phonemeList = str.format("{0}{1}{2}", OUTPUT_DIR, "phones0", MLF_EXT) #TODO: Set proper PhonemeList location
    hmmDefs = str.format("{0}{1}{2}", OUTPUT_DIR, "phones0", MLF_EXT) #TODO: Set proper HMMDef location
    proto = str.format("{0}{1}{2}", OUTPUT_DIR, "phones0", MLF_EXT) #TODO: Set proper proto location

    phn = open(phonemeList, 'r')
    hmm = open(hmmDefs, 'w')

    for line in phn:
        hmm.write(str.format("~h {0}", line))

        if line.lower() == SILENCE_PHN:
            hmm.write("\n")

        protoFile = open(proto, 'r')
        lineCount = 0

        for protoLine in protoFile:

            if lineCount > 3:
                hmm.write(protoLine)

            lineCount += 1

        hmm.write("\n")

        proto.close()

    phn.close()
    hmm.close()

def generateMacros():
    macros = str.format("{0}{1}{2}", OUTPUT_DIR, "phones0", MLF_EXT) #TODO: Set proper Macros location
    macroHeaders = str.format("{0}{1}{2}", OUTPUT_DIR, "phones0", MLF_EXT) #TODO: Set proper MacroHeaders location
    vFloor = str.format("{0}{1}{2}", OUTPUT_DIR, "phones0", MLF_EXT) #TODO: Set proper vFloor location

    macroFile = open(macros, 'w')
    headerFile = open(macroHeaders, 'r')

    for line in headerFile:
        macroFile.write(line)

    macroFile.write("\n")

    headerFile.close()

    vFloorFile = open(vFloor, 'w')

    for line in vFloorFile:
        macroFile.write(line)

    vFloorFile.close()

    macroFile.close()
