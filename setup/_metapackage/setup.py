import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-brand",
    description="Meta package for oca-brand Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-account_brand>=15.0dev,<15.1dev',
        'odoo-addon-analytic_brand>=15.0dev,<15.1dev',
        'odoo-addon-brand>=15.0dev,<15.1dev',
        'odoo-addon-brand_external_report_layout>=15.0dev,<15.1dev',
        'odoo-addon-contract_brand>=15.0dev,<15.1dev',
        'odoo-addon-product_brand>=15.0dev,<15.1dev',
        'odoo-addon-product_brand_stock>=15.0dev,<15.1dev',
        'odoo-addon-sale_brand>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
