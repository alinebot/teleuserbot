# Copyright (C) 2018 Raphielscape LLC.
#
# Licensed under the Raphielscape Public License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
#

from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User

from userbot import COUNT_PM, LOGGER, LOGGER_GROUP, NOTIF_OFF, PM_AUTO_BAN
from userbot.events import register
from userbot import CMD_HELP

@register(incoming=True)
async def permitpm(e):
    if PM_AUTO_BAN:
        global COUNT_PM
        if e.is_private and not (await e.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
            except:
                return
            apprv = is_approved(e.chat_id)

            if not apprv and e.text != \
                ("`Bleep Blop! This is a Bot. Don't fret. \n\n`"
                 "`My Master hasn't approved you to PM.`. \n\n"
                 "`If You Are Hater then Maderchod Maa Chudao Bhosdike MaderHod`\n\n"
                 "`Currently i'm offline you can get help in` @zonerschat join @mkzone For new Bins\n\n"
                 "`If You Are One Of My Friends Kindly Wait Till Me Come Online.`"):

                await e.reply(
                    "`Bleep Blop! This is a Bot. Don't fret. \n\n`"
                    "`If You Are human join Anie bot support chat @AnieRoSupport` \n\n"
                    "`If You Are One Of My Friends Kindly Wait Till Me Come Online.`\n\n"
                    "`As far as i know, he doesn't usually approve Retards.`"
                )

                if NOTIF_OFF:
                    await e.client.send_read_acknowledge(e.chat_id)
                if e.chat_id not in COUNT_PM:
                    COUNT_PM.update({e.chat_id: 1})
                else:
                    COUNT_PM[e.chat_id] = COUNT_PM[e.chat_id] + 1
                if COUNT_PM[e.chat_id] > 3:
                    await e.respond(
                        "`You were spamming my Master's PM, which I don't like.`"
                        "`Reported Spam Of This MaderChod.`"
                    )
                    del COUNT_PM[e.chat_id]
                    await e.client(BlockRequest(e.chat_id))
                    await e.client(ReportSpamRequest(peer=e.chat_id))
                    if LOGGER:
                        name = await e.client.get_entity(e.chat_id)
                        name0 = str(name.first_name)
                        await e.client.send_message(
                            LOGGER_GROUP,
                            "["
                            + name0
                            + "](tg://user?id="
                            + str(e.chat_id)
                            + ")"
                            + " was just another retarded nibba",
                        )



@register(outgoing=True, pattern="^.notifoff$")
async def notifoff(e):
    global NOTIF_OFF
    NOTIF_OFF = True
    await e.edit("`Notifications silenced!`")


@register(outgoing=True, pattern="^.notifon$")
async def notifon(e):
    global NOTIF_OFF
    NOTIF_OFF = False
    await e.edit("`Notifications unmuted!`")


@register(outgoing=True, pattern="^.pm$")
async def approvepm(apprvpm):
    if not apprvpm.text[0].isalpha() and apprvpm.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.pm_permit_sql import approve
        except:
            await apprvpm.edit("`Running on Non-SQL mode!`")
            return

        if apprvpm.reply_to_msg_id:
            reply = await apprvpm.get_reply_message()
            replied_user = await apprvpm.client(GetFullUserRequest(reply.from_id))
            aname = replied_user.user.id
            name0 = str(replied_user.user.first_name)
            approve(replied_user.user.id)
        else:
            approve(apprvpm.chat_id)
            aname = await apprvpm.client.get_entity(apprvpm.chat_id)
            name0 = str(aname.first_name)

        await apprvpm.edit(
            f"[{name0}](tg://user?id={apprvpm.chat_id}) `User Approved to PM!`"
            )
        await apprvpm.delete()

        if LOGGER:
            await apprvpm.client.send_message(
                LOGGER_GROUP,
                f"[{name0}](tg://user?id={apprvpm.chat_id})"
                "Was Approved to PM you.",
            )

@register(outgoing=True, pattern="^.dis$")
async def disapprovepm(disapprvpm):
    if not disapprvpm.text[0].isalpha() and disapprvpm.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.pm_permit_sql import dissprove
        except:
            await disapprvpm.edit("`Running on Non-SQL mode!`")
            return

        if disapprvpm.reply_to_msg_id:
            reply = await disapprvpm.get_reply_message()
            replied_user = await disapprvpm.client(GetFullUserRequest(reply.from_id))
            aname = replied_user.user.id
            name0 = str(replied_user.user.first_name)
            dissprove(replied_user.user.id)
        else:
            dissprove(disapprvpm.chat_id)
            aname = await disapprvpm.client.get_entity(disapprvpm.chat_id)
            name0 = str(aname.first_name)

        await disapprvpm.edit(
            f"[{name0}](tg://user?id={disapprvpm.chat_id}) `Nub Nimba disapproved to PM KEK!`"
            )

        if LOGGER_GROUP:
            await disapprvpm.client.send_message(
                LOGGER_GROUP,
                f"[{name0}](tg://user?id={disapprvpm.chat_id})"
                " was disapproved to PM you.",
            )

@register(outgoing=True, pattern="^.b$")
async def blockpm(block):
    if not block.text[0].isalpha() and block.text[0] not in ("/", "#", "@", "!"):

        await block.edit("`You are gonna be blocked from PM-ing my Master!`")

        if block.reply_to_msg_id:
            reply = await block.get_reply_message()
            replied_user = await block.client(GetFullUserRequest(reply.from_id))
            aname = replied_user.user.id
            name0 = str(replied_user.user.first_name)
            await block.client(BlockRequest(replied_user.user.id))
            try:
                from userbot.modules.sql_helper.pm_permit_sql import dissprove
                dissprove(replied_user.user.id)
            except Exception:
                pass
        else:
            await block.client(BlockRequest(block.chat_id))
            aname = await block.client.get_entity(block.chat_id)
            name0 = str(aname.first_name)
            try:
                from userbot.modules.sql_helper.pm_permit_sql import dissprove
                dissprove(block.chat_id)
            except Exception:
                pass

        if LOGGER:
            await block.client.send_message(
                LOGGER_GROUP,
                f"[{name0}](tg://user?id={block.chat_id})"
                " was blocked.",
            )


@register(outgoing=True, pattern="^.ub$")
async def unblockpm(unblock):
    if not unblock.text[0].isalpha() and unblock.text[0] \
            not in ("/", "#", "@", "!") and unblock.reply_to_msg_id:

        await unblock.edit("`My Master has forgiven you to PM now`")

        if unblock.reply_to_msg_id:
            reply = await unblock.get_reply_message()
            replied_user = await unblock.client(GetFullUserRequest(reply.from_id))
            name0 = str(replied_user.user.first_name)
            await unblock.client(UnblockRequest(replied_user.user.id))

        if LOGGER:
            await unblock.client.send_message(
                LOGGER_GROUP,
                f"[{name0}](tg://user?id={unblock.chat_id})"
                " was unblocc'd!.",
            )

CMD_HELP.update(
    {
        "pm": """
『 **PM OPTIONS** 』
  `.ub`  -> Unblock User From Your PM.
  `.notifon`  -> Notification Turned On.
  `.notifoff -> Notification Turned Off.
  `.pm` -> Allows a user to PM you.
  `.b` -> Block a user to PM you.
  """
    }
)
