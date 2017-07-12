from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python36\tcl\tk8.6'

exe=Executable(
     script="excel-to-console.py",
     base="Console",
     )
setup(

     version = "0.5",
     description = "Program koji Excel datoteku ispisuje u konzolu",
     author = "Goran Alković",
     name = "ExcelToConsole",
     #options = {'build_exe': {'packages':packages,'include_files':includefiles}},
     executables = [exe]
     )