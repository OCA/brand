from odoo.tests.common import TransactionCase


class TestMailTemplate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestMailTemplate, cls).setUpClass()
        cls.brand_a = cls.env["res.brand"].create(
            {"partner_id": cls.env["res.partner"].create({"name": "Brand A"}).id}
        )
        cls.brand_b = cls.env["res.brand"].create(
            {"partner_id": cls.env["res.partner"].create({"name": "Brand B"}).id}
        )
        cls.mail_template = cls.env["mail.template"]
        cls.ir_model = cls.env["ir.model"]
        cls.partner_model_id = cls.ir_model.search(
            [("model", "=", "res.partner")], limit=1
        ).id

    def test_brand_id_on_template_creation(self):
        template = self.mail_template.create(
            {
                "name": "Test Template A",
                "subject": "Test Subject",
                "body_html": "<p>Test Body</p>",
                "brand_id": self.brand_a.id,
                "model_id": self.partner_model_id,
            }
        )
        self.assertEqual(
            template.brand_id, self.brand_a, "Template should have the assigned brand"
        )

    def test_brand_id_on_template_read(self):
        template = self.mail_template.create(
            {
                "name": "Test Template B",
                "subject": "Test Subject",
                "body_html": "<p>Test Body</p>",
                "brand_id": self.brand_b.id,
                "model_id": self.partner_model_id,
            }
        )
        read_template = self.mail_template.browse(template.id)
        self.assertEqual(
            read_template.brand_id,
            self.brand_b,
            "Read template should retain the assigned brand",
        )

    def test_brand_id_on_template_write(self):
        template = self.mail_template.create(
            {
                "name": "Test Template C",
                "subject": "Test Subject",
                "body_html": "<p>Test Body</p>",
                "model_id": self.partner_model_id,
            }
        )
        template.write({"brand_id": self.brand_a.id})
        self.assertEqual(
            template.brand_id, self.brand_a, "Template should have the updated brand"
        )
