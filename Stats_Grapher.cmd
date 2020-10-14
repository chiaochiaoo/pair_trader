@echo off
git pull
set /p id="Enter Symbols: (Example: SPY) "
python Stats_report.py %id%