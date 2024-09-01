import openpyxl
import stockData, data

headers = ['Mã cổ phiếu']

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append([])

stockData.collect(sheet, headers)

for col_num, value in enumerate(headers, start=1):
    sheet.cell(row=1, column=col_num, value=value)
workbook.save("hose-collect.xlsx")