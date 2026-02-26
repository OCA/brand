# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import TransactionCase


class TestSaleOrderLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand = cls.env["res.brand"].create(
            {
                "name": "Brand",
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
            }
        )
        cls.plan = cls.env["account.analytic.plan"].create(
            {
                "name": "Test Plan",
            }
        )
        cls.plan2 = cls.env["account.analytic.plan"].create(
            {
                "name": "Test Plan 2",
            }
        )
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "Test Analytic Account",
                "plan_id": cls.plan.id,
            }
        )
        cls.analytic_account2 = cls.env["account.analytic.account"].create(
            {
                "name": "Test Analytic Account 2",
                "plan_id": cls.plan2.id,
            }
        )
        cls.product = cls.env.ref("product.product_product_1")
        cls.analytic_distribution_model = cls.env[
            "account.analytic.distribution.model"
        ].create(
            {
                "brand_id": cls.brand.id,
                "analytic_distribution": {str(cls.analytic_account.id): 100.0},
            }
        )

    def test_analytic_on_sale_order_line(self):
        self.order.brand_id = self.brand
        self.order.order_line = [Command.create({"product_id": self.product.id})]
        self.assertEqual(
            self.order.order_line.analytic_distribution,
            self.analytic_distribution_model.analytic_distribution,
        )

    def test_set_brand_on_existing_order(self):
        self.order.order_line = [Command.create({"product_id": self.product.id})]
        self.assertFalse(self.order.order_line.analytic_distribution)
        self.order.brand_id = self.brand
        self.assertEqual(
            self.order.order_line.analytic_distribution,
            self.analytic_distribution_model.analytic_distribution,
        )

    def test_combine_analytic_with_product(self):
        self.env["account.analytic.distribution.model"].create(
            {
                "product_id": self.product.id,
                "analytic_distribution": {str(self.analytic_account2.id): 100.0},
            }
        )
        self.order.brand_id = self.brand
        self.order.order_line = [Command.create({"product_id": self.product.id})]
        self.assertEqual(
            self.order.order_line.analytic_distribution,
            {
                str(self.analytic_account.id): 100.0,
                str(self.analytic_account2.id): 100.0,
            },
        )
