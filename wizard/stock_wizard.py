from datetime import date, timedelta
from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools import date_utils
import calendar
import json
import io
import xlsxwriter


class StockWizard(models.TransientModel):
    _name = 'stock.wizard'
    _description = 'Stock Wizard'
    name = fields.Char(string="Nombre", help="Nombre del informe.", default="Informe de Stock")

    @api.model
    def _default_fecha_inicio(self):
        # Retorna el primer día del mes en curso.
        today = date.today()
        return today.replace(day=1)

    @api.model
    def _default_fecha_fin(self):
        # Retorna el último día del mes en curso.
        today = date.today()
        ultimo_dia = calendar.monthrange(today.year, today.month)[1]
        return today.replace(day=ultimo_dia)

    fecha_inicio = fields.Date(string="Fecha Inicio", default=_default_fecha_inicio, help="Fecha de inicio del periodo a consultar.")
    fecha_fin = fields.Date(string="Fecha Fin", default=_default_fecha_fin, help="Fecha de fin del periodo a consultar.")   
    compania = fields.Many2one("res.company", string="Compañía", help="Compañía a consultar.", default=lambda self: self.env.company)
    almacen_relacionado = fields.Many2one("stock.warehouse", string="Almacén", help="Almacén a consultar.", default=lambda self: self.env['stock.warehouse'].search([], limit=1))
    product = fields.Many2one("product.product", string="Producto", help="Producto a consultar.", default=lambda self: self.env['product.product'].search([], limit=1))
    report_type = fields.Selection([
        ('pdf', 'PDF'),
        ('xlsx', 'XLSX')
    ], string="Formato del reporte", default='pdf', help="Formato del reporte a generar.", required=True)

    def generate_report(self):
        domain = [
            ('date', '>=', self.fecha_inicio),
            ('date', '<=', self.fecha_fin),
            ('company_id', '=', self.compania.id),
            ('product_id', '=', self.product.id),
            '|',
            ('location_id.warehouse_id', '=', self.almacen_relacionado.id),
            ('location_dest_id.warehouse_id', '=', self.almacen_relacionado.id),

        ] 
        # Buscar en stock.move.line los registros dentro del rango de fechas
        stock_moves = self.env['stock.move.line'].search(domain)
        stock_moves_data = []

        for move in stock_moves:
            # Obtener los datos necesarios de cada movimiento
            move_data = {
                'date': move.date,
                'reference': move.reference,
                'product_name': move.product_id.name,
                'from_location': move.location_id.display_name,
                'to_location': move.location_dest_id.display_name,
                'quantity': move.quantity,
            }
            stock_moves_data.append(move_data)
            
        if self.report_type =='pdf':
            return self.env.ref('stock_wizard.action_report_stock_pdf').report_action(self, data={'stock_moves_data': stock_moves_data})
        elif self.report_type == 'xlsx':
            return {
                'type': 'ir.actions.report',
                'data': {
                    'model': 'stock.wizard',
                    'options': json.dumps(stock_moves_data, default=str),
                    'output_format': 'xlsx',
                    'report_name': 'Stock Report'
                },
                'report_type': 'xlsx',
            }
        
    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Stock Report")
        bold = workbook.add_format({'bold': True})
        header_format = workbook.add_format({
            'bg_color': '#0000FF',  # Azul
            'color': 'white',       # Blanco
            'border': 1,            # Borde de las celdas
            'align': 'center',      # Centrado
            'valign': 'vcenter',     # Centrado vertical
            'bold': 'True'
        })
        # Encabezados
        headers = ["Fecha", "Referencia", "Producto", "Ubicación Origen", "Ubicación Destino", "Cantidad"]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format )

        # Datos
        row = 1
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 50)
        sheet.set_column('E:E', 50)
        sheet.set_column('F:F', 10)

        
        stock_moves_data = json.loads(data['options'])
        for move in stock_moves_data:
            sheet.write(row, 0, str(move.get('date', '')))
            sheet.write(row, 1, move.get('reference', ''))
            sheet.write(row, 2, move.get('product_name', ''))
            sheet.write(row, 3, move.get('from_location', ''))
            sheet.write(row, 4, move.get('to_location', ''))
            sheet.write(row, 5, move.get('quantity', ''))
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


        
        



        




