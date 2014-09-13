import os
import platform
import shutil

from time import sleep

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
EVAL_AUDIO_DIR = str.format("{0}Evaluation{1}", AUDIO_DIR, SEPARATOR)

SCRIPT_DIR = str.format("{0}Lists{1}", TRAINING_DIR, SEPARATOR)

CLASSIFIER_DIR = str.format("{0}Classifiers{1}", TRAINING_DIR, SEPARATOR)
CLASSIFIER_TRAINING_DIR = str.format("{0}Training{1}", CLASSIFIER_DIR, SEPARATOR)
CLASSIFIER_EVAL_DIR = str.format("{0}Eval{1}", CLASSIFIER_DIR, SEPARATOR)

DATA_DIR = str.format("{0}ConvertData{1}", FILE_START, SEPARATOR)

CONFIG_DIR = str.format("{0}Configs{1}", TRAINING_DIR, SEPARATOR)

HMM_DIR = str.format("{0}HMMs{1}", TRAINING_DIR, SEPARATOR)

RESULTS_DIR = str.format("{0}Results{1}", TRAINING_DIR, SEPARATOR)

# Extension Constants
MFC_EXT = ".mfc"
AUDIO_EXT = ".wav"
PHONEME_EXT = ".phn"
LAB_EXT = ".lab"
WORD_EXT = ".wrd"
CLASSIFIER_EXTS = [".mfc"]  # [".stft", ".lpc", ".mfc", ".nnmf"] #TODO: Replace

# Script File Extension
SCRIPT_EXT = ".scp"

# Master Label File Extension
MLF_EXT = ".mlf"

# Phoneme Constants
SILENCE_PHN = "sil"

# Config File Locations
# TODO: Actually write configs
MFC_CONVERT_CONFIG = CONFIG_DIR + "MFC_Convert_Config.ini"
HCOMPV_CONFIG = CONFIG_DIR + "||_HCompV_Config.ini"
PROTO_CONFIG = TRAINING_DIR + "Training" + SEPARATOR + "MFCProto"
HEREST_CONFIG = CONFIG_DIR + "Reestimation_Config.ini"

SIL_CONFIG = TRAINING_DIR + "Training" + SEPARATOR + "sil.hed"

# Phoneme File location
PHONE_LOC = TRAINING_DIR + "Training" + SEPARATOR + "Monophones"
PHONE_NO_SP = PHONE_LOC + '0'
PHONE_WITH_SP = PHONE_LOC + '1'
PHONE_EVAL = PHONE_LOC + 'E'

# Sleep length
SLEEP_S = 1

# Number of training iterations
TRAINING_COUNT = 12

# Dictionary Location
DICT_PHONE_LOC = TRAINING_DIR + "Training" + SEPARATOR + "PhoneDict"
DICT_ONLINE_LOC = TRAINING_DIR + "Training" + SEPARATOR + "OnlineDict"
DICT_BUILT_LOC = TRAINING_DIR + "Training" + SEPARATOR + "MyDict"
DICT_BEEP_LOC = TRAINING_DIR + "Training" + SEPARATOR + "BeepDict"
DICT_CMU_LOC = TRAINING_DIR + "Training" + SEPARATOR + "CMUDict"

# Word file location.
WORDLIST_LOC = TRAINING_DIR + "Training" + SEPARATOR + "WordList"
SORTED_WORDLIST_LOC = TRAINING_DIR + "Training" + SEPARATOR + "SortedWordList"

PHONELIST_LOC = TRAINING_DIR + "Training" + SEPARATOR + "PhoneList"
SORTED_PHONELIST_LOC = TRAINING_DIR + "Training" + SEPARATOR + "SortedPhoneList"

GRAMMAR = TRAINING_DIR + "Training" + SEPARATOR + "GrammarFile"
WORDNET_LOC = TRAINING_DIR + "Training" + SEPARATOR + "WordNet"

