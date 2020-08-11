# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice', 'res.brand.mixin']

    brand_id = fields.Many2one(
        states={
            'open': [('readonly', True)],
            'in_payment': [('readonly', True)],
            'paid': [('readonly', True)],
            'cancel': [('readonly', True)],
        }
    )

    @api.constrains('brand_id', 'company_id')
    def _check_brand_requirement(self):
        out_invoices = self.filtered(
            lambda l: l.type in ('out_invoice', 'out_refund')
        )
        return super(AccountInvoice, out_invoices)._check_brand_requirement()
