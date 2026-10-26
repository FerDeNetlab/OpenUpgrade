# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    activities = (
        env["mail.activity"]
        .with_context(active_test=False)
        .search([("activity_category", "=", "phonecall")])
    )
    activities._compute_phone()