# MLF locations
MLF_PHONES_NO_SP = CONFIG_DIR + "Phones0.mlf"
MLF_PHONES_WITH_SP = CONFIG_DIR + "Phones1.mlf"
MLF_REALIGNED = CONFIG_DIR + "Realigned||Phones.mlf"

MLF_TRAINING = CONFIG_DIR + "TrainingPhones.mlf"
MLF_TRAINING_WORD = CONFIG_DIR + "Words.mlf"
MLF_TRAINING_PHONE = CONFIG_DIR + "Phones.mlf"

MLF_EVAL = CONFIG_DIR + "Eval||Phones.mlf"
MLF_EVAL_WORD = CONFIG_DIR + "EvalWords.mlf"
MLF_EVAL_PHONE = CONFIG_DIR + "EvalPhones.mlf"

# HLEd Scripts
HLED_TRANSCRIBE = TRAINING_DIR + "Training" + SEPARATOR + "mkphones0.led"
HLED_ADD_SP = TRAINING_DIR + "Training" + SEPARATOR + "mkphones1.led"

# Missing Words
M = ["throughout", "matter"]


def listAllFiles(dir, ext):
    return [name for name in [f for r, d, f in os.walk(dir)][0] if name.lower().endswith(ext.lower())]


def buildFileStructure():
    for ext in CLASSIFIER_EXTS:
        ext = ext.lstrip('.').upper()
        dir = str.format("{0}{1}", HMM_DIR, ext)
        if (not os.path.exists(dir)):
            os.mkdir(dir)

        for i in range(TRAINING_COUNT + 1):
            subdir = str.format("{0}{1}hmm{2}", dir, SEPARATOR, i)
            if (not os.path.exists(subdir)):
                os.mkdir(subdir)


def buildPhoneList():
    """ Builds Phoneme list """
    if os.path.isfile(PHONELIST_LOC):
        open(PHONELIST_LOC, 'w').close()

    for root, subdirs, files in os.walk(TRAINING_AUDIO_DIR):

        phnList = open(PHONELIST_LOC, 'a+')

        for file in files:
            [_, ext] = file.split(".")

            if ext.lower() in PHONEME_EXT.lower():

                phnFile = os.path.join(root, file)

                if os.path.isfile(phnFile):

                    wrd = open(phnFile, 'r')

                    for line in wrd:
                        [_, _, word] = line.strip("\n").split("\t")

                        word = word.strip('.').upper()
                        phnList.write(word + "\n")
                        phnList.flush()

                    wrd.close()

        phnList.close()


def buildPhoneDictionary():
    """ Builds the dummy phoneme dictionary from the sorted phoneme list """
    if os.path.isfile(DICT_PHONE_LOC):
        open(DICT_PHONE_LOC, 'w').close()

    phnDict = open(DICT_PHONE_LOC, 'a+')
    phnList = open(SORTED_PHONELIST_LOC, 'r')

    for line in phnList:
        line = line.strip("\n")
        phnDict.write(str.format("{0} {0}\n", line))

    phnDict.close()
    phnList.close()

    fid = open(DICT_PHONE_LOC, 'a+')
    fid.write("SENT-END SIL\n")
    fid.write("SENT-START SIL\n")
    fid.close()

    sortFile(DICT_PHONE_LOC)


def createLabFiles(audioDir, eval=False):
    """
    Recursively traverses the entire audio data directory looking for .phn files and copies them into a .lab file if it
    doesn't already exist.
    """
    output = CLASSIFIER_TRAINING_DIR
    if eval:
        output = CLASSIFIER_EVAL_DIR

    for root, subdirs, files in os.walk(audioDir):
        for file in files:
            [name, ext] = file.split(".")
            wrdFile = os.path.join(root, file)
            labFile = str.format("{0}{1}{2}", output, name, LAB_EXT)

            if wrdFile.lower().endswith(PHONEME_EXT) and not os.path.isfile(labFile):
                shutil.copyfile(wrdFile, labFile)


