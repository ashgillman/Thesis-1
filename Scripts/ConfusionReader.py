confusionMatrix = "F:\\Thesis\\External\\ClassifierTraining\\Results\\Confusion.txt"
output = "F:\\Thesis\\External\\ClassifierTraining\\Results\\CleanMatrix.csv"

fid = open(confusionMatrix, 'r')
lines = fid.readlines()
fid.close()

outputFile = open(output, 'w')

for line in lines:
    data = line.split()
    data.reverse()
    data.pop(0)
    data.pop(0)
    data.reverse()
    data.pop(0)

    outputFile.write(",".join(data))
    outputFile.write("\n")

outputFile.close()