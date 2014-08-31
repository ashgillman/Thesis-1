__author__ = 'Bdesktop'

MLF_FILE = "D:\\Dropbox\\phones0.mlf"
UNIQUE_PHN_FILE = "D:\\Dropbox\\uniquePhonemes"

fid = open(MLF_FILE, 'r')
output = open(UNIQUE_PHN_FILE, 'w')
phones = []

for line in fid:
    badLines = ['#', '"', '.']
    if line[0] in badLines:
        pass
    else:
        line = line.split('\t')
        phoneme = line[-1].strip("\n")

        if not phoneme in phones:
            output.write(phoneme + "\n")
            phones.append(phoneme)

output.close()
fid.close()