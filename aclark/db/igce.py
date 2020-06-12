from django.http import HttpResponse
from openpyxl import Workbook

from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from openpyxl.styles import PatternFill


def render_xls(context, **kwargs):
    """
    """

    workbook = Workbook()
    filename = kwargs.get("filename")
    item = context["item"]
    bold = Font(bold=True)

    sheet1 = workbook.active
    sheet1.title = "Instructions"
    # https://stackoverflow.com/a/14450572
    sheet1.append(["Instructions".upper()])
    sheet1.column_dimensions["B"].width = 111.7
    sheet1["A1"].font = bold
    sheet1.merge_cells("A1:Z1")
    sheet1.append(
        [
            "",
            "This template is being provided as a tool to assist the acquisition workforce in developing an IGCE for a Firm Fixed Price Product or Service.",
        ]
    )
    sheet1.append([])
    sheet1.append(
        [
            "1.",
            "The exact amount of a vendor’s quote must NOT be used as the basis for a program office’s IGCE.",
        ]
    )
    sheet1.append(
        [
            "2.",
            "The program office must conduct all necessary research to compile an accurate and complete IGCE, independent of the vendor’s pricing/cost information.",
        ]
    )
    sheet1.append(
        [
            "3.",
            "The program office should use the results of the market reaearch to substaniate the IGCE.",
        ]
    )
    sheet1.append(
        [
            "4.",
            "The program office provide a narrative to document the basis of the IGCE.",
        ]
    )
    sheet2 = workbook.create_sheet(title="FFP IGCE")
    sheet2.append(["FFP IGCE TEMPLATE"])
    sheet2.append(["TITLE:"])
    sheet2.append(["Detailed Price Summary"])

    sheet2["A1"].font = bold
    sheet2["A2"].font = bold
    sheet2["A3"].font = bold

    sheet2.column_dimensions["A"].width = 48

    ################################################################################
    #                                                                              #
    #  Conversation with myself                                                    #
    #  ------------------------                                                    #
    #                                                                              #
    #                                                                              #
    #  Oh snap, all this Python just to                                            #
    #  put a few values into a spreadsheet                                         #
    #  without running Excel?                                                      #
    #                                                       A thousand times yes.  #
    #                                                                              #
    #                                                                              #
    #  But don't you still have to run Excel                                       #
    #  to test your output?                                                        #
    #                                                                              #
    #                                                       Soul-crushing pain     #
    #                                                       only occurs with       #
    #                                                       prolonged use of       #
    #                                                       Excel. This house      #
    #                                                       is clean.              #
    #                                                                              #
    #  What have we learned?                                                       #
    #                                                                              #
    #                                                       Python4life.           #
    #                                                                              #
    #                                                                              #
    #            No copies of Excel were harmed during the writing                 #
    #            of this code, but many expletives were used.                      #
    #                                                                              #
    ################################################################################

    column_index = 2

    count = 1
    entries = []
    for entry in item.time_set.all():
        entries.append("Estimate %s" % str(count))
        entries.append("")
        entries.append("")
        entries.append("")
        count += 1
    entries.insert(0, "Contract Line Item Description")
    sheet2.append(entries)
    sheet2["A4"].font = bold

    for cell in range(len(entries) - 1):
        # https://stackoverflow.com/a/50209914
        sheet2[
            get_column_letter(column_index + cell) + str(sheet2.max_row)
        ].fill = PatternFill(
            start_color="D3D3D3", end_color="D3D3D3", fill_type="solid"
        )

    # Merge cells
    letter_start = "B"
    merge = []
    for cell in range(len(entries) - 1):
        if (column_index + cell) % 4 == 1:
            merge.append(
                letter_start
                + str(sheet2.max_row)
                + ":"
                + get_column_letter(column_index + cell)
                + str(sheet2.max_row)
            )
            letter_start = get_column_letter(column_index + cell + 1)
    for cells in merge:
        sheet2.merge_cells(cells)

    # Bold
    sheet2[get_column_letter(column_index) + str(sheet2.max_row)].font = bold
    for cell in range(len(entries) - 1):
        if (column_index + cell) % 4 == 1:
            sheet2[
                get_column_letter(column_index + cell + 1) + str(sheet2.max_row)
            ].font = bold

    entries = []
    for entry in item.time_set.all():
        entries.append("Quantity")
        entries.append("Unit")
        entries.append("Unit Price")
        entries.append("Total Price")
    entries.insert(0, "")
    sheet2.append(entries)

    # Bold
    sheet2[get_column_letter(column_index) + str(sheet2.max_row)].font = bold
    for cell in range(len(entries) - 1):
        sheet2[
            get_column_letter(column_index + cell + 1) + str(sheet2.max_row)
        ].font = bold

    entries = []
    for entry in item.time_set.all():
        if not entry.task:
            continue
        entries.append(entry.task.name)
        entries.append(entry.description)
        entries.append(entry.hours)
        entries.append(entry.task.rate)
    entries.insert(0, "")
    sheet2.append(entries)

    for cell in range(len(entries) - 1):
        if (column_index + cell) % 4 == 1:
            sheet2[
                get_column_letter(column_index + cell) + str(sheet2.max_row)
            ].fill = PatternFill(
                start_color="D3D3D3", end_color="D3D3D3", fill_type="solid"
            )

    sheet2.append(["Line Item Subtotal"])
    for cell in range(len(entries) - 1):
        if (column_index + cell) % 4 == 1:
            sheet2[
                get_column_letter(column_index + cell) + str(sheet2.max_row)
            ].fill = PatternFill(
                start_color="D3D3D3", end_color="D3D3D3", fill_type="solid"
            )
        else:
            sheet2[
                get_column_letter(column_index + cell) + str(sheet2.max_row)
            ].fill = PatternFill(
                start_color="00008B", end_color="00008B", fill_type="solid"
            )

    sheet2.append(["Total Estimated Amount"])
    sheet2["A" + str(sheet2.max_row)].font = bold
    for cell in range(len(entries) - 1):
        if (column_index + cell) % 4 == 1:
            sheet2[
                get_column_letter(column_index + cell) + str(sheet2.max_row)
            ].fill = PatternFill(
                start_color="D3D3D3", end_color="D3D3D3", fill_type="solid"
            )
        else:
            sheet2[
                get_column_letter(column_index + cell) + str(sheet2.max_row)
            ].fill = PatternFill(
                start_color="00008B", end_color="00008B", fill_type="solid"
            )

    sheet2.append(["Total Combined Amount".upper()])
    sheet2["A" + str(sheet2.max_row)].font = bold
    for cell in range(len(entries) - 1):
        sheet2[
            get_column_letter(column_index + cell) + str(sheet2.max_row)
        ].fill = PatternFill(
            start_color="00FF00", end_color="00FF00", fill_type="solid"
        )

    # Merge cells
    letter_start = "B"
    merge = []
    for cell in range(len(entries) - 1):
        if (column_index + cell) % 4 == 1:
            merge.append(
                letter_start
                + str(sheet2.max_row)
                + ":"
                + get_column_letter(column_index + cell)
                + str(sheet2.max_row)
            )
            letter_start = get_column_letter(column_index + cell + 1)
    for cells in merge:
        sheet2.merge_cells(cells)

    sheet2.append(["Total Average Amount".upper()])
    sheet2["A" + str(sheet2.max_row)].font = bold
    for cell in range(len(entries) - 1):
        sheet2[
            get_column_letter(column_index + cell) + str(sheet2.max_row)
        ].fill = PatternFill(
            start_color="00FF00", end_color="00FF00", fill_type="solid"
        )

    sheet2.append(["Narrative:"])
    sheet2["A" + str(sheet2.max_row)].font = bold

    ################################################################################
    #                                                                              #
    #  Conversation with myself                                                    #
    #  ------------------------                                                    #
    #                                                                              #
    #  Here we go again. So you're going                                           #
    #  to write all this Python                                                    #
    #  to avoid manually entering a few cells                                      #
    #  in Excel?                                                                   #
    #                                                                              #
    #                                            My kingdom to avoid Excel!        #
    #                                                                              #
    ################################################################################

    count = 1
    for entry in item.time_set.all():
        sheet2.append(["Estimate %s—Vendor" % str(count)])
        sheet2["A" + str(sheet2.max_row)].font = bold
        sheet2.append([entry.task.name])
        sheet2.append([entry.description])
        sheet2.append([entry.hours])
        sheet2.append([entry.task.rate])
        count += 1

    response = HttpResponse(content_type="xlsx")
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    workbook.active = 1
    workbook.save(response)

    return response
