import pandas
import re
import xlrd
import os
# import scheduleloader.parser

from scheduleloader.parser.feo import feo_excelread
from scheduleloader.parser.sfk import sfk_excelread
from scheduleloader.parser.ial import ial_excelread
from scheduleloader.parser.apl import apl_excelread
from scheduleloader.parser.one import one_excelread
from scheduleloader.parser.pil import pil_excelread
# from scheduleloader.parser.mel import mel_excelread
from scheduleloader.parser.msc import msc_excelread
from scheduleloader.parser.tsl.sally import tsl_sally_excelread


def inspection(filepath):
    try:
        print("==============email address inspection=============")
        filename = os.path.basename(filepath)
        print(filename)
        temp = filename.split("^")
        print(temp[0])
        # temp = temp[0].split(os.path.sep)
        # print(temp[-1])
        excel = xlrd.open_workbook(filepath)

        if "IMPORT" in temp[1]:
            return None

        if "DHEKim@fesco.com" in temp[0]:
            return feo_excelread.parser
        elif "JayB@sofastkorea.com" in temp[0]:
            return sfk_excelread.parser
        elif "kelly.kim@interasialine.com" in temp[0]:
            return ial_excelread.parser
        elif "seulgi.park@apl.com" in temp[0]:
            return apl_excelread.parser
        elif "kr.bpit@one-line.com" in temp[0]:
            return one_excelread.parser
        elif "custsvc@pus.pilship.com" in temp[0]:
            return pil_excelread.parser
        # elif "custsvc@pus.pilship.com" in temp[0]:
        #     return mel_excelread.parser
        elif "seongjun.cheon@msc.com" in temp[0]:
            return msc_excelread.parser
        elif "sally@tslines.co.kr" in temp[0]:
            return tsl_sally_excelread.parser

            
        # elif "custsvc@pus.pilship.com" in temp[0]:
        #     return pil_excelread.parser
        # elif "sally@tslines.co.kr" in temp[0]:
        #     return tsl_sally_excelread.parser
    except Exception as identifier:
        pass


    try:
        print("==============excel content inspection=============")
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

    except Exception as identifier:
        pass


    # print(data)
    return None
    # print(data[0][3][1])
