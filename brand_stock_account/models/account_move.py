# Copyright 2022 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _fill_brand_id(self, values):
        values = values.copy()
        if "brand_id" not in values and "stock_move_id" in values:
            stock_move = self.env["stock.move"].browse(values.get("stock_move_id"))
            if stock_move.picking_id.sale_id.brand_id:
                values.update({"brand_id": stock_move.picking_id.sale_id.brand_id.id})
        return values

    @api.model_create_multi
    def create(self, vals_list):
        """

        :param vals_list: list of dict
        :return: self recordset
        """
        # FIXME:
        # We intercept the creation of the account.move to add the brand
        # due to non-inheritable code in `stock.move, _create_account_move_line`
        list_vals = [self._fill_brand_id(vals) for vals in vals_list]
        return super().create(list_vals)
