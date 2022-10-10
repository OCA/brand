# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerAccountBrand(models.Model):
    """This model is meant to be used in case we need to define different
    receivable/payable accounts for partners"""

    _name = "res.partner.account.brand"
    _description = "Receivable/Payable Partner Account By Brand"

    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", required=False
    )
    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        required=True,
        domain="[('account_type', 'in', ('liability_payable', 'asset_receivable'))]",
    )
    brand_id = fields.Many2one(comodel_name="res.brand", string="Brand", required=True)
    account_type = fields.Selection(
        string="Type",
        selection=[
            ("liability_payable", "Payable"),
            ("asset_receivable", "Receivable"),
        ],
        required=True,
    )

    _sql_constraints = [
        (
            "unique_account_by_partner",
            "unique(partner_id, account_id, brand_id, account_type)",
            _("Partner has already an account set for this brand!"),
        )
    ]

    @api.constrains("account_id", "account_type")
    def _check_account_type(self):
        for rec in self:
            if (
                rec.account_id
                and rec.account_type
                and rec.account_id.account_type != rec.account_type
            ):
                raise ValidationError(
                    _("Please select an account of type %s") % rec.account_type
                )

    @api.onchange("account_type")
    def _onchange_account_type(self):
        self.ensure_one()
        self.update({"account_id": False})
        domain = [("id", "=", False)]
        if self.account_type == "payable":
            domain = [
                ("internal_type", "=", "payable"),
                ("deprecated", "=", False),
            ]
        elif self.account_type == "receivable":
            domain = [
                ("internal_type", "=", "receivable"),
                ("deprecated", "=", False),
            ]
        return {"domain": {"account_id": domain}}

    @api.model
    def _get_partner_account_by_brand(self, account_type, brand, partner):
        domain = [
            ("brand_id", "=", brand.id),
            ("account_type", "=", account_type),
        ]
        default_rule = self.search(domain + [("partner_id", "=", False)], limit=1)
        partner_rule = False
        if partner:
            partner_rule = self.search(domain + [("partner_id", "=", partner.id)])
        return partner_rule.account_id if partner_rule else default_rule.account_id
