import gspread

SAMPLE_SPREADSHEET_ID = '1ODlGRI8YekmjJlpeH8kyMsjZUkSz_GNIjMkkuqlr-kk'
SAMPLE_RANGE_NAME = 'Лист1'


# Указываем путь к JSON
gc = gspread.service_account(filename='credentials.json')
#Открываем тестовую таблицу
# sh = gc.open("Время ухода прихода сотрудников")
#Выводим значение ячейки A1
# print(sh.sheet1.get('A1'))

ind = 0
sht1 = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
names = sht1.sheet1.get('A:A')
# names = sht1.sheet1.get('B1')
name = ''
# print(names[1][0] == name)
# print(names)

worksheet = sht1.get_worksheet(0)
cell = worksheet.find("Кенешбеков Жанарбек Уланбекович")
print("Найдено в ячейке %s %s" % (cell.row, cell.address))
worksheet.update(f'B{cell.row}', '20.12.22  9:00')

# for i in range(len(names)):
#     if names[i][0] == "ФИО":
#         continue
#     if names[i][0] == name:
#         print(True)
#         ind = i+1
#     else:
#         print(False)
#
# print(ind)
