{
    'name': 'Website Product Brand Block',
    'version': '18.0.1.0.0',
    'depends': ['website_sale', 'product_brand'],
    'data': ['views/product_brand_template.xml'],
    'assets': {
    'web.assets_frontend': [
        'website_product_brand_block/static/src/css/brand_styles.css',
    ],
},
    'installable': True,
}