import pandas
import re
import xlrd
# import scheduleloader.parser

from scheduleloader.parser.pil import pil_excelread
from scheduleloader.parser.feo import feo_excelread

def inspection(filename):
    excel = xlrd.open_workbook(filename)

    # print(len(excel.sheets()))

    # sheet_0 = excel.sheet_by_index(0) # Open the first tab
    # print("ROW:",sheet_0.nrows)
    # print("COL:",sheet_0.ncols)
    data = []
    sheet1_last_row = 0
    # print("sheet count:", len(excel.sheets()))
    # sheet_count = len(excel.sheets())
    for sheet_index in range(0, len(excel.sheets())):
        sheet = excel.sheet_by_index(sheet_index)
        rows = []
        print("sheet.nrows:", range(sheet.nrows))

        if sheet_index == 0:
            sheet1_last_row = int(sheet.nrows)
        for row_index in range(sheet.nrows):
            # print(row_index,":" ,range(sheet.nrows))
            cols=[]
            for col_index in range(sheet.ncols):
                value = sheet.cell(rowx=row_index,colx=col_index).value  
                cols.append(value)
            rows.append(cols)
        data.append(rows)

    # print(sheet1_last_row)
    # print(sheet1_last_row, "===>" ,data[0][sheet1_last_row-3][0])

    # inspection_text
    # # print(data[0][0][0])
    # try:
    #     inspection_text
    # except expression as identifier:
    #     pass
    # finally:
    #     pass


    if "PACIFIC" in str(data[0][0][0]):
        print(str(data[0][0][0]))
        return pil_excelread.parser
    elif "FESCO" in str(data[0][sheet1_last_row-3][0]):
        print(str(data[0][sheet1_last_row-3][0]))
        return feo_excelread.parser
    else:
        return None
    # print(data)
    return None
    # print(data[0][3][1])
