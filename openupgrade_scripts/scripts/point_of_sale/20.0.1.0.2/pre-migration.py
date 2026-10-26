# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

_renamed_fields = [
    (
        "pos.payment.method",
        "pos_payment_method",
        "use_payment_terminal",
        "payment_provider",
    ),
    (
        "pos.config",
        "pos_config",
        "auto_validate_terminal_payment",
        "auto_validate_electronic_payment",
    ),
]


def _pos_session_sales_move(env):
    """pos.session.move_id is now the inverse of account.move.pos_session_sales_id"""
    openupgrade.add_columns(env, [("account.move", "pos_session_sales_id", "many2one")])
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move move
        SET pos_session_sales_id = session.session_id
        FROM (
            SELECT move_id, MIN(id) AS session_id
            FROM pos_session WHERE move_id IS NOT NULL
            GROUP BY move_id
        ) session
        WHERE session.move_id = move.id AND move.pos_session_sales_id IS NULL
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, _renamed_fields)
    _pos_session_sales_move(env)
    # type was computed from the journal before, now it's a stored field
    openupgrade.add_columns(
        env, [("pos.payment.method", "type", "selection", "pay_later")]
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE pos_payment_method method
        SET type = journal.type
        FROM account_journal journal
        WHERE journal.id = method.journal_id AND journal.type IN ('cash', 'bank')
        """,
    )
    # image is computed now, the uploaded one is custom_image
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_attachment SET res_field = 'custom_image'
        WHERE res_model = 'pos.payment.method' AND res_field = 'image'
        """,
    )
