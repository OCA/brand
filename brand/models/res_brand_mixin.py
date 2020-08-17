# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from lxml import etree
from odoo import api, fields, models, _
from odoo.osv import orm
from odoo.exceptions import ValidationError
from .res_company import (
    BRAND_USE_LEVEL_SELECTION,
    BRAND_USE_LEVEL_NO_USE_LEVEL,
    BRAND_USE_LEVEL_REQUIRED_LEVEL,
)


class ResBrandMixin(models.AbstractModel):

    _name = 'res.brand.mixin'
    _description = 'Brand Mixin'

    brand_id = fields.Many2one(
        'res.brand', string='Brand', help="Brand to use for this sale"
    )
    brand_use_level = fields.Selection(
        string="Brand Use Level",
        selection=BRAND_USE_LEVEL_SELECTION,
        default=BRAND_USE_LEVEL_NO_USE_LEVEL,
        related='company_id.brand_use_level',
    )
    company_id = fields.Many2one('res.company')

    @api.multi
    def _is_brand_required(self):
        self.ensure_one()
        return (
            self.company_id.brand_use_level == BRAND_USE_LEVEL_REQUIRED_LEVEL
        )

    @api.constrains('brand_id', 'company_id')
    def _check_brand_requirement(self):
        for rec in self:
            if rec._is_brand_required() and not rec.brand_id:
                raise ValidationError(_("Brand is required"))

    @api.constrains('brand_id', 'company_id')
    def _check_brand_company_id(self):
        for rec in self:
            if (
                rec.brand_id.company_id
                and rec.brand_id.company_id != rec.company_id
            ):
                raise ValidationError(
                    _("Brand company must match document company for %s")
                    % rec.display_name
                )

    @api.onchange('brand_id')
    def _onchange_brand_id(self):
        for rec in self.filtered('brand_id.company_id'):
            if rec.brand_id and rec.brand_id.company_id:
                rec.company_id = rec.brand_id.company_id

    def fields_view_get(
        self, view_id=None, view_type='form', toolbar=False, submenu=False
    ):
        """set visibility and requirement rules"""
        result = super(ResBrandMixin, self).fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )

        if view_type in ['tree', 'form']:
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//field[@name='brand_id']"):
                elem = etree.Element(
                    'field', {'name': 'brand_use_level', 'invisible': 'True'}
                )
                orm.setup_modifiers(
                    elem,
                    self.fields_get(['brand_use_level'])['brand_use_level'],
                )
                node.addprevious(elem)
                node.set(
                    'attrs',
                    '{"invisible": '
                    '[("brand_use_level", "=", "%s")], '
                    '"required": '
                    '[("brand_use_level", "=", "%s")]}'
                    % (
                        BRAND_USE_LEVEL_NO_USE_LEVEL,
                        BRAND_USE_LEVEL_REQUIRED_LEVEL,
                    ),
                )
                orm.setup_modifiers(node, result['fields']['brand_id'])
            result['arch'] = etree.tostring(doc, encoding='unicode')
        return result
