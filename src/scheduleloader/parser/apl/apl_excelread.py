import pandas
import re
import xlrd
import traceback
# from xlrd.xldate.XLDateAmbiguous import XLDateAmbiguous

"""
    APL(APL:APLU)
"""
# _io = 'C:\\KLNET\\12월 9일자 스케줄.xlsx'

class parser():
    _line_code = "APL"
    _sheet = None
    _filename = None
    
    def __init__(self, filename):
        self._filename = filename
    def parsing(self):
        print("apl parsing start")
        excel = xlrd.open_workbook(self._filename)

        # print(len(excel.sheets()))

        # sheet_0 = excel.sheet_by_index(0) # Open the first tab
        # print("ROW:",sheet_0.nrows, "COL:",sheet_0.ncols)
        data = []
        sheet1_last_row = 0
        print("sheet count:", len(excel.sheets()))
        # sheet_count = len(excel.sheets())
        try:
            
            for sheet_index in range(0, len(excel.sheets())):
                # print("sheet_index:", sheet_index)
                sheet = excel.sheet_by_index(sheet_index)
                self._sheet = sheet
                rows = []
                # print(sheet.merged_cells)
                # print("sheet.nrows:", range(sheet.nrows))


                if sheet_index == 0:
                    sheet1_last_row = int(sheet.nrows)
                for row_index in range(sheet.nrows):
                    # print(row_index,":" ,range(sheet.nrows))
                    cols=[]
                    for col_index in range(sheet.ncols):
                        # print( "sheet:", sheet_index, "row:", row_index, "col:", col_index, "type:", sheet.cell(rowx=row_index,colx=col_index).ctype )
                        # print(type(sheet.cell(rowx=row_index,colx=col_index).value))
                        # if sheet.cell(rowx=row_index,colx=col_index).ctype == 3:
                        if sheet.cell(rowx=row_index,colx=col_index).ctype == xlrd.XL_CELL_BLANK:
                            value = sheet.cell(rowx=row_index,colx=col_index).value
                            cols.append(value)
                        elif sheet.cell(rowx=row_index,colx=col_index).ctype == xlrd.XL_CELL_DATE:
                            # print("value",sheet.cell(rowx=row_index,colx=col_index).value)
                            # print(xlrd.xldate_as_tuple(sheet.cell(rowx=row_index,colx=col_index).value, excel.datemode))
                            if sheet.cell(rowx=row_index,colx=col_index).value != None:
                                # print("333333333333")
                                # print(sheet.cell(rowx=row_index,colx=col_index).value)
                                # print(type(sheet.cell(rowx=row_index,colx=col_index).value))
                                # print("--------")
                                # value = xlrd.xldate_as_tuple(3.0, excel.datemode)
                                try:
                                    value = xlrd.xldate_as_tuple(sheet.cell(rowx=row_index,colx=col_index).value, excel.datemode)
                                    value = str(value[0]) + str(value[1]).zfill(2) + str(value[2]).zfill(2)
                                    cols.append(value)
                                except BaseException as error:
                                    value = sheet.cell(rowx=row_index,colx=col_index).value
                                    cols.append(value)
                            # print("date value", value)
                            else:
                                value = sheet.cell(rowx=row_index,colx=col_index).value
                                cols.append(value)
                        else:
                            value = sheet.cell(rowx=row_index,colx=col_index).value
                            cols.append(value)
                    rows.append(cols)
                data.append(rows)

            # print(data)
            return data
            # print(data[0][3][1])

        except Exception as identifier:
            print('Exception:', identifier)
            traceback.print_exc()
            pass 

    def parsing1(self):
        excel = xlrd.open_workbook(self._filename)

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

        # print(data)
        return data
        # print(data[0][3][1])

    def migration(self, excel):

        print("length:", len(excel))
        data = [] #line_code, vessel_name, port_name, 
        for i in range(0, len(excel)):
            for j in range(0, len(excel[i])):
                for k in range(0, len(excel[i][j])):
                    # print(i,":",j,":",k,":",excel[i][j][k])
                    try:
                        # 각 선박/항차 별 엑셀 표의 시작 위치
                        if "VESSEL" in str(excel[i][j][k]) and "VOY" in str(excel[i][j][k+2]):
                            print("start ================> ", i,":",j,":",k)
                            data.extend(self.get_routes(excel, i,j,k))
                        elif "VESSEL" in str(excel[i][j][k]) and "VOY" in str(excel[i][j][k+1]):
                            print("start ================> ", i,":",j,":",k)
                            data.extend(self.get_routes(excel, i,j,k))
                        elif "VESSEL / VOYAGE" in str(excel[i][j][k]):
                            print("start ================> ", i,":",j,":",k)
                            data.extend(self.get_routes(excel, i,j,k))
                    except Exception as identifier:
                        print(identifier)
                        traceback.print_exc()
                        pass
        # print(data)

        return data

    def get_routes(self, excel, i, j, k):
        ports = {}
        vessel_index = 0
        voy_index = 0
        port_start_index = 0
        port_end_index = 0
        row_start = j
        row_end = 0
        routes = []
        # vessel        voy        port        date
        # print("continue ================> ", i,":",j,":",k)
        # endrow = 0
        # endcol = 0
        for kk in range(k, len(excel[i][j])):

            # print("merge is:",self.is_merge(j, kk))
            # print(i,":",j,":",kk,":",excel[i][j][kk], "merge is:",self.is_merge(j, kk))
            print(i,":",j,":",kk,":",excel[i][j][kk])
            # if "" in str(excel[i][j][kk]) or None == str(excel[i][j][kk]) or "*" in str(excel[i][j][kk]):

            if "VESSEL / VOYAGE" in str(excel[i][j][kk]):
                vessel_index = kk
                voy_index = kk+2
            # if "VESSEL" in str(excel[i][j][kk]):
            #     vessel_index = kk

            # if "VOY" in str(excel[i][j][kk]):
            #     voy_index = kk

            if "" != str(excel[i][j][kk]) and None != str(excel[i][j][kk]) and "*" not in str(excel[i][j][kk]) and "VESSEL / VOYAGE" not in str(excel[i][j][kk]):
                ports[str(kk)] = excel[i][j][kk]
                if "\n" in ports[str(kk)]:
                    ports[str(kk)] = ports[str(kk)].replace("\n"," ")                
                if port_start_index == 0:
                    port_start_index = kk

            # print(">>>",str(excel[i][j][kk]),"<<<<")

            if port_start_index > 0 and ("" == str(excel[i][j][kk]) or None == str(excel[i][j][kk]) or "*" in str(excel[i][j][kk])):
                port_end_index = kk-1
                print("end ================> ", i,":",j,":",kk)
                break
            
            if kk == len(excel[i][j])-1:
                port_end_index = kk
                print("end ================> ", i,":",j,":",kk)



        for jj in range(row_start+2, len(excel[i])):
            outerbreak = False
            for kk in range(vessel_index, port_end_index):
                if kk == vessel_index:
                    if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]) :
                        row_end = jj-1
                        outerbreak = True
                        break
                # if kk == voy_index:
                #     if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]) :
                #         row_end = jj-1
                #         outerbreak = True
                #         break
                # if kk == port_end_index-1:
                #     if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]):
                #         row_end = jj-1
                #         outerbreak = True
                #         break

            if outerbreak:
                break
            
            row_end = jj

        print("ports:", ports)
        print("row_start:", row_start, "row_end:", row_end, "vessel_index:", vessel_index, "voy_index:", voy_index, "port_start_index:", port_start_index, "port_end_index:", port_end_index)


        try:
            # for jj in range(j+1, len(excel[i])):
            vessel = ""
            for jj in range(row_start+2, row_end+1):
                outerbreak = False
                voy = ""
                port = ""
                seq = 0
                # line_code = "SFK"
                # print("range:", list(range(len(excel[i][jj]))))
                print("range:", list(range(vessel_index, port_end_index+1)))
                for kk in range(vessel_index, port_end_index+1):
                # for kk in range(len(excel[i][jj])):
                    # print(i,":",jj,":",kk,":",excel[i][jj][kk]) 
                    # if "" in str(excel[i][j][kk]) or None == str(excel[i][j][kk]) or "*" in str(excel[i][j][kk]):
                    date = ""
                    if kk == vessel_index:
                        # if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]):
                        # if None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]):
                        # if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]) :
                        #     outerbreak = True
                        #     break
                        if "" != str(excel[i][jj][kk]):
                            vessel = excel[i][jj][kk]
                    if kk == voy_index:
                        # if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]):
                        if "" != str(excel[i][jj][kk]):
                            voy = excel[i][jj][kk]
                            # print("route:", route)

                    if kk > port_start_index -1 and kk < port_end_index + 1 :
                        if "" != str(excel[i][jj][kk]) and "-" != str(excel[i][jj][kk]):
                            port = ports[str(kk)]
                            date = excel[i][jj][kk]
                            # print("route:", {'line_code':line_code, 'vessel': vessel, 'voy': voy, 'port': port, 'date': date, 'seq':seq})
                            seq = seq + 1
                            routes.append({'line_code':self._line_code, 'vessel': vessel, 'voy': voy, 'port': port, 'date': date, 'seq':seq})
                            
                            

                

                # if outerbreak:
                #     # print("routes:", routes)
                #     break

        except Exception as identifier:
            print('Exception:', identifier)
            traceback.print_exc()
            pass

        return routes

    def is_merge(self, row, col):
        print(row,"," ,col)
        # print(self.sheet.merged_cells)
        # print("crange", crange)
        for crange in self._sheet.merged_cells:
            rlo, rhi, clo, chi = crange
            for rowx in range(rlo,rhi):
                for colx in range(clo, chi):
                    # print(rowx, colx)
                    if row == rowx and col == colx:
                        return True
        return False

