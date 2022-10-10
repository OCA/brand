# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "res.brand.mixin"]

    brand_id = fields.Many2one(
        states={
            "sent": [("readonly", True)],
            "sale": [("readonly", True)],
            "done": [("readonly", True)],
            "cancel": [("readonly", True)],
        }
    )

    def _prepare_invoice(self):
        invoice_vals = {}
        for order in self:
            invoice_vals = super(SaleOrder, order)._prepare_invoice()
            invoice_vals.update({"brand_id": order.brand_id.id})
        return invoice_vals

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
