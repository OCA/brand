# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResBrand(models.Model):

    _inherit = "res.brand"

    partner_bank_id = fields.Many2one(
        comodel_name="res.partner.bank",
        domain="[('partner_id.ref_company_ids', 'in', [company_id])]",
        string="Bank Account",
        description="Company Bank Account Number to which the invoices of this "
        "brand will be paid (for Customer Invoice and Vendor Credit Note)",
    )

    @api.constrains("company_id", "partner_bank_id")
    def validate_partner_bank_id(self):
        for record in self:
            if (
                record.partner_bank_id
                and not record.company_id
                in record.partner_bank_id.partner_id.ref_company_ids
            ):
                raise ValidationError(
                    _(
                        "The account selected for invoices payment does not "
                        "belong to the same company as this brand."
                    )
                )
