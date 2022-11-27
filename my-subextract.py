#!/usr/bin/python3

import sys
import argparse
import subprocess

argParser = argparse.ArgumentParser()
argParser.add_argument('-n', '--dry-run', action='store_true',
                       help='Dry run, don\'t actually call other-transcode')
argParser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose debug')
argParser.add_argument('inputFile')
argParser.add_argument('outputFile')
args = argParser.parse_args()

inputFile = args.inputFile
outputFile = args.outputFile

trackListCmd = ['mkvmerge',  '-i', '-F', 'text', inputFile]
trackExtractCmd = 'mkvextract'

trackListProc = subprocess.Popen(trackListCmd, stdout=subprocess.PIPE)
if args.verbose:
    print(subprocess.list2cmdline(trackListProc.args))
rawTracks = trackListProc.communicate()[0].decode('utf-8').split('\n')

if args.verbose:
    print ('Raw Tracks:', rawTracks)

subsFound = 0
for line in rawTracks:
    if(line.find('SubRip') != -1):
        if args.verbose:
            print(line)
        subsFound += 1
        trackNum = line.split(" ")[2].replace(':','')
        print ('Found SRT subtitles at track ' + trackNum + ', extracting with mkvextract...')
        extractCmd = [trackExtractCmd, inputFile, 'tracks', trackNum + ':' + outputFile]
        if args.verbose:
            print('Extract command line', subprocess.list2cmdline(extractCmd))
        if (args.dry_run == False):
            extractProc = subprocess.Popen(extractCmd)

if (subsFound == 0):
    print ("No text subtitles found in file " + inputFile)

sys.exit(subsFound)
