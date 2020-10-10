import PySimpleGUI as sg
import re
from collections import OrderedDict
from copy import deepcopy



def readAsTable(filename):
    table = []
    with open(filename, "r") as iff_file:
        table = [line.strip() for line in iff_file.readlines()]

    table = [i.split("\t") for i in table]
    return table


def convert(filename):
    table = readAsTable(filename)
    i=0
    
    
    values = OrderedDict([  ("Bank Account", ""),
                ("Check Number" , "ACH",),
                ("TxnDate", ""),
                ("Payee", "John Smith",),
                ("Amount", ""),
                ("To be printed", "0",),
                ("Memo", ""),
                ("TxnExpLine Account", ""),
                ("TxnExpLine Amount", ""),
                ("TxnExpLine Memo", ""),
                ("TxnExpLine Billable Status" , "0")])

    finalTable = ""
    for key in values:
        finalTable += key
        finalTable += "\t"
    finalTable += "\n"

    def push(dictionary, table):
        for key in dictionary:
            table += dictionary[key] + "\t"
        table += "\n"
        return table


    # Find all transactions in table
    while i < len(table) and table[i][0].lower() != "endtrns":

        # check to see if a transaction begins
        while not re.match("^trns", table[i][0], flags = re.I):
            i+=1

        currentLine = table[i]
        # Gather relevant information from start transaction line
        
        if currentLine[2]:
            values["Check Number"] = currentLine[2]
        values["TxnDate"] = currentLine[4] 
        values["Bank Account"] = currentLine[5]
        values["Amount"] = currentLine[6] 
        values["Memo"] = currentLine[7] 
        values["To be printed"] = str(int(currentLine[8].lower() == "y"))
        values["Payee"] = currentLine[9] 
        i+=1

        while i < len(table) and table[i][0].lower() != "endtrns":
            values["TxnExpLine Account"] = table[i][5]
            values["TxnExpLine Amount"] = table[i][6]
            values["TxnExpLine Memo"] = table[i][7]
            finalTable = push(values, finalTable)
            i+=1

       
    return finalTable

if __name__ ==  "__main__":
    window = sg.Window('Convert IIF to TXT', [[sg.FileBrowse("Select File", file_types=(("IIF Files", "*.iif"),)), sg.B("Start", key="started")]])

    while True:
        event, values = window.read()

        filename = values["Select File"]
        if filename:
            data = convert(filename)
            with open(filename[:-3]+"txt", "w") as saveFile:
                saveFile.write(data)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
