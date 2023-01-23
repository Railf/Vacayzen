from pathlib import Path

import numpy as np

import csv


ROWS_PER_FILE = 750


def GetDictFromCSV(file):
    print("creating dictionary from",file + "...")
    filePath = "Downloads/" + file

    data = {}
    with open(Path.home() / filePath) as openFile:
        reader = csv.DictReader(openFile)

        data = list(reader)
    
    return data


def CreateCSV(name, data):
    print('generating', name + '.csv...')

    namePath = 'Downloads/' + name + '.csv'

    filename = str(Path.home() / namePath)

    with open(filename, 'w') as file:
        write = csv.writer(file)
        write.writerows(data)


properties  = GetDictFromCSV('plates.csv')
houseName   = []
noHouseName = []
plateCount  = 0

for index, property in enumerate(properties):
    plateCount += int(property['Count'])
    for x in range(int(property['Count'])):
        if property['Name'] == '':
            noHouseName.append([index, '',property['Address']])
        else:
            houseName.append([index, property['Name'], property['Address']])

for index, property in enumerate(houseName):
    property[0] = 'HOUSE-' + str(index)
    # TODO: Remove " from house names

for index, property in enumerate(noHouseName):
    property[0] = 'NOHOUSE-' + str(index)

platesWithNames   = len(houseName)
platesWithNoNames = len(noHouseName)
houseFiles        = []
noHouseFiles      = []

while (len(houseName) > ROWS_PER_FILE):
    houseFiles.append(houseName[:ROWS_PER_FILE])
    houseName = houseName[ROWS_PER_FILE:]

if len(houseName) > 0: houseFiles.append(houseName)

for index, file in enumerate(houseFiles):
    if index == 0: CreateCSV('house', file)
    else:          CreateCSV('house_'+str(index), file)


while (len(noHouseName) > ROWS_PER_FILE):
    noHouseFiles.append(noHouseName[:ROWS_PER_FILE])
    noHouseName = noHouseName[ROWS_PER_FILE:]

if len(noHouseName) > 0: noHouseFiles.append(noHouseName)

for index, file in enumerate(noHouseFiles):
    if index == 0: CreateCSV('no house', file)
    else:          CreateCSV('no house_'+str(index), file)


print('')
print('plates requested in file:            ', plateCount)
print('plates for homes with house name:    ', platesWithNames)
print('plates for homes without house name: ', platesWithNoNames)
print('plates to be printed:                ', platesWithNames + platesWithNoNames)
print('')
print('plates requested match to-be-printed?', str(plateCount == (platesWithNames + platesWithNoNames)).lower())
print('')
print('house files:                         ', len(houseFiles))
print('no house files:                      ', len(noHouseFiles))