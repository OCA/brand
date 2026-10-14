# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Brand",
    "summary": "Manage brands and add branding to business documents",
    "version": "20.0.1.0.0",
    "license": "LGPL-3",
    "author": "Odoo Community Association (OCA), ACSONE SA/NV",
    "website": "https://github.com/OCA/brand",
    "depends": ["base_setup"],
    "data": [
        "views/res_config_settings.xml",
        "security/res_brand.xml",
        "views/res_brand.xml",
    ],
    "maintainers": ["sbejaoui"],
}
