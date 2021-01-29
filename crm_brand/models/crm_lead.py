# Copyright 2021 Yves Goldberg
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CrmLead(models.Model):

    _name = "crm.lead"
    _inherit = 'crm.lead'

    brand_id = fields.Many2one(related='team_id.brand_id')
