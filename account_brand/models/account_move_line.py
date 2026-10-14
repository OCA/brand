# Copyright 2026 Juliano Henriquez <juliano@consultoriahenca.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _compute_account_id(self):
        result = super()._compute_account_id()
        for line in self.filtered(
            lambda line: line.display_type == "payment_term" and line.move_id.brand_id
        ):
            move = line.move_id
            account_type = (
                "asset_receivable"
                if move.is_sale_document(include_receipts=True)
                else "liability_payable"
            )
            account = (
                self.env["res.partner.account.brand"]
                .with_company(move.company_id)
                ._get_partner_account_by_brand(
                    account_type, move.brand_id, move.commercial_partner_id
                )
            )
            if account:
                line.account_id = move.fiscal_position_id.map_account(account)
        return result
