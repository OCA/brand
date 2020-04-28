To use this module, you need to:

#. Go to Settings > General Settings
#. Select the brand use level
#. Go to Settings > Users & Companies > Brands
#. Add a new brand
#. Install one of branding module (e.g. account_brand)
#. Based on your choice for the brand use level, you will see a new field added to the
   branded object

To make a branded object, you need to:

#. Inherit from the `res.brand.mixin`
    .. code-block:: python


        class YourModel(models.Model):
            _name = 'your.model'
            _inherit = ['your.model', 'res.brand.mixin']

#. Add the brand field to the object form or tree view. The mixin will add the brand
   use level field automatically to the view and set the modifiers to the brand field.
   This will define its visibility and if it's required or not.

You can refer to the `account_brand <https://github.com/OCA/brand/blob/12.0/account_brand>`_. for more details.
