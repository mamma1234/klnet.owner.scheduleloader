import pandas
import re
import xlrd

_io = 'C:\\KLNET\\12월 9일자 스케줄.xlsx'

all_data = [[]]
excel = xlrd.open_workbook(_io)
sheet_0 = excel.sheet_by_index(0) # Open the first tab

for row_index in range(sheet_0.nrows):
    row= ""
    for col_index in range(sheet_0.ncols):
        value = sheet_0.cell(rowx=row_index,colx=col_index).value             
        row += "{0} ".format(value)
        split_row = row.split()   
    all_data.append(split_row)

print(all_data)