""" Generate WAV -> MFC list """


def generateConversionList(audioDir, outputFile, eval=False):
    # Clear WAV -> MFC conversion file, to allow appending
    open(outputFile, 'w').close()

    for folder in os.listdir(audioDir):

        dir = str.format("{0}{1}{2}", audioDir, folder, SEPARATOR)
        files = listAllFiles(dir, AUDIO_EXT)

        fid = open(wavConvertFile, 'a+')

        for file in files:
            [name, _] = file.split('.')
            output = CLASSIFIER_TRAINING_DIR
            if eval:
                output = CLASSIFIER_EVAL_DIR

            output = str.format("{0}{1} {2}{3}{4}",
                                dir,
                                file,
                                output,
                                name,
                                MFC_EXT)

            fid.write(output + "\n")

        fid.close()


""" Classifier Training Lists """


def generateClassifierLists(audioDir, ext, eval=False):
    ext = ext.lstrip('.').upper()
    files = listAllFiles(audioDir, ext)
    if eval:
        outputFile = str.format("{0}{1}_EVAL_List.scp", SCRIPT_DIR, ext)
    else:
        outputFile = str.format("{0}{1}_Training_List.scp", SCRIPT_DIR, ext)

    fid = open(outputFile, 'w')

    for file in files:
        fid.write(str.format("{0}{1}\n", audioDir, file))

    fid.close()


""" Master Label File Creation """


def generateMLF(outputFile, HLEDscript, eval=False):
    if eval:
        mlf = MLF_EVAL_WORD
    else:
        mlf = MLF_TRAINING_WORD

    command = str.format("HLEd -T 1 -l * -d {0} -i {1} {2} {3}",
                         DICT_BEEP_LOC,
                         outputFile,
                         HLEDscript,
                         mlf)

    os.system(command)


def generateWordMLF(eval=False):
    # Overwrite the MLF file
    ext = WORD_EXT.upper()

    if eval:
        audioDir = EVAL_AUDIO_DIR
        MLFFile = MLF_EVAL_WORD
    else:
        audioDir = TRAINING_AUDIO_DIR
        MLFFile = MLF_TRAINING_WORD

    fid = open(MLFFile, 'w')
    fid.write("#!MLF!#\n")
    fid.close()

    for folder in os.listdir(audioDir):

        dir = str.format("{0}{1}{2}", audioDir, folder, SEPARATOR)
        files = listAllFiles(dir, ext)

        for file in files:
            [name, _] = file.split('.')
            label = str.format("\"*/{0}{1}\"", name, LAB_EXT)

            wrd = open(dir + file, 'r+')

            mlf = open(MLFFile, 'a+')

            mlf.write(label + "\n")

            for line in wrd:
                mlf.write(line.upper())

            mlf.write(".\n")

            wrd.close()
            mlf.close()


def generatePhonemeMLF(eval=False):
    # Overwrite the MLF file
    ext = PHONEME_EXT.upper()

    if eval:
        audioDir = EVAL_AUDIO_DIR
        MLFFile = MLF_EVAL_PHONE
    else:
        audioDir = TRAINING_AUDIO_DIR
        MLFFile = MLF_TRAINING_PHONE

    fid = open(MLFFile, 'w')
    fid.write("#!MLF!#\n")
    fid.close()

    for folder in os.listdir(audioDir):

        dir = str.format("{0}{1}{2}", audioDir, folder, SEPARATOR)
        files = listAllFiles(dir, ext)

        for file in files:
            [name, _] = file.split('.')
            label = str.format("\"*/{0}{1}\"", name, LAB_EXT)

            phn = open(dir + file, 'r+')

            mlf = open(MLFFile, 'a+')

            mlf.write(label + "\n")

            for line in phn:
                mlf.write(line.upper())

            mlf.write(".\n")

            phn.close()
            mlf.close()


