import os
import platform

if platform.system() == "Windows":
    DATA_DIR = "J:\\ConvertData\\Thesis Data\\Desk\\Testing\\Development\\"
    OUTPUT_PATH = "J:\\ClassifierTraining\\Classifiers\\"
else:
    DATA_DIR = "\\Volumes\\External\\ConvertData\\Thesis Data\\Desk\\Testing\\Development\\"
    OUTPUT_PATH = "\\Volumes\\External\\ClassifierTraining\\Classifiers\\"

MFC_EXTENSION = ".mfc"
AUDIO_EXTENSION = ".wav"

OUTPUT_FILE = "J:\\Test.scp"


for folder in os.listdir(DATA_DIR):
    for file in os.listdir(DATA_DIR+folder):
        if AUDIO_EXTENSION in file:
            [name, ext] = file.split('.')

            inputPath = str.format("{0}{1}\\{2}", DATA_DIR, folder, name)
            fid = open(OUTPUT_FILE, 'a+')

            output = str.format("{0}{1} {2}{3}{4}",
                                inputPath,
                                AUDIO_EXTENSION,
                                OUTPUT_PATH,
                                name,
                                MFC_EXTENSION)
            
            fid.write(output + "\n")

            fid.close()
        
