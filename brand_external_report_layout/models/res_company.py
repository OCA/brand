# Copyright 2024 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>

from odoo import models


class CompanyBrandAdapter:
    def __init__(self, company, brand):
        super().__init__()
        for field in dir(company):
            if field.startswith("__"):
                continue
            brands_fields = brand._get_company_overriden_fields()
            if field in brands_fields and getattr(brand, field):
                setattr(self, field, getattr(brand, field))
            else:
                setattr(self, field, getattr(company, field))


class ResCompany(models.Model):
    _inherit = "res.company"

    def _get_company_brand_adapter(self, brand):
        return CompanyBrandAdapter(self, brand)
