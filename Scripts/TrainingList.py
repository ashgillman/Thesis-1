import os
import platform

if platform.system() == "Windows":
    CLASSIFIER_DIR = "J:\\ClassifierTraining\\Classifiers\\"
else:
    CLASSIFIER_DIR ="\\Volumes\\External\\ClassifierTraining\\Classifiers\\"

classifierExtensions = [".stft", ".lpc", ".mfc", ".nnmf"]

for ext in classifierExtensions:

    listFile = str.format("{0}{1}_list.scp", CLASSIFIER_DIR, ext.lstrip('.'))

    files = [f for f in os.listdir(CLASSIFIER_DIR) if ext in f]

    fid = open(listFile, 'w')

    for file in files:
        fid.write(str.format("{0}{1}\n", CLASSIFIER_DIR, file))

    fid.close()

