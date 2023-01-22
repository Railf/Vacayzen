from pathlib import Path

import csv


def GetDictFromCSV(file):
    print("creating dictionary from",file + "...")
    filePath = "Downloads/" + file

    data = {}
    with open(Path.home() / filePath) as openFile:
        reader = csv.DictReader(openFile)

        data = list(reader)
    
    return data


def CreateCSV(name, data):
    print("generating", name + ".csv...")

    namePath = "Downloads/" + name + ".csv"

    filename = str(Path.home() / namePath)

    with open(filename, 'w') as file:
        write = csv.writer(file)
        write.writerows(data)


properties = GetDictFromCSV("plates.csv")
results    = []

for index, property in enumerate(properties):
    for x in range(int(property['Count'])):
        results.append([property['Name'],property['Address']])

CreateCSV("results", results)