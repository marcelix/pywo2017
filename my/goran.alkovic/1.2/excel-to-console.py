from xlrd import open_workbook
from tabulate import tabulate
from math import ceil
import itertools
import os
import sys

# CLS funkcija
def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

# Glavna funkcija
def IspisTablice(filename, worksheet=None, max_rows = -1, max_columns = -1, max_cell_length = -1, verbose = "false"):
    # Učitavanje Excel filea
    try:
        knjiga = open_workbook(filename)
    except:
        print("[!] File {0} does not exist or is damaged.".format(filename))
        return
    
    if verbose == "true":
        print ("[i] Opened {0} successfully.".format(filename))

    # Odabir radnog lista
    if worksheet == None and len(list(knjiga.sheets())) > 1:
        print ("[i] Worksheets in {0}".format(filename))
    allSheets = []
    indeks = 1
    for k in knjiga.sheets():
        if worksheet == None and len(list(knjiga.sheets())) > 1:
            print("    ({0}) {1}".format(indeks, k.name))
        allSheets.append(k)
        indeks += 1
    if len(allSheets) == 1:
        selectedSheet = allSheets[0]
    else:
        if worksheet == None and len(list(knjiga.sheets())) > 1:
            odabraniList = int(input("    > "))
            #clearScreen()
        else:
            odabraniList = worksheet
        try:
            selectedSheet = allSheets[odabraniList - 1]
        except:
            #clearScreen()
            print("[x] Selected worksheet does not exist.")
            return
    allSheets = None
    
    # Globalne varijable
    maxRows = max_rows
    maxColumns = max_columns
    maxChars = -1
    truncate = max_cell_length
    if (truncate != -1):
        maxChars = int(truncate)

    # Handleanje overflowa
    # (da se ne prikazuje cijela tablica ako je velika)
    numRows = selectedSheet.nrows
    numColumns = selectedSheet.ncols
    if numRows > maxRows and maxRows != -1:
        numRows = maxRows

    if numColumns > maxColumns and maxColumns != -1:
        numColumns = maxColumns
        
    # Ako se unese više redaka nego što postoji
    if maxRows > numRows:
        maxRows = numRows
    if maxColumns > numColumns:
        maxColumns = numColumns

    # Za sadržaj datoteke
    workSheet = []

    # Za brojanje stupaca
    broj = 1
    # Prvi stupac tablice (slovčane oznake)
    abeceda = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    if numColumns > 25:
        slova = []
        for num in range(int(ceil(numColumns/25))):
            slova += [''.join(i) for i in itertools.product(abeceda, repeat = num)]
    else:
        slova = []
        slova = [''.join(i) for i in itertools.product(abeceda, repeat = 1)]
    slova = slova[0:numColumns]
    prviStupac = [""]
    
    for i in range(numColumns):
        prviStupac.append(slova[i])    
    workSheet.append(prviStupac)

    # Spremanje sadržaja datoteke u listu
    for row in range (numRows):
        currentRow = []
        # Oznaka retka
        currentRow.append(str(broj))
        for column in range (numColumns):
            if truncate != -1 and len(str(selectedSheet.cell(row, column).value)) > maxChars:
                currentRow.append(str(selectedSheet.cell(row, column).value)[:maxChars] + "...")
            else:
                currentRow.append(selectedSheet.cell(row, column).value)
        if (selectedSheet.nrows > maxRows and maxColumns != -1):
            currentRow.append("...")
        broj += 1
        workSheet.append(currentRow)

    # Overflow handling - zadnji redak
    zadnjiRedak = [""]
    for i in range(numColumns):
        zadnjiRedak.append("...")  
    if (selectedSheet.ncols > maxColumns and maxRows != -1):
        workSheet.append(zadnjiRedak)

    # Ispis radnog lista
    if verbose == "true":
        #print("[i] Sadržaj lista \"{0}\"".format(selectedSheet.name))
        displayMsg = ""
        if maxRows == -1 and maxColumns != -1:
            displayMsg = "[i] Showing all rows and {0} column(s).".format(maxColumns)
        if maxRows != -1 and maxColumns == -1:
            displayMsg = "[i] Showing {0} row(s) and all columns.".format(maxRows)
        if maxRows != -1 and maxColumns != -1:
            displayMsg = "[i] Showing {0} row(s) and {1} column(s).".format(maxRows, maxColumns)
        if maxChars != -1:
            displayMsg += " Cells are truncated to {0} character(s).\n".format(maxChars)
        else:
            displayMsg += "\n"
        print(displayMsg)
    print(tabulate(workSheet, tablefmt="fancy_grid", floatfmt=".2f", stralign="center", numalign="center"))