""" Generate the HMM definitions """


def generateHMMDefs(ext):
    ext = ext.lstrip('.').upper()

    hmmDefs = str.format("{0}{1}{2}hmm0{2}HMMDef", HMM_DIR, ext, SEPARATOR)
    proto = str.format("{0}{1}{2}hmm0{2}{1}Proto", HMM_DIR, ext, SEPARATOR)  # TODO: Edit proto files of each ext

    phn = open(SORTED_PHONELIST_LOC, 'r')
    hmm = open(hmmDefs, 'w')

    for line in phn:
        hmm.write(str.format("~h \"{0}\"\n", line.strip("\n")))

        if line.lower() == SILENCE_PHN:
            hmm.write("\n")

        protoFile = open(proto, 'r')
        lineCount = 0

        for protoLine in protoFile:

            if lineCount > 3:
                hmm.write(protoLine)

            lineCount += 1

        hmm.write("\n")

        protoFile.close()

    phn.close()
    hmm.close()


""" Generate the macro files """


def generateMacros(ext):
    ext = ext.lstrip('.').upper()

    macros = str.format("{0}{1}{2}hmm0{2}{1}Macros", HMM_DIR, ext, SEPARATOR)
    proto = str.format("{0}{1}{2}hmm0{2}{1}Proto", HMM_DIR, ext, SEPARATOR)
    vFloor = str.format("{0}{1}{2}hmm0{2}vFloors", HMM_DIR, ext, SEPARATOR)

    macroFile = open(macros, 'w')
    headerFile = open(proto, 'r')

    lineCount = 0
    for line in headerFile:
        macroFile.write(line)
        lineCount += 1
        if lineCount >= 3:
            break

    headerFile.close()

    vFloorFile = open(vFloor, 'r')

    for line in vFloorFile:
        macroFile.write(line)

    vFloorFile.close()

    macroFile.close()


def generateSPModel(ext, HMMIteration):
    ext = ext.lstrip('.').upper()

    currentHMM = str.format("{0}{1}{2}hmm{3}", HMM_DIR, ext, SEPARATOR, HMMIteration)

    for file in os.listdir(currentHMM):
        nextHMM = str.format("{0}{1}{2}hmm{3}{2}{4}", HMM_DIR, ext, SEPARATOR, HMMIteration + 1, file)
        shutil.copy(currentHMM + SEPARATOR + file, nextHMM)

    hmmDef = str.format("{0}{1}{2}hmm{3}{2}HMMDef", HMM_DIR, ext, SEPARATOR, HMMIteration + 1)

    fid = open(hmmDef, 'r')

    spModel = "~h \"sp\"\n"
    silFound = False
    secondState = False

    for line in fid:

        if line.startswith("~h"):
            if "sil" in line:
                silFound = True
            else:
                silFound = False

        else:
            if silFound:
                if "<NUMSTATES>" in line:
                    spModel += "<BEGINHMM>\n"
                    spModel += "<NUMSTATES> 3\n"

                elif "<STATE>" in line:
                    if '3' in line:
                        line = "<STATE> 2\n"
                        secondState = True
                    else:
                        secondState = False
                elif "<TRANSP>" in line:
                    spModel += "<TRANSP> 3\n0.0 1.0 0.0\n0.0 0.9 0.1\n0.0 0.0 0.0\n"

                if secondState:
                    spModel += line

    spModel += "<ENDHMM>"

    fid.close()

    return spModel


