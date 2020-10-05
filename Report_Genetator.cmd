@echo off
git pull
set /p id="Enter Symbols: (Example: SPY) "
python Report_generator.py %id%