# This is a zipimport example
import os
import sys

print(os.getcwd())
sys.path.insert(0, "myutils.zip")  # Add .zip file to front of path
import myutils

myutils.hello()
