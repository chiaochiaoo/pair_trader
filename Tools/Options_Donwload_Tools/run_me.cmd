@echo off
set /p id="Enter Symbols: (Example: AAPL)  "
set /p d="Enter dates(Example: 2020-10-23)  "
python options_downloader.py %id% %d%