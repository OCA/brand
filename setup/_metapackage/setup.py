import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-brand",
    description="Meta package for oca-brand Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-account_brand>=16.0dev,<16.1dev',
        'odoo-addon-brand>=16.0dev,<16.1dev',
        'odoo-addon-brand_external_report_layout>=16.0dev,<16.1dev',
        'odoo-addon-partner_brand>=16.0dev,<16.1dev',
        'odoo-addon-product_brand>=16.0dev,<16.1dev',
        'odoo-addon-product_brand_mrp>=16.0dev,<16.1dev',
        'odoo-addon-product_brand_purchase>=16.0dev,<16.1dev',
        'odoo-addon-product_brand_stock>=16.0dev,<16.1dev',
        'odoo-addon-product_brand_stock_account>=16.0dev,<16.1dev',
        'odoo-addon-product_brand_tag>=16.0dev,<16.1dev',
        'odoo-addon-sale_brand>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
