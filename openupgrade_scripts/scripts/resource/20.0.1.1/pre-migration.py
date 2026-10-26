# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # lunch breaks are not modelled as attendances anymore, they're the gap
    # between morning and afternoon
    # TODO: two weeks calendars (week_type), schedule_type and tz on calendar
    openupgrade.logged_query(
        env.cr, "DELETE FROM resource_calendar_attendance WHERE day_period = 'lunch'"
    )
