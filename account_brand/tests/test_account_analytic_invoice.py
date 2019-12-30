# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestAccountAnalyticInvoice(SavepointCase):
    def setUp(self):
        super(TestAccountAnalyticInvoice, self).setUp()
        self.invoice = self.env['account.invoice'].create(
            {
                'partner_id': self.env.ref('base.res_partner_12').id,
                'type': 'out_invoice',
            }
        )
        self.env['account.invoice.line'].create(
            {
                'product_id': self.env.ref('product.product_product_4').id,
                'quantity': 1,
                'price_unit': 42,
                'invoice_id': self.invoice.id,
                'name': 'something',
                'account_id': self.env['account.account']
                .create(
                    {
                        'name': 'Test sale',
                        'code': 'XX_700',
                        'user_type_id': self.env.ref(
                            'account.data_account_type_revenue'
                        ).id,
                    }
                )
                .id,
            }
        )
        self.brand_id = self.env['res.brand'].create({'name': 'Brand'})

    def test_invoice_analytic_account_onchange_brand(self):
        self.brand_id.analytic_account_id = self.env[
            'account.analytic.account'
        ].create({'name': 'analytic account'})
        self.invoice.brand_id = self.brand_id
        self.assertFalse(
            self.invoice.invoice_line_ids.mapped('account_analytic_id')
        )
        self.invoice._onchange_brand_id()
        self.assertEqual(
            self.invoice.invoice_line_ids.mapped('account_analytic_id'),
            self.brand_id.analytic_account_id,
        )
