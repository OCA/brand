# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from typing import ClassVar

from odoo import api, fields, models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit: ClassVar = ["sale.order", "res.brand.mixin"]

    brand_id = fields.Many2one()

    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super()._prepare_invoice()
        invoice_vals["brand_id"] = self.brand_id.id
        return invoice_vals

    def _get_invoice_grouping_keys(self):
        return super()._get_invoice_grouping_keys() + ["brand_id"]

    @api.onchange("team_id")
    def _onchange_team_id(self):
        if self.team_id.brand_id:
            self.brand_id = self.team_id.brand_id

    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        if res.get("team_id", False) and not res.get("brand_id", False):
            team = self.env["crm.team"].browse(res["team_id"])
            res["brand_id"] = team.brand_id.id

        return res
