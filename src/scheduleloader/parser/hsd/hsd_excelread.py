import pandas
import re
import xlrd
import datetime
import traceback
# from xlrd.xldate.XLDateAmbiguous import XLDateAmbiguous

"""
    HSD(HSD:HSDG)
"""

class parser():
    _line_code = "HSD"
    _sheets = []
    _filename = None
    def __init__(self, filename):
        self._filename = filename
    def parsing(self):
        print("hsd parsing start")
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
            # for sheet_index in range(0, 1):
                # print("sheet_index:", sheet_index)
                sheet = excel.sheet_by_index(sheet_index)

                print("processing:",sheet.name)
                if 'Gazette schedule' not in sheet.name:
                    continue

                self._sheets.append(sheet)
                rows = []
                # print(sheet.merged_cells)
                # print("sheet.nrows:", range(sheet.nrows))


                if sheet_index == 0:
                    sheet1_last_row = int(sheet.nrows)
                for row_index in range(sheet.nrows):

                    # if row_index > 10: return None
                    # print(row_index,":" ,range(sheet.nrows))
                    cols=[]
                    for col_index in range(sheet.ncols):
                        # print("value:",sheet.cell(rowx=row_index,colx=col_index).value)
                        # print("type:",type(sheet.cell(rowx=row_index,colx=col_index).value))
                        # print("sheet:", sheet_index, "row:", row_index, "col:", col_index, "type:", sheet.cell(rowx=row_index,colx=col_index).ctype )
                        # print("xlrd.XL_CELL_EMPTY:",xlrd.XL_CELL_EMPTY)
                        # print("xlrd.XL_CELL_BLANK:",xlrd.XL_CELL_BLANK)
                        # print("xlrd.XL_CELL_BOOLEAN:",xlrd.XL_CELL_BOOLEAN)
                        # print("xlrd.XL_CELL_ERROR:",xlrd.XL_CELL_ERROR)
                        # print("xlrd.XL_CELL_NUMBER:",xlrd.XL_CELL_NUMBER)
                        # print("xlrd.XL_CELL_DATE:",xlrd.XL_CELL_DATE)
                        # print("xlrd.XL_CELL_TEXT:",xlrd.XL_CELL_TEXT)

                        if sheet.cell(rowx=row_index,colx=col_index).ctype == xlrd.XL_CELL_EMPTY:
                            cols.append("")
                        elif sheet.cell(rowx=row_index,colx=col_index).ctype == xlrd.XL_CELL_BLANK:
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
                                    if isinstance(value, float):
                                        value = int(round(value))                                    
                                    cols.append(value)
                            # print("date value", value)
                            else:
                                value = sheet.cell(rowx=row_index,colx=col_index).value
                                cols.append(value)
                        elif sheet.cell(rowx=row_index,colx=col_index).ctype == xlrd.XL_CELL_TEXT:
                            value = sheet.cell(rowx=row_index,colx=col_index).value
                            # if "~" in value:
                            #     tmp = value.split('~')
                            #     if "/" in tmp[0]:
                            #         # print("tmp:",tmp[0], ":", tmp[0].strip(), ":")
                            #         # print(datetime.datetime.strptime(f"{datetime.datetime.now().year}{tmp[0].strip()}", "%Y%m/%d"))
                            #         value = datetime.datetime.strptime(f"{datetime.datetime.now().year}{tmp[0].strip()}", "%Y%m/%d").strftime("%Y%m%d")
                            # elif "~" in value:
                            #     tmp = value.split('-')
                            #     if "/" in tmp[0]:
                            #         value = datetime.datetime.strptime(f"{datetime.datetime.now().year}{tmp[0].strip()}", "%Y%m/%d").strftime("%Y%m%d")
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
                        if "Vessel" in str(excel[i][j][k]):
                            print("start ================> ", i,":",j,":",k)
                            data.extend(self.get_routes(excel, i,j,k))                        
                        elif "VESSEL" in str(excel[i][j][k]) and "VOY" in str(excel[i][j][k+2]):
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
        svc_index = -1
        col_start = -1
        svc = ""
        # vessel        voy        port        date
        # print("continue ================> ", i,":",j,":",k)
        # endrow = 0
        # endcol = 0
        svc = excel[i][j-1][k]
        for kk in range(k, len(excel[i][j])):

            # print("merge is:",self.is_merge(j, kk))
            # print(i,":",j,":",kk,":",excel[i][j][kk], "merge is:",self.is_merge(j, kk))
            print(i,":",j,":",kk,":",excel[i][j][kk])
            # if "" in str(excel[i][j][kk]) or None == str(excel[i][j][kk]) or "*" in str(excel[i][j][kk]):

            # if "VESSEL / VOYAGE" in str(excel[i][j][kk]):
            #     vessel_index = kk
            #     voy_index = kk+2
            if "Vessel" in str(excel[i][j][kk]):
                vessel_index = kk
                voy_index = kk

            # if "VESSEL" in str(excel[i][j][kk]):
            #     vessel_index = kk

            # if "VOY" in str(excel[i][j][kk]):
            #     voy_index = kk

            # if "" != str(excel[i][j][kk]) and None != str(excel[i][j][kk]) and "*" not in str(excel[i][j][kk]) and "VESSEL / VOYAGE" not in str(excel[i][j][kk]):
            if "" != str(excel[i][j][kk]) and None != str(excel[i][j][kk]) and "*" not in str(excel[i][j][kk]) \
                and "Vessel" not in str(excel[i][j][kk]):
                # and "VESSEL" not in str(excel[i][j][kk]) and "VOY" not in str(excel[i][j][kk]) \
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



        for jj in range(row_start+1, len(excel[i])):
            outerbreak = False
            if svc_index > -1:
                col_start = svc_index
            elif vessel_index > -1:
                col_start = vessel_index
            for kk in range(col_start, port_end_index):
                if kk == vessel_index:
                    if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]) :
                        row_end = jj-1
                        outerbreak = True
                        break
                    elif "Booking" in str(excel[i][jj][kk]):
                        row_end = jj-1
                        outerbreak = True
                        break                    
                if kk == voy_index:
                    if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]) :
                        if "BLANK SAILING" not in str(excel[i][jj][vessel_index]) and "TBN" not in str(excel[i][jj][vessel_index]):
                            row_end = jj-1
                            outerbreak = True
                            break
                # if kk == port_end_index-1:
                #     print("confirm:", str(excel[i][jj][kk]))
                    # if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]):
                    #     row_end = jj-1
                    #     outerbreak = True
                    #     break

            if outerbreak:
                break
            
            row_end = jj

        print("ports:", ports)
        print("row_start:", row_start, "row_end:", row_end, "col_start:", col_start, "vessel_index:", vessel_index, "voy_index:", voy_index, "port_start_index:", port_start_index, "port_end_index:", port_end_index, "svc_index:", svc_index)

        try:
            # for jj in range(j+1, len(excel[i])):
            vessel = ""
            svc = excel[i][row_start-1][col_start]

            for jj in range(row_start+1, row_end+1):
                outerbreak = False
                voy = ""
                port = ""
                date = ""
                seq = 0
                # line_code = "SFK"
                # print("range:", list(range(len(excel[i][jj]))))
                print("range:", list(range(col_start, port_end_index+1)))
                for kk in range(col_start, port_end_index+1):
                # for kk in range(len(excel[i][jj])):
                    # print(i,":",jj,":",kk,":",excel[i][jj][kk]) 
                    # if "" in str(excel[i][j][kk]) or None == str(excel[i][j][kk]) or "*" in str(excel[i][j][kk]):
                    # if kk == vessel_index:
                    #     # if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]):
                    #     # if None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]):
                    #     # if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]) :
                    #     #     outerbreak = True
                    #     #     break
                    #     if "" != str(excel[i][jj][kk]):
                    #         vessel = excel[i][jj][kk]
                    # if kk == voy_index:
                    #     # if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]):
                    #     if "" != str(excel[i][jj][kk]):
                    #         voy = excel[i][jj][kk]
                    #         # print("route:", route)

                    if kk == vessel_index:
                        vessel = excel[i][jj][kk]
                        voy = '0'
                        tinx = excel[i][jj][kk].rfind(' ')
                        if tinx > 0:
                            vessel = excel[i][jj][kk][:tinx].lstrip().rstrip()
                            voy = excel[i][jj][kk][tinx:].lstrip().rstrip()
                            print("vessel:",vessel, ",voy:", voy)


                    if kk > port_start_index -1 and kk < port_end_index + 1 :
                        if "" != str(excel[i][jj][kk]) and "-" != str(excel[i][jj][kk]):
                            end_port = ports[str(kk)]
                            end_date = str(excel[i][jj][kk])
                            start_port = ""
                            start_date = ""
                            
                            # print(excel[i][jj][kk], "end_date", end_date)
                            
                            if "" != date and len(end_date) < 3:
                                end_date = date[:6] + end_date
                                # print("end_date", end_date)

                            if "~" in end_date:
                                tmp = end_date.split('~')
                                if "/" in tmp[0]:
                                    # print("tmp:",tmp[0], ":", tmp[0].strip(), ":")
                                    # print(datetime.datetime.strptime(f"{datetime.datetime.now().year}{tmp[0].strip()}", "%Y%m/%d"))
                                    end_date = datetime.datetime.strptime(f"{datetime.datetime.now().year}{tmp[0].strip()}", "%Y%m/%d").strftime("%Y%m%d")
                            elif "-" in end_date:
                                tmp = end_date.split('-')
                                if "/" in tmp[0]:
                                    end_date = datetime.datetime.strptime(f"{datetime.datetime.now().year}{tmp[0].strip()}", "%Y%m/%d").strftime("%Y%m%d")
                            elif "/" in end_date:
                                tmp = end_date
                                end_date = datetime.datetime.strptime(f"{datetime.datetime.now().year}{tmp.strip()}", "%Y%m/%d").strftime("%Y%m%d")
                            # print("route:", {'line_code':line_code, 'vessel': vessel, 'voy': voy, 'port': port, 'date': date, 'seq':seq})

                            if "" != date:
                                start_port = port
                                start_date = date
                            else:
                                start_port = end_port
                                start_date = end_date
                                
                            seq = seq + 1
                            routes.append({'line_code':self._line_code, 'vessel': vessel, 'voy': voy, 'end_route_name': end_port, 'end_route_date': end_date, 'start_route_name': start_port, 'start_route_date': start_date, 'seq':seq, 'svc':svc})
                            
                            port = end_port
                            date = end_date

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

        for sheet in self._sheets:
            for crange in sheet.merged_cells:
                rlo, rhi, clo, chi = crange
                for rowx in range(rlo,rhi):
                    for colx in range(clo, chi):
                        # print(rowx, colx)
                        if row == rowx and col == colx:
                            return True
        return False


