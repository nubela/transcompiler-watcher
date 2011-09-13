#===============================================================================
# Watches files in specified directory and their subdirectories,
# and handles them appropriately.
# 
# IE: SASS files (.sass) are automatically formatted to .css files.
#===============================================================================
import sys
import time
import os

#custom handling

def convert_shpaml(file_name):
    """
    hardcoded lambda for converting shpaml
    """
    basename = os.path.basename(file_name)
    converted_name = os.path.splitext(basename)[0] + ".html"
    os.system("python /home/nubela/Workspace/transcompiler-watcher/src/shpaml.py "  + file_name + " > " + converted_name)

#--- config here ---#

HANDLING = {
            ".sass": "sass",
            ".shpaml" : convert_shpaml, 
            }

POLLING_TIMEOUT = 2 #no of seconds to sleep in between scanning for files

#--- don't fuck below ---#

monitored_files = {}

def handle(dir):
    listing = os.listdir(dir)
    for l in listing:
        l = os.path.join(dir, l)
        if os.path.isdir(l):
            handle(l)
        else: #is file
            for ext,transcompiler_handling in HANDLING.iteritems():
                if ext in l:
                    if not (l in monitored_files) or monitored_files[l] != os.stat(l).st_mtime:
                        if hasattr(transcompiler_handling, '__call__'):
                            transcompiler_handling(l)
                        else:
                            os.system(transcompiler_handling + " " + l)
                        print l
                        monitored_files[l] = os.stat(l).st_mtime

def main():
    args = sys.argv
    scanning_directories = args[1:]
    while (True):
        for dir in scanning_directories:
            handle(dir)
        time.sleep(POLLING_TIMEOUT)
        
main()