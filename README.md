# Vacayzen
Code written by Ralph McCracken, while working at Vacayzen.


## SubmitToSWBSA.py
```
python3 SubmitToSWBSA.py
```

Automate submissions to an online form. Submissions to this form would take three people multiple hours, at least one day a week. This is now handled with this script, and completes execution in minutes.


## GetSubmissionsSWBSA.py
```
python3 GetSubmissionsSWBSA.py
```

Automates a daily reporting-pulling task. Sames a few minutes each day.


## GetBenchmarkReport.py
```
python3 GetBenchmarkReport.py
```

Automates a daily reporting-pulling task. Sames a few minutes each day.


## GetScenicStaysReport.py
```
python3 GetScenicStaysReport.py
```

Automates a daily reporting-pulling task. Sames a few minutes each day.


## PullDailyReports.py
```
python3 PullDailyReports.py
```

Simplifies the execution of scripts that are required daily. Sames a few minutes each day.


## GetEscapiaOccupancy.py
```
python3 GetEscapiaOccupancy.py {all / arrival / departure} {start data: MM/dd/YYYY} {end date: MM/dd/YYYY}
```

Pulls occupancy reports for each of Vacayzen's Escapia-using partners, and combines the reports into one file. Saves 30 minutes, multiple times each week.


## Get360BlueOccupancy.py
```
python3 Get360BlueOccupancy.py
```

Pulls occupancy reports for one of Vacayzen's partners, and combines the reports into one file. Saves 10 minutes, multiple times each week.


## GetWalkupsSWBSA.py
```
python3 GetWalkupsSWBSA.py {start date: MM/dd/YYYY} {end date: MM/dd/YYYY}
```

Automates a reporting-pulling task for the SWBSA billing process. Sames a few minutes each month.


## DoSWBSABilling.py
```
python3 DoSWBSABilling.py {start date: MM/dd/YYYY} {end date: MM/dd/YYYY}
```

Automates the invoice- and report-creation process of SWBSA's monthly billing cycle. Saves 4 hours each month.


## CloseOrders.py
```
python3 CloseOrders.py
```

Automates the order-closing process for each of Vacayzen's rental orders inside of integraRental. This was a $6,000 quote from the platforms' development team that was solved with this script--written in two days by Ralph McCracken. Saves multiple hours each day.



### TODO

- [x] Submit to Online Forms
- [x] Pull Reports
- [x] Simplify the Execution of Multiple Scripts
- [x] Automate Routine Tasks
- [x] Analyze Data from CSV Files
- [x] Create PDF Files
- [ ] Pull Occupancy Data From Online Tape Charts
- [ ] Pull Occupancy Data From iCalendar Files