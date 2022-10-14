from pathlib import Path

import credentials
import webbrowser
import os

import GetBenchmarkReport
import GetScenicStaysReport

path = str(Path.home() / "Downloads")


def RenameFiles(path):
    print("renaming files...")

    os.chdir(path)

    for file in os.listdir(path):
        if "Output_" in file:
            os.rename(file, "Benchmark - Credit Program.xlsx")
        if "trip-items" in file:
            os.rename(file, "Scenic Stays 30A - Credit Program.csv")
    
    print("done")


def OpenDestinations(urls):
    for url in urls:
        os.system("open " + urls[url])


RenameFiles(path)
OpenDestinations(credentials.GoogleSheetURLs)
webbrowser.open("file://" + path)