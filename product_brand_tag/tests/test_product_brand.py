# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from psycopg2 import IntegrityError

from odoo.tools import mute_logger

from odoo.addons.product_brand.tests.common import CommonCase


class TestBrandTags(CommonCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_brand2 = cls.product_brand.copy({"name": "Test Brand 2"})
        cls.tag = cls.env["product.brand.tag"].create(
            {
                "name": "Test Tag",
                "product_brand_ids": [
                    (6, 0, [cls.product_brand.id, cls.product_brand2.id])
                ],
            }
        )

    def test_brand_rel(self):
        self.assertEqual(self.product_brand.tag_ids, self.tag)
        self.assertEqual(self.product_brand2.tag_ids, self.tag)

    def test_count(self):
        self.assertEqual(self.tag.brands_count, 2)
        self.tag.product_brand_ids -= self.product_brand2
        self.assertEqual(self.tag.brands_count, 1)

    def test_code(self):
        self.assertEqual(self.tag.code, "test-tag")
        self.tag.code = "SomeThing wëird!"
        self.assertEqual(self.tag.code, "something-weird")

    @mute_logger("odoo.sql_db")
    def test_product_template_tag_uniq(self):
        with self.assertRaises(IntegrityError):
            with self.cr.savepoint():
                self.env["product.brand.tag"].create({"name": "Test Tag"})

        self.env["product.brand.tag"].create(
            {
                "name": "Test Tag",
                "company_id": self.env.company.create({"name": "Foo"}).id,
            }
        )
