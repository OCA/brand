# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleTimesheetBrand(TransactionCase):
    def setUp(self):
        super().setUp()
        self.env = self.env(context=dict(self.env.context, tracking_disable=True))
        self.Product = self.env["product.product"]
        self.main_company = self.env.ref("base.main_company")
        self.customer = self.env.ref("base.res_partner_12")
        self.product = self.Product.create(
            {
                "name": "test",
                "type": "service",
                "service_tracking": "task_in_project",
            }
        )
        self.project = self.env["project.project"].create(
            {
                "name": "Pigs",
                "privacy_visibility": "employees",
                "alias_name": "project+pigs",
                "company_id": self.main_company.id,
            }
        )
        self.brand = self.env["res.brand"].create(
            {
                "partner_id": self.env.user.partner_id.id,
            }
        )

    def test_confirm_so_create_task(self):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.customer.id,
                "brand_id": self.brand.id,
                "project_id": self.project.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 2.0,
                        },
                    )
                ],
            }
        )
        sale_order.action_confirm()
        self.assertEqual(sale_order.tasks_count, 1)
        self.assertEqual(sale_order.tasks_ids[0].brand_id.id, self.brand.id)
