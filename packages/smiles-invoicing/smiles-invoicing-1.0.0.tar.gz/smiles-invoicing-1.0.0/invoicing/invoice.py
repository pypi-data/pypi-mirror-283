import os

import pandas as pd
from fpdf import FPDF
import glob
from pathlib import Path


def generate(invoices_path: str, pdfs_path: str, image_path, product_id,
             product_name, amount_purchased, price_per_unit, total_price):
    """
    This function converts Excel invoices into PDF files
    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    filepaths = glob.glob(f'{invoices_path}/*.xlsx')
    for file in filepaths:
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()

        filename = Path(file).stem
        invoice_number, date = filename.split('-')

        pdf.set_font('Times', size=16, style='B')
        pdf.cell(w=50, h=8, txt=f'Invoice number. {invoice_number}', ln=1)

        pdf.set_font('Times', size=16, style='B')
        pdf.cell(w=50, h=8, txt=f'Date . {date}', ln=1)

        df = pd.read_excel(file, sheet_name='Sheet 1')
        # add header
        columns = [item.replace('_', ' ').title() for item in df.columns]
        pdf.set_font(family='Times', size=10, style='B')
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=60, h=8, txt=columns[1], border=1)
        pdf.cell(w=40, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        # Add rows
        for index, row in df.iterrows():
            pdf.set_font(family='Times', size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=60, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=40, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        total_sum = df['total_price'].sum()
        pdf.cell(w=30, h=8, txt='', border=1)
        pdf.cell(w=60, h=8, txt='', border=1)
        pdf.cell(w=40, h=8, txt='', border=1)
        pdf.cell(w=30, h=8, txt='', border=1)
        pdf.set_font(family='Times', size=10, style='B')
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

        pdf.set_font(family='Times', size=15, style='B')
        pdf.ln()
        pdf.cell(w=30, h=8, txt=f'The total sum is: {total_sum}', ln=1)
        pdf.cell(w=30, h=8, txt='PythonHow')
        if image_path:
            pdf.image(image_path, w=10)
        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f'{pdfs_path}/{filename}.pdf')
