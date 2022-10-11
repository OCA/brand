# Copyright 2022 Snakebyte
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo import api, fields, models


class ResBrand(models.Model):
    _inherit = "res.brand"

    invoice_terms = fields.Html(string="Default Terms and Conditions", translate=True)
    terms_type = fields.Selection(
        [("plain", "Add a Note"), ("html", "Add a link to a Web Page")],
        string="Terms & Conditions format",
        default="plain",
    )
    terms_page = fields.Char(
        help="page on the brands site where the terms can be found",
        translate=True,
        default="/terms",
    )
    terms_url = fields.Char(string="Preview terms", compute="_compute_terms_url")

    # flake8: noqa: B950
    @api.onchange("website", "terms_page")
    def _compute_terms_url(self):
        link_tags = re.compile(
            r"""(?<!["'])((ftp|http|https):\/\/(\w+:{0,1}\w*@)?([^\s<"']+)(:[0-9]+)?(\/|\/([^\s<"']))?)(?![^\s<"']*["']|[^\s<"']*</a>)"""
        )
        for brand in self:
            idx = 0
            final = ""
            text = brand.website + brand.terms_page
            for item in re.finditer(link_tags, text):
                final += text[idx : item.start()]
                final += item.group(0)
                idx = item.end()
            final += text[idx:]
            brand.terms_url = final
