@echo off

pyinstaller out.py --onefile

move dist/out.exe %CD%
