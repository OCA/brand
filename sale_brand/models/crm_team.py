# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = "crm.team"

    brand_id = fields.Many2one(comodel_name="res.brand", string="Brand")
