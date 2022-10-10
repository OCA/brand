# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ["account.move", "res.brand.mixin"]

    brand_id = fields.Many2one(
        states={
            "open": [("readonly", True)],
            "in_payment": [("readonly", True)],
            "paid": [("readonly", True)],
            "cancel": [("readonly", True)],
        }
    )

    def _is_brand_required(self):
        self.ensure_one()
        if self.move_type in ("in_invoice", "in_refund"):
            return False
        return super()._is_brand_required()

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        res = super()._onchange_partner_id()
        if self.brand_id:
            pab_model = self.env["res.partner.account.brand"]
            company_id = self.company_id.id
            partner = (
                self.partner_id
                if not company_id
                else self.partner_id.with_company(company_id)
            )
            invoice_type = self.move_type or self.env.context.get(
                "move_type", "out_invoice"
            )
            if partner:
                rec_account = pab_model._get_partner_account_by_brand(
                    "asset_receivable", self.brand_id, partner
                )
                rec_account = (
                    rec_account
                    if rec_account
                    else partner.property_account_receivable_id
                )
                pay_account = pab_model._get_partner_account_by_brand(
                    "liability_payable", self.brand_id, partner
                )
                pay_account = (
                    pay_account if pay_account else partner.property_account_payable_id
                )
                if invoice_type in ("in_invoice", "in_refund"):
                    account_id = pay_account
                else:
                    account_id = rec_account
                if account_id:
                    self.line_ids.filtered(
                        lambda l, a=account_id: l.account_id.account_type
                        == a.account_type
                    ).update({"account_id": account_id.id})
        return res
