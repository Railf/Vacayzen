from ics import Calendar
from pathlib import Path
from glob import glob


import credentials
import webbrowser
import requests
import csv
import os


def WaitForDownload(filename, extension):
    print("downloading occupancy sources... ", end="")

    os.chdir(str(Path.home() / "Downloads"))

    while not glob(filename + "*." + extension):
        continue

def GetCSVFromGoogleSheetTab(sheetID,tabID):
    part0 = "https://docs.google.com/spreadsheets/d/"
    part1 = sheetID
    part2 = "/export?format=csv&gid="
    part3 = tabID

    webbrowser.open(part0 + part1 + part2 + part3)
    WaitForDownload("iCalendar Converter - SOURCES","csv")
    print("SUCCESS")


def GetDataFromCSV():
    data = {}
    with open(Path.home() / "Downloads/iCalendar Converter - SOURCES.csv") as file:
        reader = csv.DictReader(file)

        data = list(reader)
    
    return data

def CreateCSV(data, name):
    filepath = "Downloads/"+name+".csv"

    print("generating "+name+".csv...")

    with open(str(Path.home() / filepath), 'w') as file:
        write = csv.writer(file)
        write.writerows(data)

def TextDateToDate(text):
    return (text[4:6] + '/' + text[6:8] + '/' + text[0:4])

GetCSVFromGoogleSheetTab(credentials.GoogleSheetIDs["iCalendar Converter"],"1687799206")

calendars = []
calendars = GetDataFromCSV()

while calendars == []: continue

results = [["PARTNER","UNIT","ARRIVAL","DEPARTURE"]]
failures = [["PARTNER","UNIT"]]

for calendar in calendars:
    try:
        print("downloading", calendar["UNIT"], "occupancy... ", end="")

        reservations = Calendar(requests.get(calendar["CALENDAR"]).text)

        for reservation in reservations.events:
            results.append([calendar["PARTNER"], calendar["UNIT"], reservation.begin.format("MM/DD/YYYY"), reservation.end.format("MM/DD/YYYY")])
        
        print("SUCCESS")
    except:
        try:
            print("FAILED. Attempting next method...")
            print("downloading", calendar["UNIT"], "occupancy... ", end="")

            reservations = requests.get(calendar["CALENDAR"]).text

            if "DTSTART" not in reservations: raise Exception("Response does not include iCalendar data.")

            reservations = reservations.split('\n')

            starts = []
            ends = []

            for line in reservations:
                if "DTSTART" in line: starts.append(TextDateToDate(line[8:-1]))
                if "DTEND" in line: ends.append(TextDateToDate(line[6:-1]))
            
            for i, start in enumerate(starts):
                results.append([calendar["PARTNER"], calendar["UNIT"], starts[i], ends[i]])

        
            print("SUCCESS")
        except:
            print("FAILED")
            failures.append([calendar["PARTNER"], calendar["UNIT"]])
            continue


CreateCSV(failures, "failures")
CreateCSV(results,  "results")