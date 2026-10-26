"""Encode any known changes to the database here
to help the matching process
"""

# Renamed modules is a mapping from old module name to new module name
renamed_modules = {
    # odoo
    # vat checks moved to base, vies_valid & co to l10n_eu_account_vies
    "base_vat": "l10n_eu_account_vies",
    "purchase_requisition_sale": "purchase_alternative_sale",
    "website_sale_autocomplete": "website_address_autocomplete",
    # odoo/enterprise
    # OCA/...
}

# Merged modules contain a mapping from old module names to other,
# preexisting module names
merged_modules = {
    # odoo
    "account_add_gln": "account",
    "account_peppol_response": "account_peppol",
    "base_iban": "account",
    "delivery_stock_picking_batch": "stock_delivery",
    "hr_holidays_homeworking": "hr_holidays",
    "hr_homeworking": "hr",
    "hr_homeworking_calendar": "hr_calendar",
    "hr_hourly_cost": "hr",
    "hr_org_chart": "hr",
    "hr_work_entry_holidays": "hr_holidays",
    "l10n_cn_city": "l10n_cn",
    "l10n_dk_nemhandel": "l10n_dk",
    "l10n_dk_nemhandel_response": "l10n_dk",
    "l10n_dk_oioubl": "l10n_dk",
    "l10n_ec_stock": "l10n_ec",
    "l10n_fr_hr_work_entry_holidays": "l10n_fr_hr_holidays",
    "l10n_hu_edi_receive": "l10n_hu_edi",
    "l10n_lk_invoice": "l10n_lk",
    "l10n_pl_bank_verification": "l10n_pl",
    "l10n_ro_cpv_code": "l10n_ro_edi",
    "l10n_ro_edi_stock_batch": "l10n_ro_edi_stock",
    "l10n_sa_withholding_tax": "l10n_sa",
    "pos_restaurant_adyen": "pos_adyen",
    "pos_restaurant_stripe": "pos_stripe",
    "pos_self_order_adyen": "pos_adyen",
    "pos_self_order_stripe": "pos_stripe",
    "pos_self_order_viva_com": "pos_viva_com",
    "stock_picking_batch": "stock",
    "website_sale_collect_wishlist": "website_sale_collect",
    "website_sale_comparison": "website_sale",
    "website_sale_comparison_wishlist": "website_sale",
    "website_sale_stock_wishlist": "website_sale",
    "website_sale_wishlist": "website_sale",
    # odoo/enterprise
    # OCA/...
}

# only used here for upgrade_analysis
renamed_models = {
    # odoo
    "hr.contract.type": "hr.employee.type",
    "l10n_tr_nilvera_einvoice_extended.tax.office": "l10n_tr.tax.office",
    "website.base.unit": "product.base.unit",
    # OCA/...
}

# only used here for upgrade_analysis
merged_models = {
    # odoo
    "hr.leave.type": "hr.work.entry.type",
    # OCA/...
}
