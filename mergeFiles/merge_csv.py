# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 21:12:09 2022

@author: sagar
"""
import sys
import os
from glob import glob
import csv
from xlsxwriter.workbook import Workbook

def file_finder(rootDirectoryToProcess):
    resList = [y for x in os.walk(rootDirectoryToProcess) for y in glob(os.path.join(x[0], '*.csv'))]
    print(resList)
    return resList
def deleteCsvFiles(csvFile):
    try:
        os.remove(csvFile)
        print("{} is deleted.".format(csvFile))
        return 0
    except Exception as e:
            print(e)
            return 1
    

def merge_csv_excel(rootDirectoryToProcess,excelFileName,deleteCsvFilesFlag):
    try:
        excelFullPath=os.path.join(rootDirectoryToProcess,excelFileName)
        csvFiles= file_finder(rootDirectoryToProcess)
        if len(csvFiles) ==0:
            print("No csv file to merge")
            return 1
        workbook = Workbook(excelFullPath + '.xlsx')
        for csvfile in csvFiles:
            print("{} is merging ...".format(csvfile))            
            worksheet = workbook.add_worksheet( os.path.basename(csvfile))
            with open(csvfile, 'rt', encoding='utf8') as f:
                reader = csv.reader(f)
                for r, row in enumerate(reader):
                    for c, col in enumerate(row):
                        worksheet.write(r, c, col)
        workbook.close()
        print("{} is created".format(excelFullPath+ '.xlsx'))
        print(deleteCsvFilesFlag)  
        if deleteCsvFilesFlag == 'Yes' and  os.path.isfile(excelFullPath+ '.xlsx'):
            for csvFile in csvFiles:
                delFlag=deleteCsvFiles(csvFile)  
                
        return 0
    except Exception as e:
        print(e)
        return 1

if __name__ == "__main__":
    print(sys.argv[1])    
    print(sys.argv[2]) 
    print(sys.argv[3]) 
    rootDirectoryToProcess=sys.argv[1]
    excelFileName= sys.argv[2]
    deleteCsvFilesFlag= sys.argv[3]
    ret=merge_csv_excel(rootDirectoryToProcess,excelFileName,deleteCsvFilesFlag="Yes")
    if ret ==1:
        print('merging is failed')
    else:
        print("merging is succssful")