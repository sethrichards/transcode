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
argParser.add_argument('-e', '--encoder',
                       help='Encoder to use. Passed through to video_transcoding. Defaults to "x264".')
argParser.add_argument('-n', '--dry-run', action='store_true',
                       help='Dry run, don\'t actually call other-transcode')
argParser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose debug')
argParser.add_argument('infile')
argParser.add_argument('outfile')

args = argParser.parse_args()
if args.verbose:
    print (termcolor.colored('Args:','magenta'), args)

# Always preserve English subtitles, add all English audio
other_arg = "--quiet --main-audio eng --add-audio eng --audio-width main=double --audio-width other=surround --add-subtitle eng"

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
        if args.verbose:
            print (termcolor.colored("Framerate:", 'magenta'), frameNum.get(rate))
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

# Handle encoder argument
if args.encoder:
    encoder_arg = "--encoder %s" % (args.encoder)
else:
    encoder_arg = "--encoder x264"

# Filenames should be left over
infile = os.path.abspath(args.infile)
outfile = os.path.abspath(args.outfile)

# Do the actual transcoding!
print (termcolor.colored('=========================== Starting Transcode ===========================', 'cyan'))

if infile.endswith('.mkv') or infile.endswith('.ts'):
    print (termcolor.colored('Input file: ', 'cyan'), infile)
    print (termcolor.colored('Output file: ', 'cyan'), outfile)
    transcode_command = 'transcode-video %s %s %s %s "%s" -o "%s"' % (crop_arg, frame_arg, encoder_arg, other_arg, infile, outfile)
    print (termcolor.colored('Transcode Command: ', 'cyan'), transcode_command)
    print

    if (args.dry_run == False):
        retval = os.system(transcode_command)
    else:
        retval = 1

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
