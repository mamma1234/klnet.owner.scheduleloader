import pandas
import re
import xlrd
import traceback
"""
    FESCO(FEO:FSCO)
"""
# _io = 'C:\\KLNET\\12월 9일자 스케줄.xlsx'

line_code = "FEO"

class parser():
    def __init__(self, filename):
        self.filename = filename

    def parsing(self):
        excel = xlrd.open_workbook(self.filename)

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
                    # if sheet.cell(rowx=row_index,colx=col_index).ctype == 3:
                    if sheet.cell(rowx=row_index,colx=col_index).ctype == xlrd.XL_CELL_DATE:
                        # print(xlrd.xldate_as_tuple(sheet.cell(rowx=row_index,colx=col_index).value, excel.datemode))
                        value = xlrd.xldate_as_tuple(sheet.cell(rowx=row_index,colx=col_index).value, excel.datemode)
                        value = str(value[0]) + str(value[1]).zfill(2) + str(value[2]).zfill(2)
                        # print("date value", value)
                        cols.append(value)
                    else:
                        value = sheet.cell(rowx=row_index,colx=col_index).value
                        cols.append(value)
                rows.append(cols)
            data.append(rows)

        # print(data)
        return data
        # print(data[0][3][1])


    def parsing1(self):
        excel = xlrd.open_workbook(self.filename)

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
        # print("length:", len(excel))
        col_skip = -1
        data = [] #line_code, vessel_name, port_name, 
        for i in range(0, len(excel)):
            for j in range(0, len(excel[i])):
                col_skip = -1
                for k in range(0, len(excel[i][j])):
                    # print(i,":",j,":",k,":",excel[i][j][k])
                    try:
                        if k <= col_skip and col_skip > -1: 
                            continue                        
                        # 각 선박/항차 별 엑셀 표의 시작 위치
                        if "VESSEL" in str(excel[i][j][k]) and "VOY" in str(excel[i][j][k+2]):
                            # print("start ================> ", i,":",j,":",k)
                            data.extend(self.get_routes(excel, i,j,k))
                            col_skip = k+2
                    except Exception as identifier:
                        print(identifier)
                        traceback.print_exc()
                        pass
        # print(data)
        return data

    def get_routes(self, excel, i, j, k):
        ports = {}
        routes = []
        svc = ""
        # svc_index = -1
        # col_start = -1        
        # vessel        voy        port        date
        # print("continue ================> ", i,":",j,":",k)
        # endrow = 0
        # endcol = 0

        svc = excel[i][j-1][k]
        for kk in range(k+3, len(excel[i][j])):
            # print(i,":",j,":",kk,":",excel[i][j][kk])
            # if "" in str(excel[i][j][kk]) or None == str(excel[i][j][kk]) or "*" in str(excel[i][j][kk]):

            if "" != str(excel[i][j][kk]) and None != str(excel[i][j][kk]) and "*" not in str(excel[i][j][kk]):
                ports[str(kk)] = excel[i][j][kk]
                if "\n" in ports[str(kk)]:
                    ports[str(kk)] = ports[str(kk)].replace("\n"," ")

            if "" == str(excel[i][j][kk]) or None == str(excel[i][j][kk]) or "*" in str(excel[i][j][kk]):
                break
            
        print("ports:", ports)

        # svc = excel[i][row_start-1][col_start]
        for jj in range(j+1, len(excel[i])):
            try:
                outerbreak = False
                vessel = ""
                voy = ""
                port = ""
                date = ""
                seq = 0
                # line_code = "FEO"
                for kk in range(k, len(excel[i][jj])):
                    # print(i,":",jj,":",kk,":",excel[i][jj][kk]) 
                    # if "" in str(excel[i][j][kk]) or None == str(excel[i][j][kk]) or "*" in str(excel[i][j][kk]):
                    if kk == 1:
                        # if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]):
                        # if None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]):
                        if "*" in str(excel[i][jj][kk]):
                            outerbreak = True
                            break
                        if "" != str(excel[i][jj][kk]):
                            vessel = excel[i][jj][kk]
                    if kk == 3:
                        # if "" == str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]):
                        if "" != str(excel[i][jj][kk]):
                            voy = excel[i][jj][kk]
                            # print("route:", route)

                    if kk > 3:
                        if "" != str(excel[i][jj][kk]) and "-" != str(excel[i][jj][kk]):
                            # print("ports[kk]:", ports[kk])
                            end_port = ports[str(kk)]
                            end_date = excel[i][jj][kk] 
                            start_port = ""
                            start_date = ""

                            if "" != date:
                                start_port = port
                                start_date = date
                            else:
                                start_port = end_port
                                start_date = end_date
                            # print("route:", route)
                            seq = seq + 1
                            routes.append({'line_code':line_code, 'vessel': vessel, 'voy': voy, 'end_route_name': end_port, 'end_route_date': end_date, 'start_route_name': start_port, 'start_route_date': start_date, 'seq':seq, 'svc': svc})

                            port = end_port
                            date = end_date
                            # routes.append(route)
                            # print("routes:", routes)
                # print("route:", route)
                # routes.append(route)
                if outerbreak:
                    break
            except Exception as identifier:
                print(identifier)
                traceback.print_exc()
                pass
        return routes
        # print("routes:", routes)
                        # goto stop
            # if "" == str(excel[i][j][kk]) or None == str(excel[i][j][kk]) or "*" in str(excel[i][j][kk]):
            #     break
            # ports.append({'port':excel[i][j][kk],'col':kk})

        # print(ports)
        # for jj in range(j, len(excel[i])):
        #     print("continue ================> ", i,":",j,":",k)


        #     for kk in range(k, len(excel[i][jj])):
        #         if "" in str(excel[i][jj][kk]) or None == str(excel[i][jj][kk]) or "*" in str(excel[i][jj][kk]):
        #             endrow = jj
        #             endcol = kk
        #             print(i,":",jj,":",kk,":",excel[i][jj][kk]) 
                    