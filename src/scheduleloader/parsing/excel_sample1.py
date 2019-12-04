import pandas
import re
import xlrd

"""
    FESCO
"""

_io = 'C:\\KLNET\\12월 9일자 스케줄.xlsx'

workbook = xlrd.open_workbook(_io)
sheet = workbook.sheets()[0]
rows = sheet.get_rows()
next(rows) # skip first row
for row in rows:
    if all([cell.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK)
            for cell in row]):
        print('skip')
        break
    # process this non-empty row here...