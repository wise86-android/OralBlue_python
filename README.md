# OralBlue_python
Python library to read the data from an OralB toothbrush

#Installation
This project is developed with Python 3.6.

Install the dependecy with:

`pip install -r requirements.txt`

# Run

## [OralBScanMain](OralBScanMain.py)
This project must be run as a root (bluepy require the root acces to do a ble scan).

This program scann for the toothbush, and display the available information inside the advertise

## [OralBConnectMain](OralBConnectMain.py)

If this program works we are 10m away!

This program, connect to a specific toothbrush and start reading data or changing the settings.
It hasn't any utility is done just to test the API

