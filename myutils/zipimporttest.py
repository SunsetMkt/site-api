# This is a zipimport example
import sys
import os
print(os.getcwd())
sys.path.insert(0, 'myutils.zip')  # Add .zip file to front of path
import myutils
myutils.hello()
