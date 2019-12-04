import pandas
import re
import xlrd

"""
    PIL(PIL:PILK), MELL(MEL:MELK)
"""
_io = 'C:\\KLNET\\(NEW)가제트용 스케줄(최종).xlsx'

excel = xlrd.open_workbook(_io)

# print(len(excel.sheets()))

# sheet_0 = excel.sheet_by_index(0) # Open the first tab
# print("ROW:",sheet_0.nrows)
# print("COL:",sheet_0.ncols)
data = []
for sheet in excel.sheets():    
    rows = []
    for row_index in range(sheet.nrows):
        cols=[]
        for col_index in range(sheet.ncols):
            value = sheet.cell(rowx=row_index,colx=col_index).value  
            cols.append(value)
        rows.append(cols)
    data.append(rows)

print(data)
# print(data[0][3][1])
