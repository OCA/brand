# Copyright 2021 Yves Goldberg
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BrandExt(models.Model):

    _inherit = "res.brand"

    catchall_alias = fields.Char(string="Catchall alias")
    catchall_domain = fields.Char(string="Catchall domain")
    outgoing_mail_server_id = fields.Many2one(
        "ir.mail_server", string="Outgoing Mail Server"
    )
