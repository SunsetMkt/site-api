# This is a zipimport example
import sys
sys.path.insert(0, 'example.zip')  # Add .zip file to front of path
import some_script_in_the_zip_file
some_script_in_the_zip_file.main()
