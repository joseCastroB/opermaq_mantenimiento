from odoo import models, fields, api

class OpermaqEstadoSolicitud(models.Model):
    _name = 'opermaq.estado.solicitud'
    _description = 'Estados en el tiempo de la Solicitud'

    name = fields.Char(string='Descripción', compute='_compute_name', store=True)
    
    # 1. LA CONEXIÓN: A qué solicitud pertenece este bloque de tiempo
    request_id = fields.Many2one('maintenance.request', string='Solicitud de Mantenimiento', required=True, ondelete='cascade')
    
    # Traemos el equipo automáticamente por si lo queremos ver en la pantalla
    equipment_id = fields.Many2one('maintenance.equipment', related='request_id.equipment_id', string='Equipo', store=True)
    
    # ==========================================
    # NUEVOS CAMPOS RELACIONADOS PARA LA LISTA
    # ==========================================
    # Jalamos la orden de compra desde la Solicitud
    opermaq_orden_compra_id = fields.Many2one(related='request_id.opermaq_orden_compra_id', string='Orden de Compra')
    
    # Jalamos los datos técnicos desde la ficha del Equipo
    ubicacion = fields.Char(related='equipment_id.location', string='Ubicación')
    serie = fields.Char(related='equipment_id.serial_no', string='Serie')
    modelo = fields.Char(related='equipment_id.model', string='Modelo')
    cliente_id = fields.Many2one('res.partner', related='equipment_id.partner_id', string='Cliente')
    # ==========================================

    # Estado físico del equipo (Para la vista de Propio)
    opermaq_estado_equipo_id = fields.Many2one('opermaq.estado.equipo', related='equipment_id.opermaq_estado_equipo_id', string='Estado Físico del Equipo')

    # 2. LAS VARIABLES DEL GANTT: Estado, Fechas y Color
    # ==========================================
    # EL TRUCO: Dejamos el campo antiguo pero NO obligatorio
    # para que la base de datos quite el candado y no bloquee
    estado_gantt_id = fields.Many2one('opermaq.estado.gantt', string='Estado en Gantt', required=True)
    # ==========================================
    
    # NUEVO: Jalamos el color automáticamente desde el Estado de Gantt
    color_gantt_hex = fields.Char(related='estado_gantt_id.color_hex', string='Color de Barra')
    color_gantt = fields.Integer(related='estado_gantt_id.color', store=True, string='Color Automático')

    estado_id = fields.Many2one('opermaq.estado.equipo', string='Estado Antiguo (Ignorar)', required=False)

    horometro = fields.Float(string='Horómetro', help="Registro de las horas de la máquina")

    fecha_inicio = fields.Datetime(string='Fecha Inicio', required=True)
    fecha_fin = fields.Datetime(string='Fecha Fin', required=True)
    color = fields.Char(string='Color', default='#00A09D')

    # Traemos el tipo (Cliente/Propio) de la solicitud matriz para poder filtrar los menús
    tipo_preventivo = fields.Selection(
        related='request_id.opermaq_tipo_preventivo', 
        store=True, 
        string='Tipo de Preventivo'
    )

    # NUEVO CAMPO: Ayudará a filtrar el desplegable
    vista_actual = fields.Selection(
        selection=[('cliente', 'Cliente'), ('propio', 'Propio')],
        string='Vista Actual'
    )

    @api.depends('request_id', 'estado_gantt_id')
    def _compute_name(self):
        for record in self:
            solicitud = record.request_id.name if record.request_id else 'Sin Solicitud'
            # Actualizado para usar el nuevo campo
            estado = record.estado_gantt_id.name if record.estado_gantt_id else 'Sin Estado'
            record.name = f"{solicitud} - {estado}"