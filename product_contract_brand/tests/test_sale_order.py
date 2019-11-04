# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.product_contract.tests.test_sale_order import (
    TestSaleOrder as TestContractSaleOrder,
)


class TestSaleOrder(TestContractSaleOrder):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.brand_id = self.env["res.brand"].create({"name": "brand"})

    def test_action_confirm_branded_sale(self):
        """ It should create a branded contract based on the sale order brand
        """
        self.sale.brand_id = self.brand_id
        self.sale.action_confirm()
        self.assertEqual(self.order_line1.contract_id.brand_id, self.brand_id)
