# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    _logger.info("Delete res.brand form view")
    openupgrade.delete_records_safely_by_xml_id(
        env, "analytic_brand.res_brand_form_view"
    )
    _logger.info("Create analytic distribution models for brands")
    openupgrade.logged_query(
        env.cr,
        """
        SELECT id, analytic_distribution
        FROM res_brand
        WHERE analytic_distribution IS NOT NULL
        """,
    )
    res = env.cr.fetchall()
    vals_create = []
    for brand_id, analytic_distribution in res:
        vals_create.append(
            {"brand_id": brand_id, "analytic_distribution": analytic_distribution}
        )
    env["account.analytic.distribution.model"].create(vals_create)
