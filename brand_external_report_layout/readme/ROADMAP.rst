To simplify the customization of the external layout we replaced the variable
company that odoo compute in the external_layout view by the object brand.

With this module, all custom layouts will display brand information out of the box.

This was possible and easy to implement as the company and the brand models
inherit from partner model and share the same informational fields.

The computed variable company is used to set report header and footer. It's not
meant to be used in the report business logic itself. But in that case
(if a custom layout use the variable company for some-reason other then header
and footer) this module can cause an issue because the used field can be
missing in the brand model or not correctly set.

In this case, we recommend to always use document field company for this use-end.
