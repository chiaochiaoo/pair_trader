@echo off
git pull
set /p id="Enter Symbols: (Example: SPY.AM,QQQ.NQ) "
python Spread_viewer.py %id%