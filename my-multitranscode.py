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
        outputMkv = row['OutputDir'] + "/" + row['OutputBaseName'] + " S" + row['OutputSeason'] + "E" + row['OutputEpisode'] + " - " + row['OutputEpName'] + ".mkv"
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

        # Store the results for summary printout
        transSummary = (inputMkv, outputMkv, transStatus)
        summaryList.append(transSummary)

print
print (termcolor.colored('{:<35} {:<45} {:<10}'.format('Input File', 'Output File', 'Status'), 'blue'))
print (termcolor.colored('{:=<90}'.format(''), 'blue'))
for row in summaryList:
    if row[2] != 0:
        print ('{:<35} {:<45} {:<10}'.format(row[0], os.path.basename(row[1]), termcolor.colored("Failed!", 'red')))
    else:
        print ('{:<35} {:<45} {:<10}'.format(row[0], os.path.basename(row[1]), termcolor.colored("Success!", 'green')))

print

exit(0)
