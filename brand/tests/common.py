from odoo.tests.common import TransactionCase


class CommonCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.brand_model = cls.env["res.brand"]
        cls.company_model = cls.env["res.company"]
        cls.partner_model = cls.env["res.partner"]

        cls.company_no_brand = cls.company_model.create({"name": "No Brand Company"})
        cls.company_optional_brand = cls.company_model.create(
            {"name": "Optional Brand Company", "brand_use_level": "optional"}
        )
        cls.company_required_brand = cls.company_model.create(
            {"name": "Required Brand Company", "brand_use_level": "required"}
        )

        cls.partner = cls.partner_model.create({"name": "Test Partner"})
        cls.brand = cls.brand_model.create({"partner_id": cls.partner.id})
