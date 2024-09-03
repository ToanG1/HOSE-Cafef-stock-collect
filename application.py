import openpyxl
import stockData

headers = ['Mã cổ phiếu', 'Vốn hóa', 'Cổ đông lớn', 'Tỷ lệ']

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append([])

stockData.collect(sheet, headers)

for col_num, value in enumerate(headers, start=1):
    sheet.cell(row=1, column=col_num, value=value)
workbook.save("hose-collect.xlsx")