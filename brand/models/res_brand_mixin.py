# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from lxml.builder import E

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .res_company import BRAND_USE_LEVEL_NO_USE_LEVEL, BRAND_USE_LEVEL_REQUIRED_LEVEL


class ResBrandMixin(models.AbstractModel):
    _name = "res.brand.mixin"
    _description = "Brand Mixin"

    brand_id = fields.Many2one(
        comodel_name="res.brand",
        string="Brand",
        help="Brand to use for this sale",
    )
    brand_use_level = fields.Selection(
        string="Brand Use Level",
        related="company_id.brand_use_level",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
    )

    def _is_brand_required(self):
        self.ensure_one()
        return self.company_id.brand_use_level == BRAND_USE_LEVEL_REQUIRED_LEVEL

    @api.constrains("brand_id", "company_id")
    def _check_brand_requirement(self):
        for rec in self:
            if rec._is_brand_required() and not rec.brand_id:
                raise ValidationError(_("Brand is required"))

    @api.constrains("brand_id", "company_id")
    def _check_brand_company_id(self):
        for rec in self:
            if rec.brand_id.company_id and rec.brand_id.company_id != rec.company_id:
                raise ValidationError(
                    _("Brand company must match document company for %s")
                    % rec.display_name
                )

    @api.onchange("brand_id")
    def _onchange_brand_id(self):
        for rec in self.filtered("brand_id.company_id"):
            if rec.brand_id and rec.brand_id.company_id:
                rec.company_id = rec.brand_id.company_id

    def _get_view(self, view_id=None, view_type="form", **options):
        """set visibility and requirement rules"""
        arch, view = super()._get_view(view_id, view_type, **options)
        if self.env["res.brand"].check_access("read"):
            if view.type in ["form", "list"]:
                brand_node = next(
                    iter(
                        arch.xpath(
                            '//field[@name="brand_id"][not(ancestor::*'
                            '[@widget="one2many" or @widget="many2many"])]'
                        )
                    ),
                    None,
                )

                if brand_node is not None:
                    brand_node.addprevious(
                        E.field(
                            name="brand_use_level",
                            invisible="True",
                            column_invisible="True",
                        )
                    )

                    brand_node.set(
                        "invisible",
                        f"brand_use_level == '{BRAND_USE_LEVEL_NO_USE_LEVEL}'",
                    )
                    brand_node.set(
                        "required",
                        f"brand_use_level == '{BRAND_USE_LEVEL_REQUIRED_LEVEL}'",
                    )

        return arch, view
