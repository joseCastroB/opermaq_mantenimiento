from odoo import models, fields

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    opermaq_orden_compra_id = fields.Many2one(
        comodel_name='purchase.order',
        string='Orden de Compra',
        help='Selecciona la orden de compra relacionada a este mantenimiento.'
    )

    opermaq_tipo_preventivo = fields.Selection(
        selection=[
            ('cliente', 'Mantenimiento preventivo Cliente'),
            ('propio', 'mantenimiento preventivo Propio')
        ],
        string='Tipo de Preventivo',
        help='Indica si el preventivo es para un cliente o para un equipo propio.'
    )