from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    name = fields.Char(default='Autogenerado al guardar...', required=False, readonly=True)

    titulo = fields.Char(string='Título', tracking=True)

    equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Equipo',
        required=True,
        help='Es obligatorio seleccionar un equipo para generar la solicitud.'
    )

    opermaq_orden_compra_id = fields.Many2one(
        comodel_name='sale.order',
        string='Orden de Compra',
        domain="[('state', 'in', ['draft', 'sent', 'sale'])]", # Solo muestra cotizaciones en borrador o enviadas
        help='Selecciona la solicitud de cotización de venta relacionada a este mantenimiento.'
    )

    opermaq_tipo_preventivo = fields.Selection(
        selection=[
            ('cliente', 'Mantenimiento preventivo Cliente'),
            ('propio', 'mantenimiento preventivo Propio')
        ],
        string='Tipo de Preventivo',
        help='Indica si el preventivo es para un cliente o para un equipo propio.'
    )

    opermaq_estado_id = fields.Many2one(
        comodel_name='opermaq.estado.equipo',
        string='Estado Asignado'
    )

    opermaq_color = fields.Char(
        string='Color de la barra',
        default='#00A09D'
    )

    opermaq_fecha_inicio = fields.Datetime(
        string='Fecha de Inicio',
        help='Indica cuándo comienza la asignación del equipo.'
    )

    opermaq_fecha_fin = fields.Datetime(
        string='Fecha de Fin',
        help='Indica cuándo termina la asignación del equipo.'
    )

    # RESTRICCIÓN: Evitar duplicados del mismo equipo en curso
    @api.constrains('equipment_id')
    def _check_solicitud_unica_por_equipo(self):
        for record in self:
            if record.equipment_id:
                solicitud_duplicada = self.env['maintenance.request'].search([
                    ('equipment_id', '=', record.equipment_id.id),
                    ('id', '!=', record.id),
                    ('stage_id.done', '=', False)
                ], limit=1)
                
                if solicitud_duplicada:
                    raise ValidationError(f"¡Alto! El equipo '{record.equipment_id.name}' ya tiene una solicitud de mantenimiento en curso. Por favor, finaliza o cancela la anterior antes de crear una nueva.")

    # =========================================================
    # GENERADOR DE NOMBRES (Ahora asume que el equipo siempre existe)
    # =========================================================
    @api.model_create_multi
    def create(self, vals_list):
        # Primero dejamos que Odoo guarde el registro (así valida que el equipo esté lleno)
        records = super(MaintenanceRequest, self).create(vals_list)
        
        # Luego le ponemos el nombre correcto a cada registro creado
        for record in records:
            fecha_hoy = fields.Date.context_today(record).strftime('%d-%m-%Y')
            equipo_name = record.equipment_id.name or 'Sin equipo'
            modelo = record.equipment_id.model or 'Sin modelo'
            serie = record.equipment_id.serial_no or 'Sin serie'
            record.name = f"{equipo_name} / {modelo} / {serie}"
            
        return records

    def write(self, vals):
        res = super(MaintenanceRequest, self).write(vals)
        # Solo re-generamos el nombre si el usuario edita y cambia el equipo
        if 'equipment_id' in vals:
            for record in self:
                fecha_hoy = fields.Date.context_today(record).strftime('%d-%m-%Y')
                equipo_name = record.equipment_id.name or 'Sin equipo'
                modelo = record.equipment_id.model or 'Sin modelo'
                serie = record.equipment_id.serial_no or 'Sin serie'
                record.name = f"{equipo_name} / {modelo} / {serie}"
        return res