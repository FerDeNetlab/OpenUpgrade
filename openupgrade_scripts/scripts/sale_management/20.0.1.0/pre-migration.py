# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """require_payment is gone, the template requires payment iff
    prepayment_percent > 0"""
    if not openupgrade.column_exists(env.cr, "sale_order_template", "require_payment"):
        return
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE sale_order_template SET prepayment_percent = 0.0
        WHERE NOT COALESCE(require_payment, FALSE)
            AND prepayment_percent IS DISTINCT FROM 0.0
        """,
    )
