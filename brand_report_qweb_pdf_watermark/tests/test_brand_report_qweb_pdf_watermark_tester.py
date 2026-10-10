# © 2025 OBS Solutions BV <http://obs-solutions.com>
from odoo import fields, models


class BrandReportQwebPdfWatermarkTester(models.Model):
    _name = "brand.report.qweb.pdf.watermark.tester"
    _description = "Brand Report Qweb Pdf Watermark Tester"

    brand_id = fields.Many2one(string="Brand:", comodel_name="res.brand")