def buildDictionary():
    command = str.format("HDMan -T 1 -m -w {0} -n {1} -g {2} -i -l {3} {4} {5} {6} {7}",
                         SORTED_WORDLIST_LOC,
                         PHONE_WITH_SP,
                         TRAINING_DIR + "Training" + SEPARATOR + "global.ded",
                         TRAINING_DIR + "Training" + SEPARATOR + "HDManLogFile",
                         DICT_BUILT_LOC,
                         DICT_BEEP_LOC,
                         DICT_ONLINE_LOC,
                         DICT_CMU_LOC
    )

    print(command)
    os.system(command)

    fid = open(DICT_BUILT_LOC, 'a+')
    fid.write("SENT-END".ljust(16))
    fid.write("[]".ljust(16))
    fid.write("sil\n")
    fid.write("SENT-START".ljust(16))
    fid.write("[]".ljust(16))
    fid.write("sil\n")
    fid.write("sil".ljust(16))
    fid.write("[]".ljust(16))
    fid.write("sil\n")
    fid.close()

    sortFile(DICT_BUILT_LOC)


def generateMonophoneWithoutSP():
    withSP = open(PHONE_WITH_SP, 'r')
    withoutSP = open(PHONE_NO_SP, 'w')

    for line in withSP:

        if "sp" in line:
            continue

        withoutSP.write(line)

    withSP.close()
    withoutSP.close()


def performReestimation(ext, currentIteration, includeSPModel=False, includeNewMLF=False):
    ext = ext.lstrip('.').upper()

    if includeSPModel:
        phoneFile = PHONE_WITH_SP
    else:
        phoneFile = PHONE_NO_SP

    if includeNewMLF:
        mlf = MLF_REALIGNED.replace("||", ext)
    else:
        mlf = MLF_TRAINING_PHONE

    macros = str.format("{0}{1}{2}hmm{3}{2}{1}Macros", HMM_DIR, ext, SEPARATOR, currentIteration)
    hmmDef = str.format("{0}{1}{2}hmm{3}{2}HMMDef", HMM_DIR, ext, SEPARATOR, currentIteration)
    output = str.format("{0}{1}{2}hmm{3}", HMM_DIR, ext, SEPARATOR, currentIteration + 1)

    command = str.format("HERest -C {0} -I {1} -t 250.0 150.0 1000.0 -S {2} -H {3} -H {4} -M {5} {6}",
                         HCOMPV_CONFIG.replace("||", ext),
                         mlf,
                         SCRIPT_DIR + ext + "_Training_List.scp",
                         macros,
                         hmmDef,
                         output,
                         SORTED_PHONELIST_LOC
    )

    os.system(command)


def performRealignment(ext, currentIteration):
    ext = ext.lstrip('.').upper()

    macros = str.format("{0}{1}{2}hmm{3}{2}{1}Macros", HMM_DIR, ext, SEPARATOR, currentIteration)
    hmmDef = str.format("{0}{1}{2}hmm{3}{2}HMMDef", HMM_DIR, ext, SEPARATOR, currentIteration)

    command = str.format(
        "HVite -T 1 -l * -o SWT -b SIL -C {0} -a -H {1} -H {2} -i {3} -m -t 250.0 150.0 1000.0 -y lab -a -I {4} -S {5} {6} {7} > {8}",
        HCOMPV_CONFIG.replace("||", ext),
        macros,
        hmmDef,
        MLF_REALIGNED.replace("||", ext),
        MLF_TRAINING_PHONE,
        SCRIPT_DIR + ext + "_Training_List.scp",
        DICT_PHONE_LOC,
        SORTED_PHONELIST_LOC,
        TRAINING_DIR + "HVITE.log"
    )

    os.system(command)


def createMyOwnFuckingDictionary():
    if os.path.isfile(DICT_BUILT_LOC):
        open(DICT_PHONE_LOC, 'w').close()

    for root, subdirs, files in os.walk(TRAINING_AUDIO_DIR):

        phones = []

        for file in files:
            [name, ext] = file.split(".")

            if ext.lower() in PHONEME_EXT.lower():
                phnFile = os.path.join(root, file)
                wrdFile = os.path.join(root, name + WORD_EXT.upper())

                if os.path.isfile(phnFile) and os.path.isfile(wrdFile):
                    phones = transcribeFiles(wrdFile, phnFile, phones)


