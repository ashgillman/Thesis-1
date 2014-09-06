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
TRAINING_AUDIO_DIR = str.format("{0}ConvertData{1}ThesisData{1}Desk{1}Testing{1}", FILE_START, SEPARATOR)
EVAL_AUDIO_DIR = str.format("{0}ConvertData{1}ThesisData{1}Desk{1}Testing{1}Evaluation{1}", FILE_START, SEPARATOR)
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
WRD_EXT = ".wrd"
CLASSIFIER_EXTS = [".stft", ".lpc", ".mfc", ".nnmf"]

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
HCOMPV_MFC_CONFIG = CONFIG_DIR + "MFC_HCompV_Config.ini"
PROTO_CONFIG = TRAINING_DIR + "Training" + SEPARATOR + "MFCProto"
HEREST_CONFIG = CONFIG_DIR + "Reestimation_Config.ini"

SIL_CONFIG = TRAINING_DIR + "Training" + SEPARATOR + "sil.hed"

# Phoneme File location
PHONE_LOC = TRAINING_DIR + "Training" + SEPARATOR + "Monophones"
PHONE_NO_SP = PHONE_LOC + '0'
PHONE_WITH_SP = PHONE_LOC + '1'
PHONE_EVAL = PHONE_LOC + 'E'

# Sleep length
SLEEP_S = 3

# Number of training iterations
TRAINING_COUNT = 15

# Dictionary Location
PHONE_DICT_LOC = TRAINING_DIR + "Training" + SEPARATOR + "CMUDict"
ONLINE_DICT_LOC = TRAINING_DIR + "Training" + SEPARATOR + "OnlineDict"
MY_DICT_LOC = TRAINING_DIR + "Training" + SEPARATOR + "MyDict"

# Word file location
WORD_LOC = TRAINING_DIR + "Training" + SEPARATOR + "WordList"
WORDNET = TRAINING_DIR + "Training" + SEPARATOR + "WordNet"

# MLF locations
MLF_TRAINING = CONFIG_DIR + "TrainingPhones.mlf"
MLF_EVAL = CONFIG_DIR + "Eval||Phones.mlf"

# Missing Words
M = ["throughout", "matter"]

def listAllFiles(dir, ext):
    return [name for name in [f for r,d,f in os.walk(dir)][0] if name.lower().endswith(ext.lower())]

def buildFileStructure():
    for ext in CLASSIFIER_EXTS:
        ext = ext.lstrip('.').upper()
        dir = str.format("{0}{1}", HMM_DIR, ext)
        if (not os.path.exists(dir)):
            os.mkdir(dir)

        for i in range(TRAINING_COUNT+1):
            subdir = str.format("{0}{1}hmm{2}", dir, SEPARATOR, i)
            if (not os.path.exists(subdir)):
                os.mkdir(subdir)

def buildWordList():
    if os.path.isfile(WORD_LOC):
        open(WORD_LOC, 'w').close()

    for root, subdirs, files in os.walk(TRAINING_AUDIO_DIR):

        wrdList = open(WORD_LOC, 'a+')

        for file in files:
            [_, ext] = file.split(".")

            if ext.lower() in WRD_EXT.lower():

                wrdFile = os.path.join(root, file)

                if os.path.isfile(wrdFile):

                    wrd = open(wrdFile, 'r')

                    for line in wrd:
                        [_, _, word] = line.strip("\n").split("\t")

                        word = word.strip('.').upper()
                        wrdList.write(word + "\n")
                        wrdList.flush()

                    wrd.close()

        wrdList.close()


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
            phnFile = os.path.join(root, file)
            labFile = str.format("{0}{1}{2}", output, name, LAB_EXT)

            if phnFile.lower().endswith(PHONEME_EXT) and not os.path.isfile(labFile):
                shutil.copyfile(phnFile, labFile)


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
def generateClassifierLists(audioDir, ext, outputFile):
    ext = ext.lstrip('.').upper()
    files = listAllFiles(audioDir, ext)

    fid = open(outputFile, 'w')

    for file in files:
        fid.write(str.format("{0}{1}\n", audioDir, file))

    fid.close()


