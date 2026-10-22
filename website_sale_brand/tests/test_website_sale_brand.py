# Copyright 2026 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from odoo.addons.website.tools import MockRequest


class TestWebsiteSaleBrand(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand_company = cls.env.ref("base.main_company")
        cls.brand1 = cls.env["res.brand"].create(
            {
                "name": "Brand 1",
                "company_id": cls.brand_company.id,
            }
        )
        cls.brand2 = cls.env["res.brand"].create(
            {
                "name": "Brand 2",
                "company_id": cls.brand_company.id,
            }
        )

        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})

        cls.team = cls.env["crm.team"].create(
            {
                "name": "Sales Team with Brand",
                "brand_id": cls.brand1.id,
            }
        )

        # Set company brand requirement to required
        cls.brand_company.brand_use_level = "required"

    def test_website_with_brand(self):
        """It should set the brand from the website directly when no team brand"""
        website = self.env["website"].create(
            {
                "name": "Website with Brand",
                "company_id": self.brand_company.id,
                "brand_id": self.brand2.id,
                "salesteam_id": False,
            }
        )
        with MockRequest(self.env, website=website):
            vals = website._prepare_sale_order_values(self.partner)
        self.assertEqual(vals.get("brand_id"), self.brand2.id)
        order = self.env["sale.order"].create(vals)
        self.assertEqual(order.brand_id, self.brand2)

    def test_website_with_team_brand_precedence(self):
        """It should prioritize sales team brand over website brand"""
        website = self.env["website"].create(
            {
                "name": "Website with Brand and Team",
                "company_id": self.brand_company.id,
                "brand_id": self.brand2.id,
                "salesteam_id": self.team.id,
            }
        )
        with MockRequest(self.env, website=website):
            vals = website._prepare_sale_order_values(self.partner)
        self.assertEqual(vals.get("brand_id"), self.brand1.id)
        order = self.env["sale.order"].create(vals)
        self.assertEqual(order.brand_id, self.brand1)

    def test_website_without_brand(self):
        """It should set the brand from the website's sales team"""
        website = self.env["website"].create(
            {
                "name": "Website without Brand",
                "company_id": self.brand_company.id,
                "brand_id": False,
                "salesteam_id": self.team.id,
            }
        )
        with MockRequest(self.env, website=website):
            vals = website._prepare_sale_order_values(self.partner)
        self.assertEqual(vals.get("brand_id"), self.brand1.id)
        order = self.env["sale.order"].create(vals)
        self.assertEqual(order.brand_id, self.brand1)

    def test_website_without_brand_and_team_brand(self):
        """It should not set the brand if neither website nor team has a brand"""
        team_without_brand = self.env["crm.team"].create(
            {
                "name": "Sales Team without Brand",
                "brand_id": False,
            }
        )
        website = self.env["website"].create(
            {
                "name": "Website without Any Brand",
                "company_id": self.brand_company.id,
                "brand_id": False,
                "salesteam_id": team_without_brand.id,
            }
        )
        with MockRequest(self.env, website=website):
            vals = website._prepare_sale_order_values(self.partner)
        self.assertNotIn("brand_id", vals)

    def test_so_creation_with_only_team_brand(self):
        """It should set the brand from the sales team if website is not set"""
        so = self.env["sale.order"].new(
            {
                "partner_id": self.partner.id,
                "team_id": self.team.id,
            }
        )
        so._onchange_team_id()
        self.assertEqual(so.brand_id, self.brand1)
