import subprocess
import sys
uiFile = "gui/" + sys.argv[1]
pyFile = uiFile.replace(".ui", "") + ".py"

res = subprocess.run("python -m PyQt5.uic.pyuic -x %s -o %s" %(uiFile, pyFile))

print(res)
