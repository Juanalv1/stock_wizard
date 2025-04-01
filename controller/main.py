import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape

class XLSXReportController(http.Controller):

    #/**
    #  * @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    #  * 
    #  * Este controlador maneja la generación de reportes en formato XLSX. 
    #  * Cuando se hace una solicitud POST a la ruta '/xlsx_reports', se genera un archivo XLSX 
    #  * basado en el modelo especificado, las opciones proporcionadas y el formato de salida solicitado.
    #  * 
    #  * @param {string} model - El nombre del modelo de Odoo desde el cual se generará el reporte.
    #  * @param {string} options - Las opciones que se pasarán al reporte. Este valor debe estar en formato JSON.
    #  * @param {string} output_format - El formato de salida del reporte. Este valor debe ser 'xlsx' para generar un archivo Excel.
    #  * @param {string} report_name - El nombre que se le asignará al archivo generado.
    #  * @param {Object} kw - Cualquier parámetro adicional que sea proporcionado en la solicitud.
    #  * 
    #  * @returns {http.Response} - Devuelve una respuesta con el archivo XLSX generado, si se ha generado correctamente.
    #  * 
    #  * @throws {Exception} - Si ocurre un error en la generación del reporte, se devuelve una respuesta con el mensaje de error.
    #  * 
    #  * @example
    #  * // Llamada al controlador desde el frontend (por ejemplo, en JavaScript).
    #  * const response = await fetch('/xlsx_reports', {
    #  *     method: 'POST',
    #  *     body: JSON.stringify({
    #  *         model: 'stock.wizard',
    #  *         options: '[{"date": "2025-04-01", "reference": "WH/IN/00002"}]',
    #  *         output_format: 'xlsx',
    #  *         report_name: 'Stock Report'
    #  *     }),
    #  * });
    
    #  */
    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def generate_xlsx_report(self, model, options, output_format, report_name, **kw):

        uid = request.session.uid
        try:
            report_obj = request.env[model].with_user(uid)
            options = json.loads(options)


            if output_format == 'xlsx':
                # Generar el reporte XLSX
                response = request.make_response(
                    None, headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition(report_name + '.xlsx')),
                    ]
                )
                report_obj.get_xlsx_report(options, response)
                return response
        except Exception as e:
            se = http.serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))
