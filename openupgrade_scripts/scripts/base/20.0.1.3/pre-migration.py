# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

# pylint: disable=odoo-addons-relative-import
from odoo.addons.openupgrade_scripts.apriori import merged_modules, renamed_modules

_renamed_xmlids = [
    # same (country, code) as before, would violate res_country_state_name_code_uniq
    ("base.state_in_or", "base.state_in_od"),
]

_renamed_fields = [
    ("res.partner.bank", "res_partner_bank", "acc_number", "account_number"),
    (
        "res.partner.bank",
        "res_partner_bank",
        "sanitized_acc_number",
        "sanitized_account_number",
    ),
    ("res.partner.bank", "res_partner_bank", "acc_holder_name", "holder_name"),
]

_new_bank_columns = [
    ("res.partner.bank", "bank_name", "char"),
    ("res.partner.bank", "bank_bic", "char"),
    ("res.partner.bank", "street", "char"),
    ("res.partner.bank", "street2", "char"),
    ("res.partner.bank", "zip", "char"),
    ("res.partner.bank", "city", "char"),
    ("res.partner.bank", "state_id", "many2one"),
    ("res.partner.bank", "country_id", "many2one"),
]


def _merge_res_bank(env):
    """res.bank is gone, its data lives on res.partner.bank now"""
    openupgrade.rename_fields(env, _renamed_fields)
    openupgrade.add_columns(env, _new_bank_columns)
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_partner_bank partner_bank
        SET bank_name = bank.name,
            bank_bic = bank.bic,
            street = bank.street,
            street2 = bank.street2,
            zip = bank.zip,
            city = bank.city,
            state_id = bank.state,
            country_id = bank.country
        FROM res_bank bank
        WHERE bank.id = partner_bank.bank_id
        """,
    )
    # same fallback as _compute_country_id, which doesn't run on a precreated column
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_partner_bank partner_bank
        SET country_id = COALESCE(partner.country_id, company_partner.country_id)
        FROM res_partner partner
        LEFT JOIN res_company company ON company.id = partner.company_id
        LEFT JOIN res_partner company_partner ON company_partner.id = company.partner_id
        WHERE partner.id = partner_bank.partner_id AND partner_bank.country_id IS NULL
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        f"""
        CREATE TABLE {
            openupgrade.get_legacy_name("ir_module_module")
        } AS (SELECT name, state FROM ir_module_module);
        """,
    )
    openupgrade.update_module_names(
        env.cr, renamed_modules.items(), environment_namespec=True
    )
    openupgrade.update_module_names(
        env.cr, merged_modules.items(), merge_modules=True, environment_namespec=True
    )
    openupgrade.clean_transient_models(env.cr)
    openupgrade.rename_xmlids(env.cr, _renamed_xmlids)
    # index is a selection now, a plain type change would yield 'true'/'false'
    # which breaks manual fields (ie analytic plan columns)
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE ir_model_fields
        ALTER COLUMN index TYPE varchar
        USING CASE WHEN index THEN 'btree' END
        """,
    )
    _merge_res_bank(env)
    # TODO(test only): ir.model.access and ir.rule are replaced by ir.access.
    # Module data recreates the standard records under the same xmlids, so park
    # the old xmlids; converting custom records to ir.access is still missing.
    openupgrade.logged_query(
        env.cr,
        f"""
        CREATE TABLE {openupgrade.get_legacy_name("ir_model_data_access")} AS (
            SELECT * FROM ir_model_data WHERE model IN ('ir.model.access', 'ir.rule')
        );
        DELETE FROM ir_model_data WHERE model IN ('ir.model.access', 'ir.rule');
        """,
    )
