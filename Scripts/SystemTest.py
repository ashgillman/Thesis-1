from subprocess import call, check_output, check_call
from os import environ

TEST_DIR = environ['HOME'] + "/Dropbox"

check_output(["ls", "-a", "../.."])

results = check_output(["ls", TEST_DIR])

print(TEST_DIR)
print(results.split(b"\n"))