def startProgram():
    # Čitanje argumenata
    args = sys.argv
    
    # Help
    if len(args) >= 2 and ("-h" in args or "--help" in args):
        print("\nexcel-to-console help\n")
        print("Usage:")
        print("   excel-to-console <filename[.xls]>")
        print("   excel-to-console <filename[.xls] --verbose")
        print("   excel-to-console <filename[.xls] -compact")
        print("   excel-to-console <filename[.xls]> -r 10 -c 5")
        print("   excel-to-console <filename[.xls]> -rows 5 -trunc 10")
        print("   excel-to-console -h | --help")
        print()
        print("Options")
        print("   [-h | --help]")
        print("      Show this screen.")
        print()
        print("   [-f | -file] <file name[.xls]>")
        print("      File name of the worksheet you want to open. Required.")
        print()
        print("   [-s | -ws | -sheet <worksheet index>]")
        print("      Index of the worksheet you want to open. Index is zero-based.")
        print("      If only one worksheet is present this argument is ignored.")
        print("      If no argument is passed, the program will prompt user to select the workbook.")
        print()
        print("   [-cp | -compact]")
        print("      Compact mode: Shows at most 5 rows and 8 columns of a given worksheet.")
        print("                    Cell contents are truncated to 10 characters maximum.")
        print()
        print("   [-r | -rows | -maxrows <number of rows>]")
        print("      Limits the maximum number of rows displayed.")
        print("      Undisplayed rows will be marked with '...'")
        print("      Cannot be used with Compact mode.")
        print()
        print("   [-c | -cols | -maxcols <number of columns>]")
        print("      Limits the maximum number of columns displayed.")
        print("      Undisplayed rows will be marked with '...'")
        print("      Cannot be used with Compact mode.")
        print()
        print("   [-t | -trim | -truncate | -shorten-to <number of characters>]")
        print("      Limits the number of characters displayed in each worksheet cell.")
        print("      Ellipsis (...) marks the shortened cells")
        print()
        print("   [-full | --fullscreen]")
        print("      Clear the console before starting the program.")
        print()
        print()
        return
    
    # Provjera obveznog argumenta
    if len(args) == 1:
        print("\n[x] Required argument: file name\n")
        return

    # Argumenti
    f = args[1]
    ws = None
    rows = -1
    cols = -1
    trunc = -1
    verb = "false"
    
    # Pomoćne varijable
    isCompact = "false"
                    
    if "--verbose" in args:
        verb = "true"
        
    # Kompaktni način
    
    if "-cp" in args or "-compact" in args:
        isCompact = "true"
    
    if isCompact == "true":
        rows = 5
        cols = 8
        trunc = 10
    
    # Datoteka koju učitavamo
    
    if "-f" in args:
        f = args[args.index("-f") + 1]
    if "-file" in args:
        f = args[args.index("-file") + 1]
                
    if ".xls" not in f:
            f = f + ".xls"
    
    # Clear screen prije pokretanja
    if "--fullscreen" in args or "-full" in args:
        clearScreen()
        
    # Max retci
    if isCompact == "false":
        if "-r" in args:
            rows = int(args[args.index("-r") + 1])
        if "-rows" in args:
            rows = int(args[args.index("-rows") + 1])
        if "-maxrows" in args:
            rows = int(args[args.index("-maxrows") + 1])
            
    # Max stupci
    if isCompact == "false":
        if "-c" in args:
            cols = int(args[args.index("-c") + 1])
        if "-cols" in args:
            cols = int(args[args.index("-cols") + 1])
        if "-maxcols" in args:
            cols = int(args[args.index("-maxcols") + 1])
            
    # Truncate
        if "-t" in args:
            trunc = int(args[args.index("-t") + 1])
        if "-trim" in args:
            trunc = int(args[args.index("-trim") + 1])
        if "-trunc" in args:
            trunc = int(args[args.index("-trunc") + 1])
        if "-shorten-to" in args:
            trunc = int(args[args.index("-shorten-to") + 1])
    
    # Worksheet
        if "-s" in args:
            ws = int(args[args.index("-s") + 1])
        if "-sheet" in args:
            ws = int(args[args.index("-sheet") + 1])
        if "-ws" in args:
            ws = int(args[args.index("-ws") + 1])    
            
    # Pozivanje funkcije
    print()
    IspisTablice(f, worksheet=ws, max_rows = rows, max_columns = cols, max_cell_length = trunc, verbose = verb)
    print()
    
startProgram()