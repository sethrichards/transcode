#!/usr/bin/python3

import sys
import os
import shutil
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
argParser.add_argument('-w', '--hardware', action='store_true',
                       help='Use hardWare-accelerated HEVC encoder instead of AVC')
argParser.add_argument('-n', '--dry-run', action='store_true',
                       help='Dry run, don\'t actually call other-transcode')
argParser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose debug')
argParser.add_argument('infile')
argParser.add_argument('outfile')

args = argParser.parse_args()
if args.verbose:
    print (termcolor.colored('Args:','magenta'), args)

use_old_transcode = False

# Handle deinterlacing argument first, as it forces us to fall back to video-transcode
other_arg =""
if args.deinterlace:
    print(termcolor.colored("Falling back to video-transcode to handle deinterlacing", "magenta"))
    use_old_transcode = True
    if args.deinterlace == 'deinterlace':
        other_arg += " --filter deinterlace"
    elif args.deinterlace == 'detelecine':
        other_arg += " --filter detelecine"
    elif args.deinterlace == 'decomb':
        other_arg += " --filter decomb"

# Determine which script we're using and set defaults
if (use_old_transcode == False):
    script_string = "other-transcode"
    if (args.hardware):
        encoder_arg = "--hevc --10-bit --eac3-aac"
    else:
        encoder_arg = "--x264 --eac3-aac"
    crop_arg      = "--crop auto"
    other_arg    += "--add-audio eng=surround --add-subtitle eng"
    frame_fragment = "--rate"
else:
    script_type   = "sw"
    script_string = "transcode-video"
    encoder_arg   = "--encoder x264"
    crop_arg      = "--crop detect"
    # Always preserve English subtitles, add all English audio
    other_arg    += " --main-audio eng --add-audio eng --audio-width main=double --audio-width other=surround --add-subtitle eng --quiet"
    frame_fragment = "--force-rate"
frame_arg = ""

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
    frame_arg = frame_fragment + " %s" % (getFramerate(args.framerate))

# Handle cropping argument
if args.crop:
    if args.crop == "0":
        crop_arg = "--crop 0:0:0:0"
    else:
        crop_arg = "--crop %s" % (args.crop)


# Handle encoder argument
if args.encoder:
    encoder_arg = "%s" % (args.encoder)

# Filenames should be left over
infile = os.path.abspath(args.infile)
script_outfile = os.path.join(os.getcwd(), os.path.basename(infile))
script_logfile = script_outfile + ".log"
outfile = os.path.abspath(args.outfile)
logfile = outfile + ".log"
subfile = os.path.splitext(outfile)[0] + ".srt"
if (args.verbose):
    print(termcolor.colored("Input File: ", 'magenta'), infile)
    print(termcolor.colored("Script Output File: ", 'magenta'), script_outfile)
    print(termcolor.colored("Script Log File: ", 'magenta'), script_logfile)
    print(termcolor.colored("Output File: ", 'magenta'), outfile)
    print(termcolor.colored("Log File: ", 'magenta'), logfile)
    print(termcolor.colored("Sub File: ", 'magenta'), subfile)

# Do the actual transcoding!
print (termcolor.colored('=========================== Starting Transcode ===========================', 'cyan'))

if infile.endswith('.mkv') or infile.endswith('.ts'):
    print (termcolor.colored('Input file: ', 'cyan'), infile)
    print (termcolor.colored('Output file: ', 'cyan'), outfile)
    transcode_command = '%s %s %s %s %s "%s"' % (script_string, crop_arg, frame_arg, encoder_arg, other_arg, infile)
    print (termcolor.colored('Transcode Command: ', 'cyan'), transcode_command)
    print

    if (args.dry_run == False):
        retval = os.system(transcode_command)
    else:
        retval = 0

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

        print (termcolor.colored('Moving output file: ', 'cyan'), "%s --> %s" % (os.path.basename(script_outfile), os.path.basename(outfile)))
        print (termcolor.colored('Moving log file: ', 'cyan'), "%s --> %s" % (os.path.basename(script_logfile), os.path.basename(logfile)))
        if (args.dry_run == False):
            shutil.move(script_outfile, outfile)
            shutil.move(script_logfile, logfile)

        sub_command = 'my-subextract.py "%s" "%s"' % (infile, subfile)
        print (termcolor.colored('Subextract command: ', 'cyan'), sub_command)
        if (args.dry_run == False):
            os.system(sub_command)
    print (termcolor.colored('=========================== Finished! ===========================', 'green'))
    print
else:
    print (termcolor.colored('Input file not an MKV!', 'red'))
    print ('\a')
    sys.exit(-1)
