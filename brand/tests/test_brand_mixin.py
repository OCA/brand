from lxml import etree

from .common import CommonCase


class TestBrand(CommonCase):
    def test_get_view(self):
        view = self.env["res.config.settings"].get_view(
            view_id=self.env.ref("base.res_config_settings_view_form").id,
            view_type="form",
        )
        doc = etree.XML(view["arch"])
        self.assertTrue(doc.xpath("//field[@name='brand_use_level']"))
