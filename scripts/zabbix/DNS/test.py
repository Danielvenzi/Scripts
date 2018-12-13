import sys
import os

Lines = os.popen("cat /etc/passwd | wc -l").read()
Lines = Lines.strip("\n")
print(Lines)
