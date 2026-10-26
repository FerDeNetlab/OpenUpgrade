# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """share's name isn't translatable anymore, but the column gets created
    as jsonb from the stale translate flag of ir.model.fields"""
    env.cr.execute(
        """
        SELECT data_type FROM information_schema.columns
        WHERE table_name = 'spreadsheet_dashboard_share' AND column_name = 'name'
        """
    )
    if env.cr.fetchone() != ("jsonb",):
        return
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE spreadsheet_dashboard_share
        ALTER COLUMN name TYPE varchar USING name->>'en_US'
        """,
    )
