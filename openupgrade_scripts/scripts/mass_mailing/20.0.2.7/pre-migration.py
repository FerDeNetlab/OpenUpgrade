# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # was a window action, is a server action now
    openupgrade.delete_records_safely_by_xml_id(
        env, ["mass_mailing.mailing_list_merge_action"]
    )