""" Master Label File Creation """
def generateMLF(audioDir, MLFFile):

    # Overwrite the MLF file
    fid = open(MLFFile, 'w')
    fid.write("#!MLF!#\n")
    fid.close()

    for folder in os.listdir(audioDir):

        dir = str.format("{0}{1}{2}", audioDir, folder, SEPARATOR)
        files = listAllFiles(dir, PHONEME_EXT.upper())

        for file in files:

            label = str.format("\"*\{0}{1}\"", file.rstrip(PHONEME_EXT.upper()), LAB_EXT)

            phn = open(dir + file, 'r+')

            mlf = open(MLFFile, 'a+')

            mlf.write(label + "\n")

            for line in phn:
                mlf.write(line)

            mlf.write(".\n")

            phn.close()
            mlf.close()




""" Generate the HMM definitions """
def generateHMMDefs(ext):
    ext = ext.lstrip('.').upper()

    hmmDefs = str.format("{0}{1}{2}hmm0{2}HMMDef", HMM_DIR, ext, SEPARATOR)
    proto = str.format("{0}{1}{2}hmm0{2}{1}Proto", HMM_DIR, ext, SEPARATOR) # TODO: Edit proto files of each ext

    phn = open(PHONE_NO_SP, 'r')
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
        nextHMM = str.format("{0}{1}{2}hmm{3}{2}{4}", HMM_DIR, ext, SEPARATOR, HMMIteration+1, file)
        shutil.copy(currentHMM + SEPARATOR + file, nextHMM)

    hmmDef = str.format("{0}{1}{2}hmm{3}{2}HMMDef", HMM_DIR, ext, SEPARATOR, HMMIteration+1)

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
    command = str.format("HDMan -T 1 -m -w {0} -n {1} -g {2} -i -l {3} {4} {6} {5}",
                         WORD_LOC,
                         PHONE_NO_SP,
                         TRAINING_DIR + "Training" + SEPARATOR + "global.ded",
                         TRAINING_DIR + "Training" + SEPARATOR + "logFile",
                         MY_DICT_LOC,
                         PHONE_DICT_LOC,
                         ONLINE_DICT_LOC
                         )

    print(command)
    os.system(command)


def performReestimation(ext, currentIteration, includeSPModel=False, includeNewMLF=False):
    ext = ext.lstrip('.').upper()

    if includeSPModel:
        phoneFile = PHONE_WITH_SP
    else:
        phoneFile = PHONE_NO_SP

    if includeNewMLF:
        mlf = SCRIPT_DIR + ext + "NewPhones0.mlf"
    else:
        mlf = SCRIPT_DIR + "phones0.mlf"

    macros = str.format("{0}{1}{2}hmm{3}{2}{1}Macros", HMM_DIR, ext, SEPARATOR, currentIteration)
    hmmDef = str.format("{0}{1}{2}hmm{3}{2}HMMDef", HMM_DIR, ext, SEPARATOR, currentIteration)
    output = str.format("{0}{1}{2}hmm{3}", HMM_DIR, ext, SEPARATOR, currentIteration+1)

    command = str.format("HERest -C {0} -I {1} -t 250.0 150.0 1000.0 -S {2} -H {3} -H {4} -M {5} {6}",
                         HCOMPV_CONFIG.replace("||", ext),
                         mlf,
                         SCRIPT_DIR + ext + "_Training_List.scp",
                         macros,
                         hmmDef,
                         output,
                         phoneFile
                         )

    os.system(command)


