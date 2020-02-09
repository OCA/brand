import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-brand",
    description="Meta package for oca-brand Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-account_brand',
        'odoo12-addon-brand',
        'odoo12-addon-brand_external_report_layout',
        'odoo12-addon-contract_brand',
        'odoo12-addon-partner_brand',
        'odoo12-addon-product_contract_brand',
        'odoo12-addon-sale_brand',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
