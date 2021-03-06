#===============================================================================
# Watches files in specified directory and their subdirectories,
# and handles them appropriately.
#===============================================================================
import sys
import time
import os

#--- custom handling here ---#

def convert_coffeescript(file_name):
    """
    hardcoded lambda for converting shpaml
    """
    basename = os.path.basename(file_name)
    dir = file_name[0:len(file_name) - len(basename)]
    converted_name = os.path.join(dir, os.path.splitext(basename)[0] + ".html")
    os.system(
        "iced --runtime inline -c " + file_name)


def convert_shpaml(file_name):
    """
    hardcoded lambda for converting shpaml
    """
    basename = os.path.basename(file_name)
    dir = file_name[0:len(file_name) - len(basename)]
    converted_name = os.path.join(dir, os.path.splitext(basename)[0] + ".html")
    os.system(
        "python /Users/nubela/Workspace/transcompiler-watcher/src/shpaml.py " + file_name + " > " + converted_name)


def convert_sass(file_name):
    """
    hardcoded lambda for converting sass
    """
    basename = os.path.basename(file_name)
    dir = file_name[0:len(file_name) - len(basename)]
    converted_name = os.path.join(dir, os.path.splitext(basename)[0] + ".css")
    os.system(
        "sass " + file_name + " > " + converted_name)

#--- config here ---#

HANDLING = {
    ".sass": convert_sass,
    ".shpaml": convert_shpaml,
    ".coffee": convert_coffeescript,
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
            for ext, transcompiler_handling in HANDLING.iteritems():
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
