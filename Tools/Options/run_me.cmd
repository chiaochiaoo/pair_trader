@echo off
python -m pip install --user numpy pandas
python -m pip install -U git+https://github.com/mariostoev/finviz
python option.py > log.txt