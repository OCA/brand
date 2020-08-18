# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'res.brand.mixin']

    brand_id = fields.Many2one(
        states={
            'sent': [('readonly', True)],
            'sale': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)],
        }
    )

    @api.multi
    def _prepare_invoice(self):
        for order in self:
            invoice_vals = super(SaleOrder, order)._prepare_invoice()
            invoice_vals.update({
                'brand_id': order.brand_id.id,
            })
        return invoice_vals

    @api.onchange('team_id')
    def _onchange_team_id(self):
        self.brand_id = self.team_id.brand_id

    brand_name = fields.Many2one(
        comodel_name="res.brand.name",
        string="Template",
        help="Ce template sera utilisé pour ce document",
    )

    @api.onchange('brand_name')
    def _onchange_brand_name(self):
        self.brand_id = self.brand_name.brand