def transcribeFiles(wrdFile, phnFile, existingDict=[]):
    phn = open(phnFile, 'r')
    wrd = open(wrdFile, 'r')

    dict = open(DICT_PHONE_LOC, 'a+')

    for line in wrd:
        [start, end, word] = line.strip("\n").split("\t")

        start = int(start)
        end = int(end)
        word = word.strip('.').upper()

        if word in existingDict:
            [_, phnEnd, _] = phn.readline().strip("\n").split("\t")
            while (int(phnEnd) < end):
                [_, phnEnd, _] = phn.readline().strip("\n").split("\t")
            continue

        dict.write(word.ljust(20))
        existingDict.append(word)

        [phnStart, phnEnd, phone] = phn.readline().strip("\n").split("\t")

        phnStart = int(phnStart)
        phnEnd = int(phnEnd)

        while (phnStart < start):
            phnLine = phn.readline().strip("\n")

            [phnStart, phnEnd, phone] = phnLine.split("\t")
            phnStart = int(phnStart)
            phnEnd = int(phnEnd)

        while (phnEnd < end):
            dict.write(phone + " ")
            phnLine = phn.readline().strip("\n")
            [_, phnEnd, phone] = phnLine.split("\t")
            phnEnd = int(phnEnd)

        dict.write(phone + "\n")

    phn.close()
    wrd.close()
    dict.close()

    return existingDict


def sortFile(filename):
    f = open(filename, "r")
    # omit empty lines and lines containing only whitespace
    lines = [line for line in f if line.strip()]
    f.close()

    lines.sort()

    f = open(filename, 'w')
    f.writelines(lines)
    f.close()


def buildGrammarFile():
    wordlist = open(SORTED_PHONELIST_LOC, 'r');
    output = "$phoneme = "

    for line in wordlist:
        line = line.strip("\n")
        output += line + " | "

    output = output[:-3] + ";"

    output += "\n"
    output += "( SIL ( <$phoneme> ) SIL )"

    wordlist.close()

    grammar = open(GRAMMAR, 'w')
    grammar.write(output)
    grammar.close()


def createWordNet():
    command = str.format("HParse {0} {1}",
                         GRAMMAR,
                         WORDNET_LOC)

    os.system(command)


def stripFullStops():
    for root, subdirs, files in os.walk(AUDIO_DIR):

        for file in files:
            [_, ext] = file.split(".")

            if ext.lower() in WORD_EXT.lower():

                wrdFile = os.path.join(root, file)

                if os.path.isfile(wrdFile):

                    wrd = open(wrdFile, 'r')
                    lines = []
                    for line in wrd:
                        word = line.strip("\n").rstrip('.')
                        word = word + "\n"

                        lines.append(word)

                    wrd.close()

                    wrd = open(wrdFile, 'w')
                    wrd.writelines(lines)
                    wrd.close()


def generateFirstPassHMM(ext):
    ext = ext.lstrip('.').upper()

    script = str.format("{0}{1}_Training_List.scp", SCRIPT_DIR, ext)
    outputFolder = str.format("{0}{1}{2}hmm0", HMM_DIR, ext, SEPARATOR)
    hmmCommand = str.format("HCompV -T 1 -C {0} -f 0.01 -m -S {1} -M {2} {3}",
                            HCOMPV_CONFIG.replace("||", ext),
                            script,
                            outputFolder,
                            PROTO_CONFIG)

    os.system(hmmCommand)

def fixFirstPassHMM(ext):
    outputFolder = str.format("{0}{1}{2}hmm0{2}HMMDef", HMM_DIR, ext, SEPARATOR)

    fid = open(outputFolder, 'r')
    lines = fid.readlines()
    fid.close()

    fid = open(outputFolder, 'w')
    for line in lines:
        fid.write(line.upper())
    fid.close()

