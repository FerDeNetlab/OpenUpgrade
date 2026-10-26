# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import csv
import os

from openupgradelib import openupgrade

from odoo.modules import get_module_path


def _new_industry_xmlids_by_name():
    path = os.path.join(
        get_module_path("crm_iap_mine"), "data", "crm.iap.lead.industry.csv"
    )
    with open(path, encoding="utf-8") as csv_file:
        return {row["name"]: row["id"] for row in csv.DictReader(csv_file)}


@openupgrade.migrate()
def migrate(env, version):
    """The industry list was replaced, keep records whose name still exists
    by moving them to the new xmlid, and rename the others so they don't
    collide with new names; those are removed in post-migration"""
    new_xmlids = _new_industry_xmlids_by_name()
    env.cr.execute(
        """
        SELECT imd.name, industry.id, industry.name->>'en_US'
        FROM crm_iap_lead_industry industry
        JOIN ir_model_data imd ON
            imd.model = 'crm.iap.lead.industry'
            AND imd.module = 'crm_iap_mine'
            AND imd.res_id = industry.id
        """
    )
    renamed_xmlids = []
    obsolete_ids = []
    for xmlid, industry_id, name in env.cr.fetchall():
        new_xmlid = new_xmlids.get(name)
        if new_xmlid and new_xmlid != xmlid:
            renamed_xmlids.append(
                (f"crm_iap_mine.{xmlid}", f"crm_iap_mine.{new_xmlid}")
            )
        elif not new_xmlid:
            obsolete_ids.append(industry_id)
    openupgrade.rename_xmlids(env.cr, renamed_xmlids)
    if obsolete_ids:
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE crm_iap_lead_industry
            SET name = jsonb_build_object('en_US', (name->>'en_US') || ' (v19)')
            WHERE id IN %s
            """,
            (tuple(obsolete_ids),),
        )
