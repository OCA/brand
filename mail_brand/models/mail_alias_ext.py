# Copyright 2021 Yves Goldberg
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailAliasExt(models.Model):
    _inherit = "mail.alias"

    brand_id = fields.Many2one("res.brand", "Brand")

    def _get_alias_domain(self):
        super(MailAliasExt, self)._get_alias_domain()
        for record in self:
            if record.brand_id:
                record.alias_domain = record.brand_id.catchall_domain
