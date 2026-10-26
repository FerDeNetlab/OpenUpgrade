# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Avoid the ORM computing these while the models of activities'
    # documents (account.move, ...) aren't loaded yet. phone is filled
    # in end-migration, role_id is empty as res.role is new
    openupgrade.add_columns(
        env,
        [
            ("mail.activity", "phone", "char"),
            ("mail.activity", "role_id", "many2one"),
        ],
    )
    # v20 adds the admin's membership of #admin as noupdate data, the admin
    # usually got subscribed already
    env.cr.execute(
        """
        SELECT member.id
        FROM discuss_channel_member member
        JOIN ir_model_data channel_xmlid ON
            channel_xmlid.model = 'discuss.channel'
            AND channel_xmlid.res_id = member.channel_id
            AND channel_xmlid.module = 'mail'
            AND channel_xmlid.name = 'channel_admin'
        JOIN ir_model_data partner_xmlid ON
            partner_xmlid.model = 'res.partner'
            AND partner_xmlid.res_id = member.partner_id
            AND partner_xmlid.module = 'base'
            AND partner_xmlid.name = 'partner_admin'
        """
    )
    for (member_id,) in env.cr.fetchall():
        openupgrade.add_xmlid(
            env.cr,
            "mail",
            "channel_member_channel_admin_partner_admin",
            "discuss.channel.member",
            member_id,
            noupdate=True,
        )
