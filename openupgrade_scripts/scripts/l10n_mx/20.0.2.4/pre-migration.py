# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """res.bank is merged into res.partner.bank by base: the bank's ABM code
    becomes the account's clearing number labelled 'ABM Code', like Odoo's
    own demo data does. Banks with an ABM code are Mexican."""
    if not openupgrade.column_exists(env.cr, "res_bank", "l10n_mx_edi_code"):
        return
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_partner_bank partner_bank
        SET clearing_number = TRIM(bank.l10n_mx_edi_code),
            clearing_label_id = %(label)s,
            country_id = %(mx)s
        FROM res_bank bank
        WHERE bank.id = partner_bank.bank_id
            AND COALESCE(TRIM(bank.l10n_mx_edi_code), '') != ''
            AND COALESCE(partner_bank.clearing_number, '') = ''
            AND (partner_bank.country_id = %(mx)s OR bank.country IS NULL)
        """,
        {
            "mx": env.ref("base.mx").id,
            "label": env.ref("base.clearing_label_mx").id,
        },
    )
