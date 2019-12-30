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

    @api.onchange('brand_id', 'invoice_line_ids')
    def _onchange_brand_id(self):
        res = super()._onchange_brand_id()
        for invoice in self:
            if invoice.state == 'draft' and invoice.brand_id:
                account_analytic = invoice.brand_id.analytic_account_id
                invoice.invoice_line_ids.update(
                    {'account_analytic_id': account_analytic.id}
                )
        return res

    @api.multi
    def _is_brand_required(self):
        self.ensure_one()
        if self.type in ('in_invoice', 'in_refund'):
            return False
        return super(AccountInvoice, self)._is_brand_required()

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None,
                        description=None, journal_id=None):
        values = super(AccountInvoice, self)._prepare_refund(
            invoice, date_invoice=date_invoice, date=date,
            description=description, journal_id=journal_id)
        if invoice.brand_id:
            values['brand_id'] = invoice.brand_id.id
        return values
