# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

_renamed_xmlids = [
    (
        "stock_account.action_report_stock_valuation",
        "account.action_report_stock_valuation",
    ),
    (
        "stock_account.ir_cron_post_stock_valuation",
        "account.ir_cron_post_stock_valuation",
    ),
]


def _deductible_percentage(env):
    """deductible_amount (0-100) became deductible_percentage (0-1)"""
    if not openupgrade.column_exists(env.cr, "account_move_line", "deductible_amount"):
        return
    openupgrade.add_columns(
        env,
        [
            (
                "account.move.line",
                "deductible_percentage",
                "float",
                1.0,
                "account_move_line",
                "float8",
            )
        ],
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move_line
        SET deductible_percentage = deductible_amount / 100.0
        WHERE deductible_amount IS NOT NULL AND deductible_amount != 100
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, _renamed_xmlids)
    _deductible_percentage(env)
