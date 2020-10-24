import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-brand",
    description="Meta package for oca-brand Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-account_brand',
        'odoo13-addon-analytic_brand',
        'odoo13-addon-brand',
        'odoo13-addon-brand_external_report_layout',
        'odoo13-addon-product_brand',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
