#!/usr/bin/env python3

import sys
import os
import subprocess
import termcolor
import argparse
import csv

# Script locations - may need to modify depending on installation
transcode_script = "~/bin-local/transcode/my-transcode.py"
subextract_script = "~/bin-local/transcode/my-subextract.py"

argParser = argparse.ArgumentParser()
argParser.add_argument('-w', '--hardware', action='store_true',
                       help='Use hardWare-accelerated HEVC encoder instead of AVC')
argParser.add_argument('inputCsv')
arguments = argParser.parse_args()

inputCsv = arguments.inputCsv

print(termcolor.colored('=========================== Parsing Input CSV ===========================', 'blue'))
print(termcolor.colored('Input CSV: ', 'blue'),  inputCsv)

summaryList = []

with open(inputCsv) as csvFile:
    csvReader = csv.DictReader(csvFile)
    csvList = list(csvReader)
    num_records = len(csvList)
    #for row in csvReader:
    for record, row in enumerate(csvList):
        #print (row)
        print (termcolor.colored("Processing file: ", 'blue'), f"{record + 1}/{num_records}")
        # Build the filenames
        inputMkv = row['InputDir'] + "/" + row['InputBaseName'] + row['InputTrackName'] + ".mkv"
        outputDir = row['OutputDir'];
        if (outputDir == ""):
            outputDir = os.getcwd();
        outputName = outputDir + "/" + row['OutputBaseName'] + " S" + row['OutputSeason'].zfill(2) + "E" + row['OutputEpisode'].zfill(2) + " - " + row['OutputEpName'] + " " + row['OutputSuffix']
        outputMkv = outputName + '.mkv'
        outputSrt = outputName + '.srt'

        # Frame rate
        frameRate = ""
        if row["FrameRate"] != "":
            frameRate = "-f " + row["FrameRate"] + " "

        # Cropping
        crop = ""
        if row["Crop"] != "":
            crop = "-c " + row["Crop"] + " "

        # Deinterlacing
        deinterlace = ""
        if row["Deinterlace"] != "":
            deinterlace = "-d " + row["Deinterlace"] + " "

        other_args = ""
        if (arguments.hardware):
            other_args += " -w "
        
        # Transcode!
        print("Transcoding " + inputMkv + " to " + outputMkv)
        commandLine =  transcode_script + " " + crop + frameRate + deinterlace + other_args + " \"" + inputMkv + "\" \"" + outputMkv + "\""
        print(termcolor.colored("Transcode Command: ", 'blue'), commandLine)
        #transStatus = 0
        transStatus = os.system(commandLine)

        # Try to extract subtitles for this title
        print('Attempting to extract subtitles from ' + inputMkv + ' to ' + outputSrt)
        subCmdLine = subextract_script + ' \"' + inputMkv + '\" \"' + outputSrt + '\"'
        print(termcolor.colored("Subtitle Command: ", 'blue'), subCmdLine)
        #subStatus = 0
        subStatus = os.system(subCmdLine)

        # Store the results for summary printout
        transSummary = (inputMkv, outputName, transStatus, subStatus)
        summaryList.append(transSummary)

# Print out a status summary
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
