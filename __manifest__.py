{
    'name': 'Opermaq Mantenimiento',
    'version': '1.0',
    'summary': 'Personalizaciones de mantenimiento para Opermaq',
    'category': 'Maintenance',
    'depends': ['maintenance', 'purchase', 'web_timeline'], 
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_equipment_views.xml',
        'views/maintenance_request_views.xml',
        'views/estado_gantt_views.xml',
        'views/estado_solicitud_views.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}