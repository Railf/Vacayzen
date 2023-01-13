from pathlib import Path

import csv


def GetDataFromCSV():
    data = {}
    with open(Path.home() / "Downloads/plates.csv") as file:
        reader = csv.DictReader(file)

        data = list(reader)
    
    return data


def CreateCSV(name, data):
    print("generating", name + ".csv...")

    namePath = "Downloads/" + name + ".csv"

    filename = str(Path.home() / namePath)

    with open(filename, 'w') as file:
        write = csv.writer(file)
        write.writerows(data)


properties = GetDataFromCSV()
counts     = []
results    = []

for index, property in enumerate(properties):
    for x in range(int(property['Count'])):
        results.append([property['Name'],property['Address']])

CreateCSV("results", results)