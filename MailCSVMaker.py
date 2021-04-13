import csv
import os
import xlrd


# from xlsxwriter import Workbook


def get_data_from_file(path):
    create_csv_file()
    try:
        # convert_txt_to_xlsx(path)
        wb = xlrd.open_workbook(path)
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        csv_file = open("csv-output/byla.csv", encoding='utf-8', mode='a')
        for columns in range(sheet.nrows):
            if not columns == 0:
                data = sheet.row_values(columns)
                add_to_mail_csv(data, csv_file)
        csv_file.close()
    except Exception as e:  # work on python 3.x
        print('Failed: ' + str(e))


# def convert_txt_to_xlsx(path):
#     # noinspection PyBroadException
#     try:
#         workbook = Workbook(path[:-4] + '.xlsx')
#         worksheet = workbook.add_worksheet()
#         with open(path, 'rt') as f:
#             reader = csv.reader(f, delimiter='\t')
#             for r, row in enumerate(reader):
#                 for c, col in enumerate(row):
#                     worksheet.write(r, c, col)
#         workbook.close()
#     except:
#         print('Some data may be lost')
#         print('Please close ' + os.path.basename(path[:-4] + '.xlsx'))


def read_SKU_list_from_file(sku_name, sku_weight, sku_package_weight):
    try:
        wb = xlrd.open_workbook('SKU.xlsx')
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        for columns in range(sheet.nrows):
            if not columns == 0:
                sku_name.append(sheet.row_values(columns)[0])
                sku_weight.append(sheet.row_values(columns)[1])
                sku_package_weight.append(sheet.row_values(columns)[2])
    except:
        print('read_SKU_list_from_file failed')


def get_weight(sku_name, sku_weight, sku_package_weight, sku_cloth):
    try:
        sku = str(sku_cloth).strip('123456789').strip()
        index_name = sku_name.index(sku)
        return int(sku_weight[index_name]) + int(sku_package_weight[index_name])
    except:
        print('get_weight failed. Couldnt find: ' + sku + ' in the SKU.xlsx, so used default weight 150')
        return 150


def add_to_mail_csv(data, csv_file):
    sku_name: list = []
    sku_weight: list = []
    sku_package_weight: list = []
    read_SKU_list_from_file(sku_name, sku_weight, sku_package_weight)
    order_weight = get_weight(sku_name, sku_weight, sku_package_weight, str(data[10]))
    order_weight = order_weight * int(data[12])
    if order_weight > 500:
        typo_of_shipment = 'P2P_1_M'
    else:
        typo_of_shipment = 'P2P_1_S'

    try:
        csv_file.write(
            '\n' + typo_of_shipment + ',,' + str(data[8]) + ',,,,,' + str(data[20]) + ',' + str(data[22]) +
            ',' + str(data[17]).replace(',', ' ') + ' ' + str(data[18]).replace(',', ' ') + ',' + str(
                data[19]).replace(',', ' ') + ' ' + str(data[21]) + ',' + str(data[23]) + ',' + str(data[9]) +
            ',' + str(data[7]) + ',' + str(order_weight) + ',,' + str(data[12]) +
            ',,,,,K2,' + str(data[12]) + ',,LT,Men\'s cotton shirts,' + str(data[12]) + ',' +
            str(order_weight) + ',10,,')
    except:
        print('add_to_mail_csv failed')


def create_csv_file():
    if not os.path.exists("csv-output/"):
        os.makedirs("csv-output/")
    if not os.path.exists("csv-output/byla.csv"):
        csv_file = open("csv-output/byla.csv", encoding='utf-8', mode='x')
        csv_file.write(
            "Siuntos rūšis,Terminalo ID,Gavėjo pavadinimas,Gavėjo įmonės pavadinimas,Gavėjo gatvė,Gavėjo namas,"
            "Gavėjo butas,Gavėjo gyvenvietė,Gavėjo pašto kodas,Adreso eilutė 1,Adreso eilutė 2,Gavėjo šalies kodas,"
            "Gavėjo mob. tel. (370xxxxxxxx),Gavėjo el. paštas,Svoris (g),Dalių skaičius,Pirmenybinis siuntimas,"
            "Draudimas (Eur),COD (Eur),Gauti informaciją apie įteiktą siuntą (POD),Moka gavėjas,Komentaras,"
            "Siuntos turinio kategorija,HS kodas,Prekių kilmės šalis,Siuntos turinio aprašymas anglų kalba,"
            "Kiekis (vnt),Deklaruojamas siuntos svoris (g),Deklaruojama vertė (eur),Nepavykus pristatyti")
        csv_file.close()
