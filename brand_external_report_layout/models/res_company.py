# Copyright 2023 Guillaume Masson <guillaume.masson@meta-it.fr>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResCompany(models.Model):

    _inherit = "res.company"

    def _get_style_vals(self):
        res = self.read(self.env["res.brand"]._get_company_overriden_fields())[0]
        res.pop("id")
        return res

    def update_style(self, vals):
        self.write(vals)
        return self
