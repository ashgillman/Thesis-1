from subprocess import call, check_output, check_call
from os import environ
from platform import system as checkOS


HOME = environ['HOME']

# Check whether this is running on my mac or windows machine
if checkOS() == "Darwin":
    THESIS_DIR = "/Dropbox/Thesis/Data"
else:
    THESIS_DIR = ""

OPERATING_DIR = str.format("{0}{1}", HOME, THESIS_DIR)

call(['cd', OPERATING_DIR])
print(check_output(['find . \\ -name "*.wv1" -print']))
#egrep -i -e .*[si_tr]+.*\.wv[0-9] Files.txt > Audio_List.txt
