# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

_renamed_fields = [
    ("product.template", "product_template", "expense_policy", "reinvoice_policy"),
]


def _convert_sale_delay(env):
    """sale_delay moved from stock and is company dependent now: store the
    old value for the product's company, or for all companies if shared"""
    if not openupgrade.column_exists(env.cr, "product_template", "sale_delay"):
        return
    legacy_column = openupgrade.get_legacy_name("sale_delay")
    openupgrade.rename_columns(
        env.cr, {"product_template": [("sale_delay", legacy_column)]}
    )
    openupgrade.logged_query(
        env.cr, "ALTER TABLE product_template ADD COLUMN sale_delay jsonb"
    )
    openupgrade.logged_query(
        env.cr,
        f"""
        UPDATE product_template
        SET sale_delay = CASE
            WHEN company_id IS NOT NULL
                THEN jsonb_build_object(company_id::text, {legacy_column})
            ELSE (
                SELECT jsonb_object_agg(company.id::text, {legacy_column})
                FROM res_company company
            )
        END
        WHERE COALESCE({legacy_column}, 0) != 0
        """,
    )


def _require_payment_to_prepayment(env):
    """require_payment is gone, online payment is required iff
    prepayment_percent > 0; v19 kept the company default in there"""
    if not openupgrade.column_exists(env.cr, "sale_order", "require_payment"):
        return
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE sale_order SET prepayment_percent = 0.0
        WHERE NOT COALESCE(require_payment, FALSE)
            AND prepayment_percent IS DISTINCT FROM 0.0
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, _renamed_fields)
    _require_payment_to_prepayment(env)
    # was a window action, is a server action now
    openupgrade.delete_records_safely_by_xml_id(
        env, ["sale.action_accrued_revenue_entry_sale_order_line"]
    )
    _convert_sale_delay(env)
