# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResBrand(models.Model):
    _name = "res.brand"
    _inherit = ["analytic.mixin", "res.brand"]
