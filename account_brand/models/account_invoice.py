# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


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
    brand_name = fields.Many2one(
        comodel_name="res.brand.name",
        string="Template",
        help="Ce template sera utilisé pour ce document",
    )

    @api.onchange('brand_name')
    def _onchange_brand_name(self):
        self.brand_id = self.brand_name.brand
