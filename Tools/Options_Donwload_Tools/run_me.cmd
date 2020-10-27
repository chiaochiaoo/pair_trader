@echo off
set /p id="Enter Symbols: (Example: AAPL)  " "
python options_downloader.py %id% > log.txt