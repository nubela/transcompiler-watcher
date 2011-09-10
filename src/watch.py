#===============================================================================
# Watches files in specified directory and their subdirectories,
# and handles them appropriately.
# 
# IE: SASS files (.sass) are automatically formatted to .css files.
#===============================================================================
import sys

#--- config here ---#

#--- don't fuck below ---#

monitored_files = {}

def main():
    args = sys.argv
    