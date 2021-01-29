# Copyright 2021 Yves Goldberg
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CrmTeam(models.Model):

    _name = 'crm.team'
    _inherit = ['crm.team', 'res.brand.mixin']

    brand_id = fields.Many2one(
        comodel_name='res.brand',
        string='Brand'
    )
