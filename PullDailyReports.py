from pathlib import Path

import credentials
import webbrowser
import os

import GetBenchmarkReport
import GetScenicStaysReport
import GetSubmissionsSWBSA

path = str(Path.home() / "Downloads")


def RenameFiles(path):
    print("renaming files...")

    os.chdir(path)

    for file in os.listdir(path):
        if "Output_" in file:
            os.rename(file, "Benchmark - Credit Program.xlsx")
        if "trip-items" in file:
            os.rename(file, "Scenic Stays 30A - Credit Program.csv")
        if "Export_ExportRentalsByDay" in file:
            os.rename(file, "SWBSA - Rentals By Day.csv")
    
    print("done")


def OpenDestinations(urls):
    for url in urls:
        os.system("open " + urls[url])


RenameFiles(path)
OpenDestinations(credentials.GoogleSheetURLs)
webbrowser.open("file://" + path)