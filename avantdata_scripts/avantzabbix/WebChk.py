import json
import os
import sys
import time
import random

Host = sys.argv[1]

then = time.time()
Result = os.popen("bash ./WebChk.sh -h {0}".format(Host)).read()
now = time.time()
Result = Result.strip("\n")
time = now-then
Result = Result+";{0}".format(time)
print(Result)
