# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """Set Brand for existing forecasts."""
    _logger.info('Set Brand for existing forecasts')
    cr.execute(
        """
            UPDATE contract_line_forecast_period AS forecast
            SET brand_id=contract.brand_id
            FROM contract_contract AS contract
            WHERE forecast.contract_id=contract.id
            AND forecast.contract_id IS NOT NULL
        """
    )
