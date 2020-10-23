@echo off
set /p id="Enter Symbols: (seperate by ,) "
set /p n="Enter Days:"
set /p r="Market Hours only?(0 or 1):"
python Database.py d %id% %n% %r%