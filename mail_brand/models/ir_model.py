# Copyright (C) 2022 Snakebyte
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class BaseModel(models.AbstractModel):
    _inherit = "base"

    def get_base_url(self):
        if not self:
            return super().get_base_url()
        if "brand_id" in self and "website_id" in self.brand_id:
            return self.brand_id.website_website_id.domain
        else:
            return super().get_base_url()
