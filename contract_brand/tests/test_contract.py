# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.contract.tests.test_contract import TestContractBase


class TestContract(TestContractBase):
    def setUp(self):
        super(TestContract, self).setUp()
        self.brand_id = self.env["res.brand"].create({"name": "brand"})
        self.account_receivable_type = self.env.ref(
            'account.data_account_type_receivable'
        )
        self.account_receivable_brand_default = self.env[
            'account.account'
        ].create(
            {
                'name': 'Receivable Brand Default',
                'code': 'RCV01',
                'user_type_id': self.account_receivable_type.id,
                'reconcile': True,
            }
        )
        self.partner_account_brand = self.env['res.partner.account.brand'].create(
            {
                'partner_id': self.contract.partner_id.id,
                'account_id': self.account_receivable_brand_default.id,
                'brand_id': self.brand_id.id,
                'account_type': 'receivable',
            }
        )

    def test_contract_create_branded_invoice(self):
        """ It should create a branded invoice based on the contract brand
        """
        self.contract.brand_id = self.brand_id
        invoice = self.contract.recurring_create_invoice()
        self.assertEqual(invoice.brand_id, self.brand_id)
        self.assertEqual(invoice.account_id, self.account_receivable_brand_default)

    def test_contract_analytic_account_onchange_brand(self):
        self.brand_id.analytic_account_id = self.env[
            'account.analytic.account'
        ].create({'name': 'analytic account'})
        self.contract.brand_id = self.brand_id
        self.assertFalse(
            self.contract.contract_line_ids.mapped('analytic_account_id')
        )
        self.contract._onchange_brand_id()
        self.assertEqual(
            self.contract.contract_line_ids.mapped('analytic_account_id'),
            self.brand_id.analytic_account_id,
        )
