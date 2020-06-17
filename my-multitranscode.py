#!/usr/bin/python

import sys
import os
import subprocess
import termcolor
import argparse
import csv

argParser = argparse.ArgumentParser()
argParser.add_argument('inputCsv')
arguments = argParser.parse_args()

inputCsv = arguments.inputCsv

print termcolor.colored('=========================== Parsing Input CSV ===========================', 'blue')
print termcolor.colored('Input CSV: ', 'blue'),  inputCsv

summaryList = []

with open(inputCsv) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for row in csvReader:
        #print (row)
        inputMkv = row['InputDir'] + "/" + row['InputBaseName'] + row['InputTrackName'] + ".mkv"
        outputName = row['OutputDir'] + "/" + row['OutputBaseName'] + " S" + row['OutputSeason'] + "E" + row['OutputEpisode'] + " - " + row['OutputEpName']
        outputMkv = outputName + '.mkv'
        outputSrt = outputName + '.srt'
        frameRate = ""
        if row["FrameRate"] != "":
            frameRate = "-f " + row["FrameRate"] + " "
        crop = ""
        if row["Crop"] != "":
            crop = "-c " + row["Crop"] + " "
        otherParams = ""
        if row["Params"] != "":
            otherParams = row["Params"] + " "
            otherParams = otherParams.replace('\"', '')
        print "Transcoding " + inputMkv + " to " + outputMkv
        commandLine = "my-transcode.py " + crop + frameRate + otherParams + " \"" + inputMkv + "\" \"" + outputMkv + "\""
        print termcolor.colored("Transcode Command: ", 'blue'), commandLine
        #transStatus = 0
        transStatus = os.system(commandLine)

        # Try to extract subtitles for this title
        print ('Attempting to extract subtitles from ' + inputMkv + ' to ' + outputSrt)
        subCmdLine = 'my-subextract.py \"' + inputMkv + '\" \"' + outputSrt + '\"'
        print termcolor.colored("Subtitle Command: ", 'blue'), subCmdLine
        #subStatus = 0
        subStatus = os.system(subCmdLine)

        # Store the results for summary printout
        transSummary = (inputMkv, outputName, transStatus, subStatus)
        summaryList.append(transSummary)

print
formatStr = '{:<30} {:<70} {:<10} {:<10}'
print (termcolor.colored(formatStr.format('Input File', 'Output Name', 'Encode', 'Subtitle'), 'blue'))
print (termcolor.colored('{:=<120}'.format(''), 'blue'))
for row in summaryList:
    if row[2] != 0:
        encodeStatus = termcolor.colored("Failed!", 'red')
    else:
        encodeStatus = termcolor.colored("Success!", 'green')

    if row[3] == 0:
        subtitleStatus = termcolor.colored("No subs found", 'yellow')
    else:
        subtitleStatus = termcolor.colored(str(row[3]) + ' sub(s) found', 'green')

    print (formatStr.format(row[0], os.path.basename(row[1]), encodeStatus, subtitleStatus))

print

exit(0)
