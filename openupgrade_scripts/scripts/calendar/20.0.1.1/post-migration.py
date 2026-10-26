# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """The default privacy moved from the user settings to the user's
    primary calendar, which v20 creates in a post_init_hook only"""
    users = (
        env["res.users"]
        .with_context(active_test=False)
        .search(
            [
                ("share", "=", False),
                ("calendar_user_ids", "not any", [("is_primary", "=", True)]),
            ]
        )
    )
    users._generate_primary_calendar()
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE calendar_calendar calendar
        SET calendar_default_privacy = settings.calendar_default_privacy
        FROM calendar_user calendar_user
        JOIN res_users_settings settings ON settings.user_id = calendar_user.user_id
        WHERE calendar_user.calendar_id = calendar.id
            AND calendar_user.is_primary
            AND calendar_user.access_role = 'owner'
            AND settings.calendar_default_privacy IN
                ('public', 'private', 'confidential')
        """,
    )
