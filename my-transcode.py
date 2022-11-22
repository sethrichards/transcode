#!/usr/bin/python3

import sys
import os
import subprocess
import termcolor
import argparse

argParser = argparse.ArgumentParser(description='Frontend for transcode-video')
argParser.add_argument('-f', '--framerate',
                       help='One of [film|ntsc|pal].')
argParser.add_argument('-c', '--crop',
                       help='0 for no crop, otherwise output from "detect-crop". Defaults to "detect".')
argParser.add_argument('-d', '--deinterlace',
                       help='Deinterlace filter to use. One of [detelecine|deinterlace|decomb]')
argParser.add_argument('infile')
argParser.add_argument('outfile')

args = argParser.parse_args()

# Always preserve English subtitles
other_arg = "--quiet --add-subtitle eng"

# Handle framerate argument
if args.framerate:
    def getFramerate(rate):
        frameNum = {
            "film": "23.976",
            "pal" : "25",
            "PAL" : "25",
            "ntsc": "29.97",
            "NTSC": "29.97",
        }
        #print frameNum.get(rate)
        return (frameNum.get(rate))
    frame_arg = "--force-rate %s" % (getFramerate(args.framerate))
else:
    frame_arg = ""

# Handle cropping argument
if args.crop:
    if args.crop == "0":
        crop_arg = "--crop 0:0:0:0"
    else:
        crop_arg = "--crop %s" % (args.crop)
else:
    crop_arg = "--crop detect"

# Handle deinterlacing argument
if args.deinterlace:
    if args.deinterlace == 'deinterlace':
        other_arg += " --filter deinterlace"
    elif args.deinterlace == 'detelecine':
        other_arg += " --filter detelecine"
    elif args.deinterlace == 'decomb':
        other_arg += " --filter decomb"

#sys.exit(0)

# Filenames should be left over
infile = os.path.abspath(args.infile)
outfile = os.path.abspath(args.outfile)

# Do the actual transcoding!
print (termcolor.colored('=========================== Starting Transcode ===========================', 'cyan'))

if infile.endswith('.mkv') or infile.endswith('.ts'):
    print (termcolor.colored('Input file: ', 'cyan'), infile)
    print (termcolor.colored('Output file: ', 'cyan'), outfile)
    transcode_command = 'transcode-video %s %s %s "%s" -o "%s"' % (crop_arg, frame_arg, other_arg, infile, outfile)
    print (termcolor.colored('Transcode Command: ', 'cyan'), transcode_command)
    print
    #retval = 1
    retval = os.system(transcode_command)
    if retval != 0:
        print
        print (termcolor.colored('=========================== Transcode failed! ===========================', 'red'))
        print ('\a')
        print
        sys.exit(-1)
    else:
        print
        print (termcolor.colored('=========================== Transcode succeeded ===========================', 'green'))
        print ('\a')
        print

    print (termcolor.colored('=========================== Finished! ===========================', 'green'))
    print
else:
    print (termcolor.colored('Input file not an MKV!', 'red'))
    print ('\a')
    sys.exit(-1)
