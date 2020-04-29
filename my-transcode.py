#!/usr/bin/python

import sys
import os
import subprocess
import termcolor

infile = os.path.abspath(sys.argv[1])
outfile = os.path.abspath(sys.argv[2])

crop_arg = "--crop detect"
frame_arg = "--force-rate 23.976"
other_arg = "--add-subtitle eng --filter detelecine"

print termcolor.colored('=========================== Starting Transcode ===========================', 'cyan')

if infile.endswith('.mkv'):
    print termcolor.colored('Input file: ', 'cyan'), infile
    print termcolor.colored('Output file: ', 'cyan'), outfile
    transcode_command = 'transcode-video %s %s %s "%s" -o "%s"' % (crop_arg, frame_arg, other_arg, infile, outfile)
    print termcolor.colored('Transcode Command: ', 'cyan'), transcode_command
    print
    #retval = 1
    retval = os.system(transcode_command)
    if retval != 0:
        print
        print termcolor.colored('=========================== Transcode failed! ===========================', 'red')
        print
        sys.exit(-1)
    else:
        print
        print termcolor.colored('=========================== Transcode succeeded ===========================', 'green')
        print

    print termcolor.colored('=========================== Finished! ===========================', 'green')
    print
else:
    print termcolor.colored('Input file not an MKV!', 'red')
    sys.exit(-1)
    
