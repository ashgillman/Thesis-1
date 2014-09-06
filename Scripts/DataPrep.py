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

TRAINING_DIR = str.format("{0}ClassifierTraining{1}", FILE_START, SEPARATOR)

WORDLIST = TRAINING_DIR + "Training" + SEPARATOR + "WordList"
GRAMMAR = TRAINING_DIR + "Training" + SEPARATOR + "GrammarFile"
WORDNET = TRAINING_DIR + "Training" + SEPARATOR + "WordNet"

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

createWordNet()