def performRealignment(ext, currentIteration):
    ext = ext.lstrip('.').upper()

    macros = str.format("{0}{1}{2}hmm{3}{2}{1}Macros", HMM_DIR, ext, SEPARATOR, currentIteration)
    hmmDef = str.format("{0}{1}{2}hmm{3}{2}HMMDef", HMM_DIR, ext, SEPARATOR, currentIteration)

    command = str.format("HVite -T 1 -l '*' -o SWT -b SENT-END -C {0} -a -H {1} -H {2} -i {3} -m -t 250.0 150.0 1000.0 -y lab -a -I {4} -S {5} {6} {7} > {8}",
                         HCOMPV_CONFIG.replace("||", ext),
                         macros,
                         hmmDef,
                         SCRIPT_DIR + ext + "NewPhones0.mlf",
                         CONFIG_DIR + "Words.mlf",
                         SCRIPT_DIR + ext + "_Training_List.scp",
                         MY_DICT_LOC,
                         PHONE_WITH_SP,
                         TRAINING_DIR + "HVITE.log"
                         )

    os.system(command)


def createMyOwnFuckingDictionary():
    if os.path.isfile(MY_DICT_LOC):
        open(PHONE_DICT_LOC, 'w').close()

    for root, subdirs, files in os.walk(TRAINING_AUDIO_DIR):

        phones = []

        for file in files:
            [name, ext] = file.split(".")

            if ext.lower() in PHONEME_EXT.lower():
                phnFile = os.path.join(root, file)
                wrdFile = os.path.join(root, name + WRD_EXT.upper())

                if os.path.isfile(phnFile) and os.path.isfile(wrdFile):
                    phones = transcribeFiles(wrdFile, phnFile, phones)

def transcribeFiles(wrdFile, phnFile, existingDict=[]):
    phn = open(phnFile, 'r')
    wrd = open(wrdFile, 'r')

    dict = open(PHONE_DICT_LOC, 'a+')

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

        while(phnStart < start):
            phnLine = phn.readline().strip("\n")

            [phnStart, phnEnd, phone] = phnLine.split("\t")
            phnStart = int(phnStart)
            phnEnd = int(phnEnd)

        while(phnEnd < end):
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

command = input("(I)nitiatise, (T)rain, (E)valuate or (Q)uit: ").upper()

