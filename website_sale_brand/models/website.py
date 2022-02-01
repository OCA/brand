# Copyright 2022 Gecko escalade Sàrl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Website(models.Model):
    _inherit = 'website'
    """ res.brand.mixin is not inherited here because it does not work well
    with the Brand Use Level in the setting pages
    """

    brand_id = fields.Many2one(
        comodel_name='res.brand',
        string='Default Brand',
    )

    @api.multi
    def _prepare_sale_order_values(self, partner, pricelist):
        values = super(Website, self)._prepare_sale_order_values(partner, pricelist)
        if self.brand_id:
            values['brand_id'] = self.brand_id.id
        return values
