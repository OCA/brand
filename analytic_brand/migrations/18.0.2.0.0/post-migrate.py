# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def _find_company_from_analytic_distribution(env, analytic_distribution):
    # Take inspiration from Odoo method _compute_distribution_analytic_account_ids
    # on analytic.mixin
    account_ids = {int(_id) for key in analytic_distribution for _id in key.split(";")}
    env.cr.execute(
        """
        SELECT DISTINCT company_id
        FROM account_analytic_account
        WHERE id IN %(account_ids)s
        """,
        {
            "account_ids": tuple(account_ids),
        },
    )
    res = env.cr.fetchall()
    if not res:
        return False
    if len(res) > 1:
        _logger.error(
            "Analytic distribution %s mixes accounts from several companies",
            analytic_distribution,
        )
    return res[0][0]


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
        company_id = _find_company_from_analytic_distribution(
            env, analytic_distribution
        )
        vals_create.append(
            {
                "brand_id": brand_id,
                "analytic_distribution": analytic_distribution,
                "company_id": company_id,
            }
        )
    env["account.analytic.distribution.model"].create(vals_create)