while (not command.startswith("Q")):
    if (command.startswith("I")):
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
        #os.system(conversionCommand)
        print("Completed")

        sleep(SLEEP_S)

        # Generate the classifier lists
        print("Generating lists for each classifier")
        for ext in CLASSIFIER_EXTS:
            ext = ext.lstrip('.').upper()
            listFile = str.format("{0}{1}_Training_List.scp", SCRIPT_DIR, ext)
            generateClassifierLists(CLASSIFIER_TRAINING_DIR, ext, listFile)
        print("Completed")

        sleep(SLEEP_S)

        # Generate MLF
        print("Generating MLF")
        generateMLF(TRAINING_AUDIO_DIR, MLF_TRAINING)
        print("Completed")

        sleep(SLEEP_S)

        # Generate first pass HMM's
        for ext in ['.mfc']:    #TODO: Update so it can do multiple classifier configs
            ext = ext.lstrip('.').upper()
            trainingFolder = "Training" + SEPARATOR

            script = str.format("{0}{1}_Training_List.scp", SCRIPT_DIR, ext)
            outputFolder = str.format("{0}{1}{2}hmm0", HMM_DIR, ext, SEPARATOR)
            hmmCommand = str.format("HCompV -T 1 -C {0} -f 0.01 -m -S {1} -M {2} {3}",
                                    HCOMPV_CONFIG.replace("||", ext),
                                    script,
                                    outputFolder,
                                    PROTO_CONFIG)
            print(str.format("Performing {0} HMM initialisation", ext))
            os.system(hmmCommand)
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
        createLabFiles(TRAINING_AUDIO_DIR)
        print("Completed")

        sleep(SLEEP_S)

        print("Creating phoneme dictionary (if one doesn't already exist)")
        if not os.path.isfile(MY_DICT_LOC):
            pass
            #createMyOwnFuckingDictionary()

        print("Completed")

    elif (command.startswith("T")):
        for ext in [".mfc"]:                # TODO: Handle all classifiers
            ext = ext.lstrip('.').upper()

            currentIteration = 0

            # Re-estimation 1-3
            for i in range(3):
                print(str.format("Performing Re-Estimation {0} for the {1} classifier", currentIteration+1, ext))

                performReestimation(ext, currentIteration)

                currentIteration += 1

                print("Completed")

                sleep(SLEEP_S)

            print("Generating the sp model and tying it to the center model of sil.")

            spModel = generateSPModel(ext, currentIteration)
            currentIteration += 1

            hmmDef = str.format("{0}{1}{2}hmm{3}{2}HMMDef", HMM_DIR, ext, SEPARATOR, currentIteration)

            fid = open(hmmDef, 'a+')
            fid.write(spModel)
            fid.close()

            print("Model generated\nTying model to sil.")

            macros = str.format("{0}{1}{2}hmm{3}{2}{1}Macros", HMM_DIR, ext, SEPARATOR, currentIteration)
            output = str.format("{0}{1}{2}hmm{3}", HMM_DIR, ext, SEPARATOR, currentIteration+1)

            command = str.format("HHEd -H {0} -H {1} -M {2} {3} {4}",
                                 hmmDef,
                                 macros,
                                 output,
                                 SIL_CONFIG,
                                 PHONE_WITH_SP)

            os.system(command)

            currentIteration += 1

            print("Completed")

            sleep(SLEEP_S)

            # Re-estimation 4-6
            for i in range(3):
                print(str.format("Performing Re-Estimation {0} for the {1} classifier", currentIteration+1, ext))

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

                print(str.format("Performing Re-Estimation {0} for the {1} classifier", currentIteration+1, ext))

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
        os.system(conversionCommand)
        print("Completed")

        sleep(SLEEP_S)

        # Generate the classifier lists
        print("Generating lists for each classifier")
        for ext in CLASSIFIER_EXTS:
            ext = ext.lstrip('.').upper()
            listFile = str.format("{0}{1}_EVAL_List.scp", SCRIPT_DIR, ext)
            generateClassifierLists(EVAL_AUDIO_DIR, ext, listFile)
        print("Completed")

        sleep(SLEEP_S)

        # Check if .phn have been converted to .lab files
        print("Checking if .phn -> .lab conversion has occurred")
        createLabFiles(EVAL_AUDIO_DIR, True)
        print("Completed")

        sleep(SLEEP_S)

        # Recognition test
        for ext in [".mfc"]:            #TODO: Fix to include all classifiers
            ext = ext.lstrip('.').upper()

            hmmDef = str.format("{0}{1}{2}hmm{3}{2}HMMDef", HMM_DIR, ext, SEPARATOR, TRAINING_COUNT)
            listFile = str.format("{0}{1}_EVAL_List.scp", SCRIPT_DIR, ext)

            MLFOutput = MLF_EVAL.replace("||", ext)

            command = str.format("HVite -C {0} -H {1} -S {2} -l '*' -i {3} -w {4} -p 0.0 -s 5.0 {5} {6}",
                                 HCOMPV_CONFIG.replace("||", ext),
                                 hmmDef,
                                 listFile,
                                 MLFOutput,
                                 WORD_LOC,
                                 PHONE_DICT_LOC,
                                 PHONE_EVAL
                                 )

            print(str.format("Performing recognition test for {0}", ext))
            #os.system(command)
            print("Completed")


        sleep(SLEEP_S)

        # Results
        for ext in CLASSIFIER_EXTS:
            ext = ext.lstrip('.').upper()

            MLFOutput = MLF_EVAL.replace("||", ext)

            command = str.format("HResults -f -p -L {0} {1} {2} > {3}{4}Output.txt",
                                 CLASSIFIER_EVAL_DIR,
                                 PHONE_WITH_SP,
                                 MLFOutput,
                                 RESULTS_DIR,
                                 ext)

            print(str.format("Outputing results for {0}", ext))
            #os.system(command)
            print("Completed")

    elif (command.startswith("N")):
        #createMyOwnFuckingDictionary()
        #sortFile(PHONE_DICT_LOC)
        #buildWordList()

        buildDictionary()
        #sortFile(MY_DICT_LOC)
        #performRealignment("MFC", 9)
    else:
        print("Invalid option.")


    command = input("(I)nitiatise, (T)rain, (E)valuate or (Q)uit: ").upper()
