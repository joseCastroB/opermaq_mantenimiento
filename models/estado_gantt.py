from odoo import models, fields

class OpermaqEstadoGantt(models.Model):
    _name = 'opermaq.estado.gantt'
    _description = 'Estado para el Planificador Gantt'

    name = fields.Char(string='Nombre del Estado', required=True)

    color = fields.Integer(string='Color')

    color_hex = fields.Char(string='Color', default='#00A09D')