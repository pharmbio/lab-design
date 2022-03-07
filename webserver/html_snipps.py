import logging
import string
import dbqueries
from typing import List, Dict


def drawImageAnalysesPerPlateTable(dictrows: List[Dict[str, str]]) -> string:
    return drawTable(dictrows)

def drawPlateLayoutTable(dictrows: List[Dict[str, str]]) -> string:
    return drawTable(dictrows)

def drawPlateTable(dictrows: List[Dict[str, str]]) -> string:
    return drawTable(dictrows)

def drawTable(dictrows: List[Dict[str, str]]) -> string:
    out = []

    out.append('<thead>')

    logging.info("len(dictrows)" + str(len(dictrows)))

    if len(dictrows) > 0:
        for key in dictrows[0]:
            out.append('<th>' + str(key) + '</th>')


    out.append('</thead>')

    for row in dictrows:
        out.append('<tr>')
        for key, value in row.items():
            out.append('<td>' + str(value) + '</td>')
        out.append('</tr>')

    return "".join(out)

def drawProjectSelect(selected_id) -> string:

    options = dbqueries.list_all_projects()
    value_col = 'name'

    out = []

    out.append('<option value=""></option>')

    for option in options:

        out.append('<option value="' + option[value_col] + '"')
        if option[value_col] == selected_id:
            out.append(' selected ')

        out.append('>' + option[value_col] + '</option>')

    out.append('<option value="%">All</option>')

    return "".join(out)


def drawPlateSelect(options, selected_id) -> string:
    out = []

    out.append('<option value=""></option>')

    for option in options:

        out.append('<option value="' + option['barcode'] + '"')
        if option['barcode'] == selected_id:
            out.append(' selected ')

        out.append('>' + option['barcode'] + '</option>')

    out.append('<option value="%">All</option>')

    return "".join(out)

def drawLayoutSelect(plate_layouts, selected_layout_id) -> string:
    out = []

    out.append('<option value=""></option>')

    for plate_layout in plate_layouts:

        out.append('<option value="' + plate_layout['layout_id'] + '"')
        if plate_layout['layout_id'] == selected_layout_id:
            out.append(' selected ')

        out.append('>' + plate_layout['layout_id'] + '</option>')

    out.append('<option value="%">All</option>')

    return "".join(out)


def drawVisualPlateLayout(plateLayout):
    nRows = 16 # 8
    nCols = 24 # 12
    rownames = ['A','B','C','D','E','F','G','H','J','I','J','K','L','M','N','O']

    out = []

    out.append('<tr>')

    #add empty cell before (to match column headers)
    out.append('<td class="headerCell"></td>')

    for nCol in range(1, nCols + 1):
        out.append('<td class="headerCell">' + str(nCol) + '</td>')

    out.append('</tr>')

    for nRow in range(0, nRows):
        out.append('<tr>')

        for nCol in range(0, nCols + 1):

            if nCol == 0:
                out.append('<td class="headerCell">' + rownames[nRow] + '</td>')
            else:
                out.append('<td class="wellCell">' + rownames[nRow] +  str(nCol) + '</td>')

        out.append('</tr>')

    return "".join(out)