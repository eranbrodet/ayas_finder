import re
from Tkinter import END, INSERT     # Index positions
import xlrd


def find(source, glossary, found, not_found):
    found.delete(1.0, END)
    not_found.delete(1.0, END)
    l1 = re.split('[, ]+', source.get(1.0, END).strip())
    l2 = re.split('[, ]+', glossary.get(1.0, END).strip())
    l1 = [x.upper() for x in l1]
    l2 = [x.upper() for x in l2]
    dict2 = {x[1]: x[0] for x in enumerate(l2)}
    for item in l1:
        if item == '':
            continue
        elif item in l2:
             found.insert(INSERT, "gene: %s --- index in glossary: %s\n" % (item, dict2[item]))
        else:
            not_found.insert(INSERT, "gene: %s --- not found\n" % (item,))


def get_from_excel(file_name, sheet_name, row_num=None, col_num=None):
    if (row_num is None) and (col_num is None):
        raise Exception("need either column or row.")
    workbook = xlrd.open_workbook(file_name)
    worksheet = workbook.sheet_by_name(sheet_name)

    if row_num is not None:
        cells = worksheet.row(row_num)
    else:
        cells = worksheet.col(col_num)
    return ", ".join([str(x.value) for x in cells])


def get_excel_sheets(file_name):
    workbook = xlrd.open_workbook(file_name)
    return workbook.sheet_names()