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
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
