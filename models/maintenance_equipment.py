from odoo import models, fields

class OpermaqEstadoEquipo(models.Model):
    _name = 'opermaq.estado.equipo'
    _description = 'Estado de Equipo Opermaq'

    name = fields.Char(string='Nombre del Estado', required=True)

    active = fields.Boolean(default=True, string='Activo')

class MaintenaceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    opermaq_cliente_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        help='Cliente al que pertenece o está asignado este equipo.'
    )

    opermaq_estado_equipo_id = fields.Many2one(
        comodel_name='opermaq.estado.equipo',
        string='Estado de Equipo',
        help='Selecciona o crea un estado para este equipo.'
    )

    maquina = fields.Char(string='Máquina')
    marca = fields.Char(string='Marca')
    medida_ruedas = fields.Char(string='Medida de Ruedas')

    alias = fields.Char(string='Alias')