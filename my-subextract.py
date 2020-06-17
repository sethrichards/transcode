#!/usr/bin/python3

import sys
import argparse
import subprocess

argParser = argparse.ArgumentParser()
argParser.add_argument('inputFile')
argParser.add_argument('outputFile')
arguments = argParser.parse_args()

inputFile = arguments.inputFile
outputFile = arguments.outputFile

trackListCmd = ['mkvmerge',  '-i', '-F', 'verbose-text', inputFile]
trackExtractCmd = 'mkvextract'

trackListProc = subprocess.Popen(trackListCmd, stdout=subprocess.PIPE)
#print(subprocess.list2cmdline(trackListProc.args))
rawTracks = trackListProc.communicate()[0].decode('utf-8').split('\n')

#print (rawTracks)

subsFound = 0
for line in rawTracks:
    if(line.find('SubRip') != -1):
        #print(line)
        subsFound += 1
        trackNum = line.split(" ")[2].replace(':','')
        print ('Found SRT subtitles at track ' + trackNum + ', extracting with mkvextract...')
        extractCmd = [trackExtractCmd, inputFile, 'tracks', trackNum + ':' + outputFile]
        #print(subprocess.list2cmdline(extractCmd))
        extractProc = subprocess.Popen(extractCmd)

if (subsFound == 0):
    print ("No text subtitles found in file " + inputFile)

sys.exit(subsFound)
