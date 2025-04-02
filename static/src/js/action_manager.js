/** @odoo-module **/

/** 
 * @odoo-module
 * @module stock_wizard.action_manager
 * 
 * Action Manager para la descarga de reportes en formato XLSX en el backend de Odoo.
 * 
 * Esta acción se maneja cuando el tipo de reporte es "xlsx". Al activar la acción, se realiza una solicitud
 * al servidor para descargar el reporte de movimientos de stock en formato XLSX.
 
 * @param {Object} action - La acción que se está ejecutando en el frontend de Odoo.
 * @param {string} action.report_type - El tipo de reporte. En este caso, se espera "xlsx".
 * @param {Object} action.data - Los datos que se pasan junto con la acción, que contienen la información para generar el reporte.
 * 
 * @throws {Error} Si ocurre algún error durante la descarga del reporte, se registra en la consola.
 */
import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";

registry.category("ir.actions.report handlers").add("xlsx", async (action) => {
    // Verificar que el tipo de reporte sea "xlsx"
    if (action.report_type === "xlsx") {
        try {
            // Realizar la solicitud para descargar el reporte XLSX
            await download({
                url: '/xlsx_reports',  // URL del controlador que genera el reporte
                data: {
                    model: action.model,  // Modelo de los datos que se deben incluir en el reporte
                    options: JSON.stringify(action.data),  // Datos del reporte serializados en formato JSON
                    output_format: 'xlsx',  // Formato de salida del reporte
                    report_name: action.report_name,  // Nombre del reporte generado
                },
            });
        } catch (error) {
            // Manejo de errores si la descarga falla
            console.error("Error al descargar el reporte XLSX:", error);
        } finally {
        }
    }
});