command = input("(I)nitiatise, (T)rain, (E)valuate or (Q)uit: ").upper()

while (not command.startswith("Q")):
    if (command.startswith("I")):

        buildFileStructure()

        # Create WordList
        print("Generating phoneme list")
        buildPhoneList()
        print("Completed")

        sleep(SLEEP_S)

        if platform.system() != "Windows":
            print("Sorting and retrieving unique words from word list")
            command = str.format("cat {0} | sort | uniq > {1}",
                                 PHONELIST_LOC,
                                 SORTED_PHONELIST_LOC)
            os.system(command)
            print("Completed")
        else:
            print("You are running Windows")
            print("You need to manually sort and extract the unique phonemes from the phoneme list")
            print("The program will pause operation until you complete the task and press Enter")
            input()
            print("Completed")

        sleep(SLEEP_S)

        # Create grammar file
        print("Creating grammar file")
        buildGrammarFile()
        print("Completed")

        sleep(SLEEP_S)

        # Create word net
        print("Creating WordNet")
        createWordNet()
        print("Completed")

        sleep(SLEEP_S)

        # Build Dictionary
        print("Building dictionary")
        buildPhoneDictionary()
        print("Completed")

        sleep(SLEEP_S)

        # Generate MLFs
        print("Generating phoneme MLF")
        generatePhonemeMLF()
        print("Completed")

        sleep(SLEEP_S)

        # Generate the wav -> MFC script
        print("Generating the wav -> MFC conversion script")
        wavConvertFile = str.format("{0}{1}{2}", SCRIPT_DIR, "WAV_MFC_Conversion_List", SCRIPT_EXT)
        generateConversionList(TRAINING_AUDIO_DIR, wavConvertFile)
        print("Completed")

        sleep(SLEEP_S)

        # Perform the wav -> MFC conversion
        convertFile = str.format("{0}{1}{2}", SCRIPT_DIR, "WAV_MFC_Conversion_List", SCRIPT_EXT)
        conversionCommand = str.format("HCopy -T 1 -C {0} -S {1}", MFC_CONVERT_CONFIG, convertFile)
        print("Performing wav -> MFC conversion")
        # os.system(conversionCommand)
        print("Completed")

        sleep(SLEEP_S)

        # Generate the classifier lists
        print("Generating lists for each classifier")
        for ext in CLASSIFIER_EXTS:
            ext = ext.lstrip('.').upper()
            generateClassifierLists(CLASSIFIER_TRAINING_DIR, ext)
        print("Completed")

        sleep(SLEEP_S)

        # Generate first pass HMM's
        for ext in CLASSIFIER_EXTS:  #TODO: Update so it can do multiple classifier configs
            ext = ext.lstrip('.').upper()

            print(str.format("Performing {0} HMM initialisation", ext))
            generateFirstPassHMM(ext)
            print("Completed")

            sleep(SLEEP_S)

            # Generate hmmdef and macro files
            print("Generating HMM Definitions")
            generateHMMDefs(ext)
            print("Completed")

            print("Generating Macros")
            generateMacros(ext)
            print("Completed")

            sleep(SLEEP_S)

        # Check if .phn have been converted to .lab files
        print("Checking if .phn -> .lab conversion has occurred")
        #createLabFiles(TRAINING_AUDIO_DIR)
        print("Completed")

        sleep(SLEEP_S)

    elif (command.startswith("T")):
        for ext in CLASSIFIER_EXTS:  # TODO: Handle all classifiers
            ext = ext.lstrip('.').upper()

            currentIteration = 0

            # Re-estimation 1-3
            for i in range(3):
                print(str.format("Performing Re-Estimation {0} for the {1} classifier", currentIteration + 1, ext))

                performReestimation(ext, currentIteration)

                currentIteration += 1

                print("Completed")

                sleep(SLEEP_S)

            # Re-estimation 4-6
            for i in range(3):
                print(str.format("Performing Re-Estimation {0} for the {1} classifier", currentIteration + 1, ext))

                performReestimation(ext, currentIteration, True)

                currentIteration += 1

                print("Completed")

                sleep(SLEEP_S)


            # Realign phonetic data with dictionary
            print("Realigning the training data")
            performRealignment(ext, currentIteration)
            print("Completed")

            sleep(SLEEP_S)

            # Re-estimation 7-9
            for i in range(TRAINING_COUNT - currentIteration):
                print(str.format("Performing Re-Estimation {0} for the {1} classifier", currentIteration + 1, ext))

                performReestimation(ext, currentIteration, True, True)

                currentIteration += 1

                print("Completed")

                sleep(SLEEP_S)

    elif (command.startswith("E")):
        # Generate the training wav -> MFC script
        print("Generating the wav -> MFC conversion script")
        wavConvertFile = str.format("{0}{1}{2}", SCRIPT_DIR, "WAV_MFC_EVAL_Conversion_List", SCRIPT_EXT)
        generateConversionList(EVAL_AUDIO_DIR, wavConvertFile, True)
        print("Completed")

        sleep(SLEEP_S)

        # Perform the wav -> MFC conversion
        convertFile = str.format("{0}{1}{2}", SCRIPT_DIR, "WAV_MFC_EVAL_Conversion_List", SCRIPT_EXT)
        conversionCommand = str.format("HCopy -T 1 -C {0} -S {1}", MFC_CONVERT_CONFIG, convertFile)
        print("Performing wav -> MFC conversion")
        # os.system(conversionCommand)
        print("Completed")

        sleep(SLEEP_S)

        # Generate the classifier lists
        print("Generating lists for each classifier")
        for ext in CLASSIFIER_EXTS:
            ext = ext.lstrip('.').upper()
            generateClassifierLists(CLASSIFIER_EVAL_DIR, ext, True)
        print("Completed")

        sleep(SLEEP_S)

        # Check if .phn have been converted to .lab files
        print("Generating correct phone transcriptions")
        #generatePhonemeMLF(True)
        print("Completed")

        sleep(SLEEP_S)

        # Recognition test
        for ext in CLASSIFIER_EXTS:  #TODO: Fix to include all classifiers
            ext = ext.lstrip('.').upper()

            hmmDef = str.format("{0}{1}{2}hmm{3}{2}HMMDef", HMM_DIR, ext, SEPARATOR, TRAINING_COUNT)
            listFile = str.format("{0}{1}_EVAL_List.scp", SCRIPT_DIR, ext)

            command = str.format("HVite -b SIL -C {0} -H {1} -S {2} -i {3} -w {4} -p 0.0 -s 3.0 {5} {6}",
                                 HCOMPV_CONFIG.replace("||", ext),
                                 hmmDef,
                                 listFile,
                                 MLF_EVAL.replace("||", ext),
                                 WORDNET_LOC,
                                 DICT_PHONE_LOC,
                                 SORTED_PHONELIST_LOC
            )

            print(str.format("Performing recognition test for {0}", ext))
            os.system(command)
            print("Completed")

        sleep(SLEEP_S)

        # Results
        for ext in CLASSIFIER_EXTS:
            ext = ext.lstrip('.').upper()

            MLFOutput = MLF_EVAL.replace("||", ext)

            command = str.format("HResults -d 5 -f -p -I {0} {1} {2} > {3}{4}Output.txt",
                                 MLF_EVAL_PHONE,
                                 SORTED_PHONELIST_LOC,
                                 MLFOutput,
                                 RESULTS_DIR,
                                 ext
            )

            print(str.format("Outputing results for {0}", ext))
            os.system(command)
            print("Completed")

    elif (command.startswith("N")):
        performRealignment("MFC", 6)
    else:
        print("Invalid option.")

    command = input("(I)nitiatise, (T)rain, (E)valuate or (Q)uit: ").upper()
