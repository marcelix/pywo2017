# Biblioteke
from xlrd import open_workbook
from tabulate import tabulate
from math import ceil
import itertools

def IspisTablice(filename, max_rows = -1, max_columns = -1, max_cell_length = "-1", verbose = "false"):
    # Učitavanje Excel filea
    knjiga = open_workbook(filename)
    firstSheet = knjiga.sheet_by_index(0) 
    if verbose == "true":
        print ("[i] Otvorena je datoteka {0}\n".format(filename))

    # Globalne varijable
    maxRows = max_rows
    maxColumns = max_columns
    maxChars = 0
    truncate = max_cell_length
    if (truncate != "-1"):
        maxChars = int(truncate)

    # Handleanje overflowa
    # (da se ne prikazuje cijela tablica ako je velika)
    numRows = firstSheet.nrows
    numColumns = firstSheet.ncols
    if numRows > maxRows and maxRows != -1:
        numRows = maxRows

    if numColumns > maxColumns and maxColumns != -1:
        numColumns = maxColumns

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
            if truncate != "-1" and len(str(firstSheet.cell(row, column).value)) > maxChars:
                currentRow.append(str(firstSheet.cell(row, column).value)[:maxChars] + "...")
            else:
                currentRow.append(firstSheet.cell(row, column).value)
        if (firstSheet.nrows > maxRows and maxColumns != -1):
            currentRow.append("...")
        broj += 1
        workSheet.append(currentRow)

    # Overflow handling - zadnji redak
    zadnjiRedak = [""]
    for i in range(numColumns):
        zadnjiRedak.append("...")  
    if (firstSheet.ncols > maxColumns and maxRows != -1):
        workSheet.append(zadnjiRedak)

    # Ispis radnog lista
    if verbose == "true":
        print("Sadržaj prvog lista (\"{0}\")\n".format(knjiga.sheet_by_index(0).name)) 

    print(tabulate(workSheet, tablefmt="grid", floatfmt=".2f", stralign="center", numalign="center"))
    

a1 = input("Ime datoteke (s nastavkom): ")
a2 = int(input("Koliko redaka da se ispiše (-1 za sve): "))
a3 = int(input("Koliko stupaca da se ispiše (-1 za sve): "))
a4 = int(input("Maksimalna duljina teksta u ćeliji (-1 za cijeli tekst): "))
IspisTablice(a1,a2,a3,a4,"true")
#IspisTablice("knjiga.xls", max_cell_length="5", verbose="true", max_columns=6)