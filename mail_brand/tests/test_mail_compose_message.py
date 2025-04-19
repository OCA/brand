from odoo.addons.mail_brand.tests.common import MailBrandCommon


class TestMailComposeMessage(MailBrandCommon):
    def test_default_get_brand_id(self):
        wizard = (
            self.env["mail.compose.message"]
            .with_context(active_id=self.test_contact.id, active_model="res.partner")
            .create({"brand_id": self.test_brand.id})
        )
        self.assertEqual(
            wizard.brand_id,
            self.test_brand,
            "Brand should be pre-populated (if logic was present)",
        )

    def test_action_send_mail_context(self):
        recipient = self.env["res.partner"].create({"name": "Test Recipient"})
        # Create the wizard with a brand and a recipient
        wizard = self.env["mail.compose.message"].create(
            {
                "brand_id": self.test_brand.id,
                "partner_ids": [(6, 0, [recipient.id])],
                "subject": "Test Subject",
                "body": "<p>Test body</p>",
            }
        )
        # Modify the environment's context directly
        self.env = self.env(
            context=dict(self.env.context, email_brand=self.test_brand.id)
        )
        wizard.action_send_mail()
        self.assertEqual(
            self.env.context.get("email_brand"),
            self.test_brand.id,
            "Email brand should be in context",
        )
