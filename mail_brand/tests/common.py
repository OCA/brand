import base64

from odoo.modules import get_resource_path
from odoo.tests.common import TransactionCase, tagged


@tagged("mail_brand")
class MailBrandCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(MailBrandCommon, cls).setUpClass()
        cls.module_name = "mail_brand"
        cls.icon_path = get_resource_path(
            cls.module_name, "static", "description", "icon.png"
        )
        with open(cls.icon_path, "rb") as f:
            cls.icon_bytes = f.read()
            cls.icon_base64 = base64.b64encode(cls.icon_bytes)

        cls.test_brand = cls.env["res.brand"].create(
            {"partner_id": cls.env["res.partner"].create({"name": "Test Brand"}).id}
        )
        cls.test_contact = cls.env["res.partner"].create({"name": "Test Contact"})
