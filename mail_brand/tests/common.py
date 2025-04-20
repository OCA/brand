import base64

from odoo.tests.common import TransactionCase, tagged
from odoo.tools.misc import file_path


@tagged("mail_brand")
class MailBrandCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.module_name = "mail_brand"
        icon_path = file_path("mail_brand/static/description/CommunityBadge.png")
        with open(icon_path, "rb") as f:
            cls.icon_bytes = f.read()
        cls.icon_base64 = base64.b64encode(cls.icon_bytes).decode("utf-8")
        cls.test_brand = cls.env["res.brand"].create({"name": "Test Brand"})

        cls.test_brand = cls.env["res.brand"].create(
            {"partner_id": cls.env["res.partner"].create({"name": "Test Brand"}).id}
        )
        cls.test_contact = cls.env["res.partner"].create({"name": "Test Contact"})
