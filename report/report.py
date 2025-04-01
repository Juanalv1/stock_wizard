from odoo import api, models

class StockWizardReport(models.AbstractModel):
    _name = 'report.stock_wizard.stock_pdf_report_template'
    _description = 'Stock Wizard Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Asegurar que data contiene stock_moves_data
        stock_moves_data = data.get('stock_moves_data', []) if data else []

        return {
            'doc_ids': docids,
            'doc_model': 'stock.wizard',
            'docs': stock_moves_data,  # Enviamos los datos al template
        }
