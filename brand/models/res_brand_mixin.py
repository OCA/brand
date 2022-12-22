# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.base.models import ir_ui_view

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

    def setup_modifiers(self, node, field=None):
        modifiers = {}
        attributes = ["invisible", "readonly", "required"]
        if field is not None:
            ir_ui_view.transfer_field_to_modifiers(field, modifiers, attributes)
        ir_ui_view.transfer_node_to_modifiers(node, modifiers)
        ir_ui_view.transfer_modifiers_to_node(modifiers, node)

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        """set visibility and requirement rules"""
        result = super(ResBrandMixin, self).get_view(
            view_id=view_id, view_type=view_type, **options
        )

        if view_type in ["tree", "form"]:
            doc = etree.XML(result["arch"])
            for node in doc.xpath("//field[@name='brand_id']"):
                elem = etree.Element(
                    "field", {"name": "brand_use_level", "invisible": "True"}
                )
                brand_use_level_field = self.fields_get(["brand_use_level"])[
                    "brand_use_level"
                ]
                brand_id_field = self.fields_get(["brand_id"])["brand_id"]
                self.setup_modifiers(elem, field=brand_use_level_field)
                node.addprevious(elem)
                node.set(
                    "attrs",
                    '{"invisible": '
                    '[("brand_use_level", "=", "%s")], '
                    '"required": '
                    '[("brand_use_level", "=", "%s")]}'
                    % (
                        BRAND_USE_LEVEL_NO_USE_LEVEL,
                        BRAND_USE_LEVEL_REQUIRED_LEVEL,
                    ),
                )
                self.setup_modifiers(node, field=brand_id_field)
            result["arch"] = etree.tostring(doc, encoding="unicode")
        return result
