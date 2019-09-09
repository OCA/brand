# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.contract.tests.test_contract import TestContractBase


class TestContract(TestContractBase):
    def setUp(self):
        super(TestContract, self).setUp()
        self.brand_id = self.env["res.brand"].create({"name": "brand"})

    def test_contract_create_branded_invoice(self):
        """ It should create a branded invoice based on the contract brand
        """
        self.contract.brand_id = self.brand_id
        invoice = self.contract.recurring_create_invoice()
        self.assertEqual(invoice.brand_id, self.brand_id)
