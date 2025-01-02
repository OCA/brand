To use this module, you need to:

1.  Go to Settings \> General Settings
2.  Select the brand use level
3.  Go to Settings \> Users & Companies \> Brands
4.  Add a new brand
5.  Install one of branding module (e.g. account_brand)
6.  Based on your choice for the brand use level, you will see a new
    field added to the branded object

To make a branded object, you need to:

1.  Inherit from the res.brand.mixin
    ``` python
    class YourModel(models.Model):
        _name = 'your.model'
        _inherit = ['your.model', 'res.brand.mixin']
    ```

2.  Add the brand field to the object form or tree view. The mixin will
    add the brand use level field automatically to the view and set the
    modifiers to the brand field. This will define its visibility and if
    it's required or not.

You can refer to the
[account_brand](https://github.com/OCA/brand/blob/18.0/account_brand).
for more details.
