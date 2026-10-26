# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """Remove the industries of the old list now, instead of at the end of the
    upgrade, so that the new required columns get their NOT NULL constraint"""
    env.cr.execute(
        """
        SELECT imd.module || '.' || imd.name
        FROM ir_model_data imd
        JOIN crm_iap_lead_industry industry ON industry.id = imd.res_id
        WHERE imd.model = 'crm.iap.lead.industry' AND industry.sic_group IS NULL
        """
    )
    openupgrade.delete_records_safely_by_xml_id(
        env, [xmlid for (xmlid,) in env.cr.fetchall()]
    )
