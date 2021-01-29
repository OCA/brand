# Copyright 2021 Yves Goldberg
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Crm Brand',
    'description': """
        Add brand to CRM""",
    'version': '13.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Yves Goldberg',
    'website': 'https://www.ygol.com',
    'depends': ['brand', 'crm'
                ],
    'data': [
        'views/crm_lead.xml',
        'views/crm_team.xml',
    ],
    'demo': [
    ],
}
