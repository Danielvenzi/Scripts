import os
import sys

results = str(os.popen("fdisk -l | grep 'Disk /' | grep -Ev '/dev/mapper' | grep -Po '\K/dev/.+:'").read())
results = results.strip(':\n')

print(results)
