# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.addons.product_brand.tests.common import CommonCase


class TestBrandCompanies(CommonCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company1 = cls.env["res.company"].create({"name": "ACME Inc."})
        cls.company2 = cls.env["res.company"].create({"name": "Umbrella Corp."})
        cls.env.user.company_ids += cls.company1 + cls.company2
        cls.user = cls.env.ref("base.user_demo")
        cls.product_brand2 = cls.product_brand.copy({"name": "Test Brand 2"})

    def _test_find_records(self, user, count):
        records = self.product_brand_obj.with_user(user).search([])
        self.assertEqual(len(records), count)
        return records

    def test_user_simple_default(self):
        records = self._test_find_records(self.user, 2)
        self.assertIn(self.product_brand, records)
        self.assertIn(self.product_brand2, records)

    def test_user_simple_company_set_1(self):
        # Assign a company to a brand, user has none of these companies
        self.product_brand.company_ids += self.company1
        records = self._test_find_records(self.user, 1)
        self.assertIn(self.product_brand2, records)

    def test_user_simple_company_set_2(self):
        # Assign a company to both brands
        self.product_brand.company_ids += self.company1
        self.product_brand2.company_ids += self.company2
        self._test_find_records(self.user, 0)

    def test_user_simple_company_set_3(self):
        # Assign a company to both brands
        self.product_brand.company_ids += self.company1
        self.product_brand2.company_ids += self.company2
        # Assign a company to the user
        self.user.company_ids += self.company1
        records = self._test_find_records(self.user, 1)
        self.assertIn(self.product_brand, records)

    def test_user_simple_company_set_4(self):
        # Assign a company to both brands
        self.product_brand.company_ids += self.company1
        self.product_brand2.company_ids += self.company2
        # Assign both companies to the user
        self.user.company_ids += self.company1
        self.user.company_ids += self.company2
        records = self._test_find_records(self.user, 2)
        self.assertIn(self.product_brand, records)
        self.assertIn(self.product_brand2, records)
