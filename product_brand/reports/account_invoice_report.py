# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    product_brand_id = fields.Many2one(comodel_name="product.brand", string="Brand")

    @api.model
    def _select(self):
        select_str = super()._select().code
        select_str += """
            , template.product_brand_id as product_brand_id
            """
        return SQL(select_str)

    @api.model
    def _group_by(self):
        group_by_str = super()._group_by().code
        group_by_str += ", template.product_brand_id"
        return SQL(group_by_str)
