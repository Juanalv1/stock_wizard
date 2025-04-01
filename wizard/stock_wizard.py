from odoo import fields, models, api
from datetime import date, timedelta
import calendar


class StockWizard(models.TransientModel):
    _name = 'stock.wizard'
    _description = 'Stock Wizard'

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

    fecha_inicio = fields.Date(
        string="Fecha Inicio", default=_default_fecha_inicio)
    fecha_fin = fields.Date(string="Fecha Fin", default=_default_fecha_fin)
    compania = fields.Many2one("res.company", string="Compañía")
    almacen = fields.Many2one("stock.location", string="Almacén")
    productos = fields.Many2one("product.product", string="Producto")
