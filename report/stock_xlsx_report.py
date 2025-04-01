from odoo import models
import io
import xlsxwriter

class StockXlsxReport(models.AbstractModel):
    _name = 'stock_xlsx_report'
    _inherit = 'report.report_xlsx'

    def generate_xlsx_report(self, workbook, data, objs):
        sheet = workbook.add_worksheet("Stock Report")
        bold = workbook.add_format({'bold': True})

        # Encabezados
        headers = ["Fecha", "Referencia", "Producto", "Ubicación Origen", "Ubicación Destino", "Cantidad", "Estado"]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, bold)

        # Datos
        row = 1
        for move in data['stock_moves_data']:
            sheet.write(row, 0, str(move['date']))
            sheet.write(row, 1, move['reference'])
            sheet.write(row, 2, move['product_name'])
            sheet.write(row, 3, move['from_location'])
            sheet.write(row, 4, move['to_location'])
            sheet.write(row, 5, move['quantity'])
            sheet.write(row, 6, move['state'])
            row += 1
