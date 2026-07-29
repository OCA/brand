from odoo import models


class AnalyticMixin(models.AbstractModel):
    _inherit = "analytic.mixin"

    def _merge_distribution(self, old_distribution, new_distribution):
        if "__update__" not in new_distribution:
            return new_distribution
        (
            non_changing_values,
            changing_values,
            non_changing_amount,
            changing_amount,
        ) = self._modifiying_distribution_values(
            old_distribution,
            dict(new_distribution),
        )
        if non_changing_values and changing_values:
            return {
                ",".join(map(str, k)): v for k, v in non_changing_values.items()
            } | {",".join(map(str, k)): v for k, v in changing_values.items()}
        return super()._merge_distribution(old_distribution, new_distribution)
