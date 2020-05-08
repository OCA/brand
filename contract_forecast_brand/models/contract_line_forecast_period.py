# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ContractLineForecastPeriod(models.Model):

    _name = 'contract.line.forecast.period'
    _inherit = ['contract.line.forecast.period', 'res.brand.mixin']
