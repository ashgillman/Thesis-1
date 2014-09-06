import platform
import os

__author__ = 'Bdesktop'

""" Define System Directory Constants """
if platform.system() == "Windows":
    FILE_START = "F:\\Thesis\\External\\"
    SEPARATOR = "\\"
else:
    FILE_START = "/Volumes/External/"
    SEPARATOR = "/"

TRAINING_DIR = str.format("{0}ClassifierTraining{1}Training{1}", FILE_START, SEPARATOR)

WORDLIST = TRAINING_DIR + "WordList"
GRAMMAR = TRAINING_DIR + "GrammarFile"
WORDNET = TRAINING_DIR + "WordNet"

MY_DICT_LOC = TRAINING_DIR + "MyDict"

PHONE_CREATION_SCRIPT = TRAINING_DIR + "mkphones0.led"

PHONE_OUTPUT = str.format("{0}ClassifierTraining{1}Configs{1}Phones.mlf", FILE_START, SEPARATOR)

WORDS_MLF = str.format("{0}ClassifierTraining{1}Configs{1}Words.mlf", FILE_START, SEPARATOR)


def buildGrammarFile():
    wordlist = open(WORDLIST, 'r');
    output = "$word = "

    for line in wordlist:
        line = line.strip("\n")
        output += line + " | "

    output.strip(" | ")

    output += "\n"
    output += "( SENT-START ( <$word> ) SENT-END )"

    wordlist.close()

    grammar = open(GRAMMAR, 'w')
    grammar.write(output)
    grammar.close()

def createWordNet():
    command = str.format("HParse {0} {1}",
                         GRAMMAR,
                         WORDNET)

    os.system(command)

def createPhoneTranscript():

    command = str.format("HLEd -T 1 -d {0} -i {1} {2} {3}",
                         MY_DICT_LOC,
                         PHONE_OUTPUT,
                         PHONE_CREATION_SCRIPT,
                         WORDS_MLF
                         )

    print(command)
    os.system(command)

createPhoneTranscript()