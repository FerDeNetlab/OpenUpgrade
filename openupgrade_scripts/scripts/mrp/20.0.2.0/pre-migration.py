# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

_renamed_fields = [
    ("mrp.bom", "mrp_bom", "product_uom_id", "uom_id"),
    ("mrp.bom.byproduct", "mrp_bom_byproduct", "product_uom_id", "uom_id"),
    ("mrp.bom.line", "mrp_bom_line", "product_uom_id", "uom_id"),
    ("mrp.production", "mrp_production", "product_uom_id", "uom_id"),
    ("mrp.unbuild", "mrp_unbuild", "product_uom_id", "uom_id"),
    ("mrp.workcenter.capacity", "mrp_workcenter_capacity", "product_uom_id", "uom_id"),
    ("mrp.production", "mrp_production", "location_final_id", "forecasted_location_id"),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, _renamed_fields)
