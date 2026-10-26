# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

_renamed_fields = [
    ("stock.move", "stock_move", "product_uom", "uom_id"),
    ("stock.move.line", "stock_move_line", "product_uom_id", "uom_id"),
    ("stock.move", "stock_move", "location_final_id", "forecasted_location_id"),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, _renamed_fields)
    # 'none' was removed, an untracked product has no tracking now
    openupgrade.logged_query(
        env.cr, "UPDATE product_template SET tracking = NULL WHERE tracking = 'none'"
    )
