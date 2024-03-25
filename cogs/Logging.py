'''
Server Logs
'''

import discord
from discord.ext import commands, tasks
import json
import asyncio
import re
import motor.motor_asyncio
import nest_asyncio
import datetime
import os
import time
import emojis

nest_asyncio.apply()
cluster = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb_cluster_id")
modlogsdb = cluster["modlogs"]["modlogs"]
invitetrack = cluster["modlogs"]["invitetrack"]


# modlogs , invite logs , member logs , message logs
async def getmodlogschannel(ctx, client, view):
    embed = discord.Embed(colour=discord.Colour.purple(),
                          description="Enter the channel where you want to set Mod Logs")
    msg = await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        channelinput = await client.wait_for("message", timeout=120, check=check)
    except:
        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
        await msg.edit(embed=embed)
        return "timeout"
    try:
        channel = await commands.TextChannelConverter().convert(ctx, channelinput.content)
    except:
        return "invalid channel"

    return channel


async def getmessagelogschannel(ctx, client, view):
    embed = discord.Embed(colour=discord.Colour.purple(),
                          description="Enter the channel where you want to set Message Logs")
    msg = await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        channelinput = await client.wait_for("message", timeout=120, check=check)
    except:
        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
        await msg.edit(embed=embed)
        return "timeout"
    try:
        channel = await commands.TextChannelConverter().convert(ctx, channelinput.content)
    except:
        return "invalid channel"

    return channel


async def getmemlogschannel(ctx, client, view):
    embed = discord.Embed(colour=discord.Colour.purple(),
                          description="Enter the channel where you want to set Member Logs")
    msg = await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        channelinput = await client.wait_for("message", timeout=120, check=check)
    except:
        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
        await msg.edit(embed=embed)
        return "timeout"
    try:
        channel = await commands.TextChannelConverter().convert(ctx, channelinput.content)
    except:
        return "invalid channel"

    return channel

async def getmemjoinlogschannel(ctx, client, view):
    embed = discord.Embed(colour=discord.Colour.purple(),
                          description="Enter the channel where you want to set Member Join Logs")
    msg = await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        channelinput = await client.wait_for("message", timeout=120, check=check)
    except:
        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
        await msg.edit(embed=embed)
        return "timeout"
    try:
        channel = await commands.TextChannelConverter().convert(ctx, channelinput.content)
    except:
        return "invalid channel"

    return channel

async def getinvlogschannel(ctx, client, view):
    embed = discord.Embed(colour=discord.Colour.purple(),
                          description="Enter the channel where you want to set Invite Logs")
    msg = await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        channelinput = await client.wait_for("message", timeout=120, check=check)
    except:
        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
        await msg.edit(embed=embed)
        return "timeout"
    try:
        channel = await commands.TextChannelConverter().convert(ctx, channelinput.content)
    except:
        return "invalid channel"

    return channel


class modlogs(discord.ui.Button['Logs']):

    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.primary, label="Mod Logs", row=1)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Logs = self.view
        if interaction.user != self.ctx.author:
            return
        if view.modlogs == 1:
            view.modlogs = 0
            emoji = "<:toggle0:859707856370401280>"
        else:
            view.modlogs = 1
            emoji = "<:toggle1:859707856381935657>"
        view.fields[0] = ("Mod Logs", f"    {emoji}", True)
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await interaction.response.edit_message(embed=embed, view=view)


class msglogs(discord.ui.Button['Logs']):

    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.danger, label="Message Logs", row=1)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Logs = self.view
        if interaction.user != self.ctx.author:
            return
        if view.msglogs == 1:
            view.msglogs = 0
            emoji = "<:toggle0:859707856370401280>"
        else:
            view.msglogs = 1
            emoji = "<:toggle1:859707856381935657>"
        view.fields[1] = ("Message Logs\u0020\u0020\u0020\u0020", emoji, True)
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await interaction.response.edit_message(embed=embed, view=view)


class memlogs(discord.ui.Button['Logs']):

    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.success, label="Member Logs", row=1)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Logs = self.view
        if interaction.user != self.ctx.author:
            return
        if view.memlogs == 1:
            view.memlogs = 0
            emoji = "<:toggle0:859707856370401280>"
        else:
            view.memlogs = 1
            emoji = "<:toggle1:859707856381935657>"
        view.fields[2] = ("Member Logs\u0020\u0020\u0020\u0020", emoji, True)
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await interaction.response.edit_message(embed=embed, view=view)
class memjoinlogs(discord.ui.Button['Logs']):

    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.blurple, label="Member Join Logs", row=1)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Logs = self.view
        if interaction.user != self.ctx.author:
            return
        if view.memjoinlogs == 1:
            view.memjoinlogs = 0
            emoji = "<:toggle0:859707856370401280>"
        else:
            view.memjoinlogs = 1
            emoji = "<:toggle1:859707856381935657>"
        view.fields[3] = ("Member Join Logs\u0020\u0020\u0020\u0020", emoji, True)
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await interaction.response.edit_message(embed=embed, view=view)

class invlogs(discord.ui.Button['Logs']):

    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.secondary, label="Invite Logs", row=2)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Logs = self.view
        if interaction.user != self.ctx.author:
            return
        if view.invlogs == 1:
            view.invlogs = 0
            emoji = "<:toggle0:859707856370401280>"
        else:
            view.invlogs = 1
            emoji = "<:toggle1:859707856381935657>"
        view.fields[4] = ("Invite Logs\u0020\u0020\u0020\u0020", emoji, True)
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await interaction.response.edit_message(embed=embed, view=view)


class Done(discord.ui.Button['Logs']):
    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.primary, label="Done", row=2)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Logs = self.view
        if interaction.user != self.ctx.author:
            return
        if view.modlogs == 0 and view.msglogs == 0 and view.invlogs == 0 and view.memlogs == 0 and view.memjoinlogs == 0:
            embed = discord.Embed(colour=discord.Colour.purple(),
                                  description="No Logs Type Chosen.\n\nU can use the same command to setlogs if you wish to setup logs lateron")
            await interaction.response.edit_message(embed=embed)
            return
        view.stop()
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Alright Let's setup the Logs for your server!")
        await interaction.response.edit_message(embed=embed)

        c = view.modlogs + view.invlogs + view.msglogs + view.memlogs + view.memjoinlogs
        checkmod = 0
        checkmsg = 0
        checkinv = 0
        checkmem = 0
        checkmemjoin = 0
        dict = {"guildid": str(self.ctx.guild.id), "modlogs": 0, "msglogs": 0, "memlogs": 0, "memjoinlogs":0,"invlogs": 0}
        if view.modlogs == 1:
            input = await getmodlogschannel(self.ctx, view.client, view)
            if input == "invalid channel":
                if c == 1:
                    desc = "Invalid Channel Entered. Logs Setup Cancelled.\n\nRestart from the beginning and enter correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)

                    return
                else:
                    desc = "Invalid Channel Entered. Ignoring this input"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    checkmod = 2  # failed
            elif input == "timeout":
                return
            else:  # append to db
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Mod Logs have been setup successfully in {input.mention}")
                await self.ctx.send(embed=embed)
                dict["modlogs"] = 1
                dict["modlogschannelid"] = input.id
                checkmod = 1
        if view.msglogs == 1:
            input = await getmessagelogschannel(self.ctx, view.client, view)
            if input == "invalid channel":
                if c == 1:
                    desc = "Invalid Channel Entered. Logs Setup Cancelled.\n\nRestart from the beginning and enter correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)

                    return
                elif c == 2:
                    desc = "Invalid Channel Entered. Ignoring this input. Message Logs were not able to setup. you can use `>updatelogs` command to add Message Logs by entering correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    if checkmod != 1:
                        return
                    else:
                        await modlogsdb.insert_one(dict)
                        return

                else:
                    desc = "Invalid Channel Entered. Ignoring this input. You can use `>updatelogs` command lateron to setup Message Logs by entering a correct channel next time."
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    checkmsg = 2  # failed
            elif input == "timeout":
                if checkmod != 1:
                    return
                else:
                    await modlogsdb.insert_one(dict)
                    return

            else:
                # append to db
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Message Logs have been setup successfully in {input.mention}")
                await self.ctx.send(embed=embed)
                dict["msglogs"] = 1
                dict["msglogschannelid"] = input.id
                checkmsg = 1

        if view.memlogs == 1:
            input = await getmemlogschannel(self.ctx, view.client, view)
            if input == "invalid channel":
                if c == 1:
                    desc = "Invalid Channel Entered. Logs Setup Cancelled.\n\nRestart from the beginning and enter correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)

                    return
                elif c == 2 or c == 3:
                    desc = "Invalid Channel Entered. Ignoring this input. Member Logs were not able to setup. you can use `>updatelogs` command to setup Member Logs by entering correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    if checkmod == 1 or checkmsg == 1:
                        await modlogsdb.insert_one(dict)
                    return
                else:
                    desc = "Invalid Channel Entered. Ignoring this input. You can use `>updatelogs` command lateron to setup Member Logs by entering a correct channel next time."
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    checkmem = 2
            elif input == "timeout":
                if checkmod == 1 or checkmsg == 1:
                    await modlogsdb.insert_one(dict)
                return
            else:
                # append to db
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Member Logs have been setup successfully in {input.mention}")
                await self.ctx.send(embed=embed)
                dict["memlogs"] = 1
                dict["memlogschannelid"] = input.id
                checkmem = 1
        if view.memjoinlogs == 1:
            input = await getmemjoinlogschannel(self.ctx, view.client, view)
            if input == "invalid channel":
                if c == 1:
                    desc = "Invalid Channel Entered. Logs Setup Cancelled.\n\nRestart from the beginning and enter correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)

                    return
                elif c == 2 or c == 3 or c==4:
                    desc = "Invalid Channel Entered. Ignoring this input. Member Join Logs were not able to setup. you can use `>updatelogs` command to setup Member Join Logs by entering correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    if checkmod == 1 or checkmsg == 1 or checkmem ==1:
                        await modlogsdb.insert_one(dict)
                    return
                else:
                    desc = "Invalid Channel Entered. Ignoring this input. You can use `>updatelogs` command lateron to setup Member Join Logs by entering a correct channel next time."
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    checkmemjoin = 2
            elif input == "timeout":
                if checkmod == 1 or checkmsg == 1 or checkmem == 1:
                    await modlogsdb.insert_one(dict)
                return
            else:
                # append to db
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Member Join Logs have been setup successfully in {input.mention}")
                await self.ctx.send(embed=embed)
                dict["memjoinlogs"] = 1
                dict["memjoinlogschannelid"] = input.id
                checkmemjoin= 1
        if view.invlogs == 1:
            perms  = self.ctx.channel.permissions_for(self.ctx.me)
            tempperms =[]
            for i in iter(perms):
                if i[1]==True:
                    tempperms.append(i[0])
            check = False
            if "manage_guild" in tempperms:
                check = True
            
            if check != True:
                if checkmod == 1 or checkmsg == 1 or checkmem == 1 or checkmemjoin==1:
                    await modlogsdb.insert_one(dict)
                embed = discord.Embed(colour=discord.Colour.purple(),description = "I need to have Manage Server Permission for Invite Logs. Make sure i have that permission before trying to setup Invite Logs again.")
                return await ctx.send(embed = embed)
            input = await getinvlogschannel(self.ctx, view.client, view)
            if input == "invalid channel":
                if c == 1:
                    desc = "Invalid Channel Entered. Logs Setup Cancelled.\n\nRestart from the beginning and enter correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)

                    return
                elif c == 2 or c == 3 or c == 4 or c==5:
                    desc = "Invalid Channel Entered. Ignoring this input. Invite Logs were not able to setup. you can use `>updatelogs` command to setup Invite Logs by entering correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    if checkmod == 1 or checkmsg == 1 or checkmem == 1 or checkmemjoin ==1:
                        await modlogsdb.insert_one(dict)
                    return
            elif input == "timeout":
                if checkmod == 1 or checkmsg == 1 or checkmem == 1 or checkmemjoin==1:
                    await modlogsdb.insert_one(dict)
                return
            else:
                # append to db
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Invite Logs have been setup successfully in {input.mention}")
                await self.ctx.send(embed=embed)
                dict["invlogs"] = 1
                dict["invlogschannelid"] = input.id
                checkinv = 1

        if view.modlogs == 0 and view.msglogs == 0 and view.memlogs == 0 and view.invlogs == 0 and view.checkmemjoin==0:
            return
        # if (checkmod==2 and view.modlogs==1) and (checkmsg==2 and view.msglogs==1) and (checkmem==2 and view.memlogs==1) and (checkinv==2 and view.invlogs==1):
        #     embed = discord.Embed(colour=discord.Colour.purple(),description="None of the Logs were able to setup as all the inputs entered were incorrect.\n\nYou can use this command again if you wish to setup logs lateron and enter correct channels next time.")
        #     await self.ctx.send(embed=embed)

        await modlogsdb.insert_one(dict)
        if checkinv ==1:

            invitesall = await self.ctx.guild.invites()
            invitesdict = {}
            for i in invitesall:
                invitesdict[i.id]=i.uses
            invites = {
                "guildid":str(self.ctx.guild.id),
                "invites" : invitesdict
            }
            await invitetrack.insert_one(invites)

        return


class Logs(discord.ui.View):
    def __init__(self, ctx, client):
        super().__init__()
        self.ctx = ctx
        self.client = client
        self.modlogs = 0
        self.invlogs = 0
        self.memlogs = 0
        self.msglogs = 0
        self.memjoinlogs = 0
        self.fields = [
            ("Mod Logs\u0020\u0020\u0020\u0020", "<:toggle0:859707856370401280>", True),
            ("Message Logs\u0020\u0020\u0020\u0020", "<:toggle0:859707856370401280>", True),
            ("Member Logs\u0020\u0020\u0020\u0020", "<:toggle0:859707856370401280>", True),
            ("Member Join Logs\u0020\u0020\u0020\u0020", "<:toggle0:859707856370401280>", True),
            ("Invite Logs\u0020\u0020\u0020\u0020", "<:toggle0:859707856370401280>", True)
        ]
        self.add_item(modlogs(self.ctx))
        self.add_item(msglogs(self.ctx))
        self.add_item(memlogs(self.ctx))
        self.add_item(memjoinlogs(self.ctx))
        self.add_item(invlogs(self.ctx))
        self.add_item(Done(self.ctx))


# ---------------update logs---------------------
class upmodlogs(discord.ui.Button['UpdateLogs']):

    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.primary, label="Mod Logs", row=1)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: UpdateLogs = self.view
        if interaction.user != self.ctx.author:
            return
        if view.modlogs == 1:
            view.modlogs = 0
            emoji = "<:toggle0:859707856370401280>"
        else:
            view.modlogs = 1
            emoji = "<:toggle1:859707856381935657>"
        view.fields[0] = ("Mod Logs", f"    {emoji}", True)
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await interaction.response.edit_message(embed=embed, view=view)


class upmsglogs(discord.ui.Button['UpdateLogs']):

    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.danger, label="Message Logs", row=1)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: UpdateLogs = self.view
        if interaction.user != self.ctx.author:
            return
        if view.msglogs == 1:
            view.msglogs = 0
            emoji = "<:toggle0:859707856370401280>"
        else:
            view.msglogs = 1
            emoji = "<:toggle1:859707856381935657>"
        view.fields[1] = ("Message Logs\u0020\u0020\u0020\u0020", emoji, True)
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await interaction.response.edit_message(embed=embed, view=view)


class upmemlogs(discord.ui.Button['UpdateLogs']):

    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.success, label="Member Logs", row=1)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: UpdateLogs = self.view
        if interaction.user != self.ctx.author:
            return
        if view.memlogs == 1:
            view.memlogs = 0
            emoji = "<:toggle0:859707856370401280>"
        else:
            view.memlogs = 1
            emoji = "<:toggle1:859707856381935657>"
        view.fields[2] = ("Member Logs\u0020\u0020\u0020\u0020", emoji, True)
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await interaction.response.edit_message(embed=embed, view=view)
class upmemjoinlogs(discord.ui.Button['UpdateLogs']):

    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.blurple, label="Member Join Logs", row=1)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: UpdateLogs = self.view
        if interaction.user != self.ctx.author:
            return
        if view.memjoinlogs == 1:
            view.memjoinlogs = 0
            emoji = "<:toggle0:859707856370401280>"
        else:
            view.memjoinlogs = 1
            emoji = "<:toggle1:859707856381935657>"
        view.fields[3] = ("Member Join Logs\u0020\u0020\u0020\u0020", emoji, True)
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await interaction.response.edit_message(embed=embed, view=view)

class upinvlogs(discord.ui.Button['UpdateLogs']):

    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.secondary, label="Invite Logs", row=2)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: UpdateLogs = self.view
        if interaction.user != self.ctx.author:
            return
        if view.invlogs == 1:
            view.invlogs = 0
            emoji = "<:toggle0:859707856370401280>"
        else:
            view.invlogs = 1
            emoji = "<:toggle1:859707856381935657>"
        view.fields[4] = ("Invite Logs\u0020\u0020\u0020\u0020", emoji, True)
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await interaction.response.edit_message(embed=embed, view=view)


class upDone(discord.ui.Button['Logs']):
    def __init__(self, ctx):
        super().__init__(style=discord.ButtonStyle.primary, label="Done", row=2)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: UpdateLogs = self.view
        if interaction.user != self.ctx.author:
            return
        view.stop()
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in view.fields:
            embed.add_field(name=name, value=value, inline=inline)
        modlogscheckup = ""
        msglogscheckup = ""
        memlogscheckup = ""
        memjoinlogscheckup = ""
        invlogscheckup = ""

        c = 0
        dict = view.dict
        if view.modlogs != view.modlogsconst:
            modlogscheckup = "Mod Logs"
            c += 1
            if view.modlogs == 0:
                dict['modlogs'] = 0
                dict.pop('modlogschannelid')
        if view.msglogs != view.msglogsconst:
            msglogscheckup = "Message Logs"
            c += 1
            if view.msglogs == 0:
                dict['msglogs'] = 0
                dict.pop('msglogschannelid')
        if view.memlogs != view.memlogsconst:
            memlogscheckup = "Member Logs"
            c += 1
            if view.memlogs == 0:
                dict['memlogs'] = 0
                dict.pop('memlogschannelid')
        if view.memjoinlogs != view.memjoinlogsconst:
            memjoinlogscheckup = "Member Join Logs"
            c += 1
            if view.memjoinlogs == 0:
                dict['memjoinlogs'] = 0
                dict.pop('memjoinlogschannelid')
        if view.invlogs != view.invlogsconst:
            invlogscheckup = "Invite Logs"
            c += 1
            if view.invlogs == 0:
                dict['invlogs'] = 0
                dict.pop('invlogschannelid')

        if c == 0:
            if view.modlogs == 0 and view.msglogs == 0 and view.invlogs == 0 and view.memlogs == 0 and view.memjoinlogs==0:
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description="No Changes Observed.\n\nTo change the channel use `>updatechannel[logtype] [newchannel]`")
                await interaction.response.edit_message(embed=embed)
                return
        embed.set_footer(
            text=f"Changes observed in {modlogscheckup}{',' if modlogscheckup != '' else ' '} {msglogscheckup}{',' if msglogscheckup != '' else ' '} {memlogscheckup}{',' if memlogscheckup != '' else ' '} {memjoinlogscheckup}{',' if memjoinlogscheckup != '' else ' '} {invlogscheckup}")
        await interaction.response.edit_message(embed=embed)

        checkmod = 0
        checkmsg = 0
        checkinv = 0
        checkmem = 0
        checkmemjoin = 0

        if view.modlogs == 1 and not view.modlogsconst == 1:
            input = await getmodlogschannel(self.ctx, view.client, view)
            if input == "invalid channel":
                if c == 1:
                    desc = "Invalid Channel Entered. Logs Setup Cancelled.\n\nRestart from the beginning and enter correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)

                    return
                else:
                    desc = "Invalid Channel Entered. Ignoring this input"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    checkmod = 2  # failed
            elif input == "timeout":
                return
            else:  # append to db
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Mod Logs have been setup successfully in {input.mention}")
                await self.ctx.send(embed=embed)
                dict["modlogs"] = 1
                dict["modlogschannelid"] = input.id
                checkmod = 1
        if view.msglogs == 1 and not view.msglogsconst == 1:
            input = await getmessagelogschannel(self.ctx, view.client, view)
            if input == "invalid channel":
                if c == 1:
                    desc = "Invalid Channel Entered. Logs Setup Cancelled.\n\nRestart from the beginning and enter correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)

                    return
                elif c == 2:
                    desc = "Invalid Channel Entered. Ignoring this input. Message Logs were not able to setup. you can use `>updatelogs` command to add Message Logs by entering correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    if checkmod != 1:
                        return
                    else:
                        await modlogsdb.replace_one({"guildid": str(view.ctx.guild.id)}, dict)
                        return

                else:
                    desc = "Invalid Channel Entered. Ignoring this input. You can use `>updatelogs` command lateron to setup Message Logs by entering a correct channel next time."
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    checkmsg = 2  # failed
            elif input == "timeout":
                if checkmod != 1:
                    return
                else:
                    await modlogsdb.replace_one({"guildid": str(view.ctx.guild.id)}, dict)
                    return

            else:
                # append to db
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Message Logs have been setup successfully in {input.mention}")
                await self.ctx.send(embed=embed)
                dict["msglogs"] = 1
                dict["msglogschannelid"] = input.id
                checkmsg = 1

        if view.memlogs == 1 and not view.memlogsconst == 1:
            input = await getmemlogschannel(self.ctx, view.client, view)
            if input == "invalid channel":
                if c == 1:
                    desc = "Invalid Channel Entered. Logs Setup Cancelled.\n\nRestart from the beginning and enter correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)

                    return
                elif c == 2 or c == 3:
                    desc = "Invalid Channel Entered. Ignoring this input. Member Logs were not able to setup. you can use `>updatelogs` command to setup Member Logs by entering correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    if checkmod == 1 or checkmsg == 1:
                        await modlogsdb.replace_one({"guildid": str(view.ctx.guild.id)}, dict)
                    return
                else:
                    desc = "Invalid Channel Entered. Ignoring this input. You can use `>updatelogs` command lateron to setup Member Logs by entering a correct channel next time."
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    checkmem = 2
            elif input == "timeout":
                if checkmod == 1 or checkmsg == 1:
                    await modlogsdb.replace_one({"guildid": str(view.ctx.guild.id)}, dict)
                return
            else:
                # append to db
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Member Logs have been setup successfully in {input.mention}")
                await self.ctx.send(embed=embed)
                dict["memlogs"] = 1
                dict["memlogschannelid"] = input.id
                checkmem = 1
        if view.memjoinlogs == 1 and not view.memjoinlogsconst == 1:
            input = await getmemjoinlogschannel(self.ctx, view.client, view)
            if input == "invalid channel":
                if c == 1:
                    desc = "Invalid Channel Entered. Logs Setup Cancelled.\n\nRestart from the beginning and enter correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)

                    return
                elif c == 2 or c == 3 or c==4:
                    desc = "Invalid Channel Entered. Ignoring this input. Member Join Logs were not able to setup. you can use `>updatelogs` command to setup Member Join Logs by entering correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    if checkmod == 1 or checkmsg == 1 or checkmem ==1:
                        await modlogsdb.replace_one({"guildid": str(view.ctx.guild.id)}, dict)
                    return
                else:
                    desc = "Invalid Channel Entered. Ignoring this input. You can use `>updatelogs` command lateron to setup Member Join Logs by entering a correct channel next time."
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    checkmemjoin = 2
            elif input == "timeout":
                if checkmod == 1 or checkmsg == 1 or checkmem ==1:
                    await modlogsdb.replace_one({"guildid": str(view.ctx.guild.id)}, dict)
                return
            else:
                # append to db
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Member Join Logs have been setup successfully in {input.mention}")
                await self.ctx.send(embed=embed)
                dict["memjoinlogs"] = 1
                dict["memjoinlogschannelid"] = input.id
                checkmemjoin = 1
        if view.invlogs == 1 and not view.invlogsconst == 1:
            perms  = self.ctx.channel.permissions_for(self.ctx.me)
            tempperms =[]
            for i in iter(perms):
                if i[1]==True:
                    tempperms.append(i[0])
            check = False
            if "manage_guild" in tempperms:
                check = True
            
            if check != True:
                if checkmod == 1 or checkmsg == 1 or checkmem == 1 or checkmemjoin==1:
                    await modlogsdb.replace_one({"guildid": str(view.ctx.guild.id)}, dict)
                embed = discord.Embed(colour=discord.Colour.purple(),description = "I need to have Manage Server Permission for Invite Logs. Make sure i have that permission before trying to setup Invite Logs again.")
                return await ctx.send(embed = embed)
            input = await getinvlogschannel(self.ctx, view.client, view)
            if input == "invalid channel":
                if c == 1:
                    desc = "Invalid Channel Entered. Logs Setup Cancelled.\n\nRestart from the beginning and enter correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)

                    return
                elif c == 2 or c == 3 or c == 4 or c==5:
                    desc = "Invalid Channel Entered. Ignoring this input. Invite Logs were not able to setup. you can use `>updatelogs` command to setup Invite Logs by entering correct channel next time"
                    embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
                    await self.ctx.send(embed=embed)
                    if checkmod == 1 or checkmsg == 1 or checkmem == 1 or checkmemjoin ==1:
                        await modlogsdb.replace_one({"guildid": str(view.ctx.guild.id)}, dict)
                    return
            elif input == "timeout":
                if checkmod == 1 or checkmsg == 1 or checkmem == 1 or checkmemjoin ==1:
                    await modlogsdb.replace_one({"guildid": str(view.ctx.guild.id)}, dict)
                return
            else:
                # append to db
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Invite Logs have been setup successfully in {input.mention}")
                await self.ctx.send(embed=embed)
                dict["invlogs"] = 1
                dict["invlogschannelid"] = input.id
                checkinv = 1

        if view.modlogs == 0 and view.msglogs == 0 and view.memlogs == 0 and view.invlogs == 0 and view.memjoinlogs==0:
            return
        # if (checkmod==2 and view.modlogs==1) and (checkmsg==2 and view.msglogs==1) and (checkmem==2 and view.memlogs==1) and (checkinv==2 and view.invlogs==1):
        #     embed = discord.Embed(colour=discord.Colour.purple(),description="None of the Logs were able to setup as all the inputs entered were incorrect.\n\nYou can use this command again if you wish to setup logs lateron and enter correct channels next time.")
        #     await self.ctx.send(embed=embed)

        await modlogsdb.replace_one({"guildid": str(view.ctx.guild.id)}, dict)
        if checkinv ==1:
            invitesall = await self.ctx.guild.invites()
            invitesdict = {}
            for i in invitesall:
                invitesdict[i.id]=i.uses
            invites = {
                "guildid":str(self.ctx.guild.id),
                "invites" : invitesdict
            }

            await invitetrack.insert_one(invites)
        return


class UpdateLogs(discord.ui.View):
    def __init__(self, ctx, client, modlogs, invlogs, memlogs, msglogs,memjoinlogs, dict):
        super().__init__()
        self.ctx = ctx
        self.client = client

        self.dict = dict
        self.modlogsconst = modlogs
        self.invlogsconst = invlogs
        self.memlogsconst = memlogs
        self.memjoinlogsconst = memjoinlogs
        self.msglogsconst = msglogs
        self.modlogs = modlogs
        self.invlogs = invlogs
        self.memlogs = memlogs
        self.memjoinlogs = memjoinlogs
        self.msglogs = msglogs
        emojidict = {1: "<:toggle1:859707856381935657>", 0: "<:toggle0:859707856370401280>"}
        self.fields = [
            ("Mod Logs\u0020\u0020\u0020\u0020", emojidict[self.modlogs], True),
            ("Message Logs\u0020\u0020\u0020\u0020", emojidict[self.msglogs], True),
            ("Member Logs\u0020\u0020\u0020\u0020", emojidict[self.memlogs], True),
            ("Member Join Logs\u0020\u0020\u0020\u0020", emojidict[self.memjoinlogs], True),
            ("Invite Logs\u0020\u0020\u0020\u0020", emojidict[self.invlogs], True)
        ]
        self.add_item(upmodlogs(self.ctx))
        self.add_item(upmsglogs(self.ctx))
        self.add_item(upmemlogs(self.ctx))
        self.add_item(upmemjoinlogs(self.ctx))
        self.add_item(upinvlogs(self.ctx))
        self.add_item(upDone(self.ctx))


class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Sets up Logs in the Server")
    @commands.has_permissions(manage_guild=True)
    async def setlogs(self, ctx):
        count = await modlogsdb.count_documents({"guildid": str(ctx.guild.id)})

        if count != 0:
            embed = discord.Embed(colour=discord.Colour.purple(),
                                  description="Logs are already setup on your server .\nUse `>showlogs` command to see which logs are enabled in the server\n Use `>updatelogs` command or other specific update logs commands to update the logs.")
            return await ctx.send(embed=embed)
        fields = [
            ("Mod Logs", "<:toggle0:859707856370401280>", True),
            ("Message Logs", "<:toggle0:859707856370401280>", True),
            ("Member Logs", "<:toggle0:859707856370401280>", True),
            ("Member Join Logs", "<:toggle0:859707856370401280>", True),
            ("Invite Logs", "<:toggle0:859707856370401280>", True)
        ]
        embed = discord.Embed(colour=discord.Colour.purple())
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await ctx.send(embed=embed, view=Logs(ctx, self.client))

    @commands.command(aliases = ['logs'],description="Shows the logs setup in the server")
    @commands.has_permissions(manage_guild=True)
    async def showlogs(self, ctx):
        count = await modlogsdb.count_documents({"guildid": str(ctx.guild.id)})
        if count == 0:
            embed = discord.Embed(colour=discord.Colour.purple(),
                                  description="Logs are not setup on your server . Use `>setlogs` command to set logs before using this cmd")
            return await ctx.send(embed=embed)
        data = modlogsdb.find({"guildid": str(ctx.guild.id)})
        embed = discord.Embed(colour=discord.Colour.purple())
        async for x in data:
            if x["modlogs"] == 1:
                embed.add_field(name="Mod Logs", value=f"<:toggle1:859707856381935657>\n<#{x['modlogschannelid']}>")
            else:
                embed.add_field(name="Mod Logs", value=f"<:toggle0:859707856370401280>")
            if x["msglogs"] == 1:
                embed.add_field(name="Message Logs", value=f"<:toggle1:859707856381935657>\n<#{x['msglogschannelid']}>")
            else:
                embed.add_field(name="Message Logs", value=f"<:toggle0:859707856370401280>")
            if x["memlogs"] == 1:
                embed.add_field(name="Member Logs", value=f"<:toggle1:859707856381935657>\n<#{x['memlogschannelid']}>")
            else:
                embed.add_field(name="Member Logs", value=f"<:toggle0:859707856370401280>")
            if x["memjoinlogs"] == 1:
                embed.add_field(name="Member Join Logs", value=f"<:toggle1:859707856381935657>\n<#{x['memjoinlogschannelid']}>")
            else:
                embed.add_field(name="Member Join Logs", value=f"<:toggle0:859707856370401280>")
            if x["invlogs"] == 1:
                embed.add_field(name="Invite Logs", value=f"<:toggle1:859707856381935657>\n<#{x['invlogschannelid']}>")
            else:
                embed.add_field(name="Invite Logs", value=f"<:toggle0:859707856370401280>")
        return await ctx.send(embed=embed)

    @commands.command(description="Updates Logs setup in the server. Use this cmd to toggle logs")
    @commands.has_permissions(manage_guild=True)
    async def updatelogs(self, ctx):
        data = modlogsdb.find({"guildid": str(ctx.guild.id)})
        embed = discord.Embed(colour=discord.Colour.purple())
        async for x in data:
            modlogs = x['modlogs']
            invlogs = x['invlogs']
            memlogs = x['memlogs']
            msglogs = x['msglogs']
            memjoinlogs = x['memjoinlogs']
            dict = x
            if x["modlogs"] == 1:
                embed.add_field(name="Mod Logs", value=f"<:toggle1:859707856381935657>\n<#{x['modlogschannelid']}>")
            else:
                embed.add_field(name="Mod Logs", value=f"<:toggle0:859707856370401280>")
            if x["msglogs"] == 1:
                embed.add_field(name="Message Logs", value=f"<:toggle1:859707856381935657>\n<#{x['msglogschannelid']}>")
            else:
                embed.add_field(name="Message Logs", value=f"<:toggle0:859707856370401280>")
            if x["memlogs"] == 1:
                embed.add_field(name="Member Logs", value=f"<:toggle1:859707856381935657>\n<#{x['memlogschannelid']}>")
            else:
                embed.add_field(name="Member Logs", value=f"<:toggle0:859707856370401280>")
            if x["memjoinlogs"] == 1:
                embed.add_field(name="Member Join Logs", value=f"<:toggle1:859707856381935657>\n<#{x['memjoinlogschannelid']}>")
            else:
                embed.add_field(name="Member Join Logs", value=f"<:toggle0:859707856370401280>")
            if x["invlogs"] == 1:
                embed.add_field(name="Invite Logs", value=f"<:toggle1:859707856381935657>\n<#{x['invlogschannelid']}>")
            else:
                embed.add_field(name="Invite Logs", value=f"<:toggle0:859707856370401280>")
        embed.set_footer(text="Click on the buttons below to toggle logs")
        await ctx.send(embed=embed, view=UpdateLogs(ctx, self.client, modlogs, invlogs, memlogs, msglogs,memjoinlogs, dict))

    @commands.command(description="Removes Logs from the server")
    @commands.has_permissions(manage_guild=True)
    async def dellogs(self, ctx):
        count = await modlogsdb.count_documents({"guildid": str(ctx.guild.id)})
        if count == 0:
            embed = discord.Embed(colour=discord.Colour.purple(),
                                  description="You need to set logs up before deleting them")
            return await ctx.send(embed=embed)
        await modlogsdb.delete_many({"guildid": str(ctx.guild.id)})
        await invitetrack.delete_many({"guildid":str(ctx.guild.id)})
        embed = discord.Embed(colour=discord.Colour.purple(),
                              description="Logs Deleted Successfully from this server")
        return await ctx.send(embed=embed)

    @commands.command(description="updates Mod logs channel to a new one")
    @commands.has_permissions(manage_guild=True)
    async def updatemodlogschannel(self, ctx, newchannel: discord.TextChannel):
        count = await modlogsdb.count_documents({"guildid": str(ctx.guild.id)})
        if count == 0:
            embed = discord.Embed(colour=discord.Colour.purple(),
                                  description="You need to set logs up before updating logs")
            return await ctx.send(embed=embed)
        data = modlogsdb.find({"guildid": str(ctx.guild.id)})
        async for x in data:
            if x['modlogs'] == 0:
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description="You need to set Mod Logs up before using this command. Use `>updatelogs` command to set Mod Logs through it")
                return await ctx.send(embed=embed)
            else:
                x['modlogschannelid'] = newchannel.id
                await modlogsdb.replace_one({"guildid": str(ctx.guild.id)}, x)
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Mod Logs successfully updated to {newchannel.mention}")
                return await ctx.send(embed=embed)

    @commands.command(description="updates Message logs channel to a new one")
    @commands.has_permissions(manage_guild=True)
    async def updatemsglogschannel(self, ctx, newchannel: discord.TextChannel):
        count = await modlogsdb.count_documents({"guildid": str(ctx.guild.id)})
        if count == 0:
            embed = discord.Embed(colour=discord.Colour.purple(),
                                  description="You need to set logs up before updating logs")
            return await ctx.send(embed=embed)
        data = modlogsdb.find({"guildid": str(ctx.guild.id)})
        async for x in data:
            if x['msglogs'] == 0:
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description="You need to set Message Logs up before using this command. Use `>updatelogs` command to set Message Logs through it")
                return await ctx.send(embed=embed)
            else:
                x['msglogschannelid'] = newchannel.id
                await modlogsdb.replace_one({"guildid": str(ctx.guild.id)}, x)
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Message Logs successfully updated to {newchannel.mention}")
                return await ctx.send(embed=embed)

    @commands.command(description="updates Member logs channel to a new one")
    @commands.has_permissions(manage_guild=True)
    async def updatememlogschannel(self, ctx, newchannel: discord.TextChannel):
        count = await modlogsdb.count_documents({"guildid": str(ctx.guild.id)})
        if count == 0:
            embed = discord.Embed(colour=discord.Colour.purple(),
                                  description="You need to set logs up before updating logs")
            return await ctx.send(embed=embed)
        data = modlogsdb.find({"guildid": str(ctx.guild.id)})
        async for x in data:
            if x['memlogs'] == 0:
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description="You need to set Member Logs up before using this command. Use `>updatelogs` command to set Member Logs through it")
                return await ctx.send(embed=embed)
            else:
                x['memlogschannelid'] = newchannel.id
                await modlogsdb.replace_one({"guildid": str(ctx.guild.id)}, x)
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Member Logs successfully updated to {newchannel.mention}")
                return await ctx.send(embed=embed)
    @commands.command(description="updates Member Join logs channel to a new one")
    @commands.has_permissions(manage_guild=True)
    async def updatememjoinlogschannel(self, ctx, newchannel: discord.TextChannel):
        count = await modlogsdb.count_documents({"guildid": str(ctx.guild.id)})
        if count == 0:
            embed = discord.Embed(colour=discord.Colour.purple(),
                                  description="You need to set logs up before updating logs")
            return await ctx.send(embed=embed)
        data = modlogsdb.find({"guildid": str(ctx.guild.id)})
        async for x in data:
            if x['memjoinlogs'] == 0:
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description="You need to set Member Join Logs up before using this command. Use `>updatelogs` command to set Member Join Logs through it")
                return await ctx.send(embed=embed)
            else:
                x['memjoinlogschannelid'] = newchannel.id
                await modlogsdb.replace_one({"guildid": str(ctx.guild.id)}, x)
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Member Join Logs successfully updated to {newchannel.mention}")
                return await ctx.send(embed=embed)
    @commands.command(description="updates invite logs channel to a new one")
    @commands.has_permissions(manage_guild=True)
    async def updateinvlogschannel(self, ctx, newchannel: discord.TextChannel):
        count = await modlogsdb.count_documents({"guildid": str(ctx.guild.id)})
        if count == 0:
            embed = discord.Embed(colour=discord.Colour.purple(),
                                  description="You need to set logs up before updating logs")
            return await ctx.send(embed=embed)
        data = modlogsdb.find({"guildid": str(ctx.guild.id)})
        async for x in data:
            if x['invlogs'] == 0:
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description="You need to set Invite Logs up before using this command. Use `>updatelogs` command to set Invite Logs through it")
                return await ctx.send(embed=embed)
            else:
                x['invlogschannelid'] = newchannel.id
                await modlogsdb.replace_one({"guildid": str(ctx.guild.id)}, x)
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"Invite Logs successfully updated to {newchannel.mention}")
                return await ctx.send(embed=embed)
    
    @commands.command(description="Tells Information About Logs")
    async def tellmeaboutlogs(self,ctx):
        embed = discord.Embed(title = "Information about Logs",colour = discord.Colour.purple(),description='''
```
Message Logs:-
  • Message Edit
  • Message Delete
  • Bulk Message Delete
  
Mod Logs:-
  • Invite Create
  • Invite Delete
  • Role Create
  • Role Delete
  • And all other Mod Actions like Kick, Ban, Mute ...etc
  
Member Logs:-
  • Role Added
  • Role Removed
  • Nickname Changed

Member Join Logs:-
  • Member Join
  • Member Leave

Invite Logs:-
  • Shows who invited a person and through which invite (on a member joining the server)
  ⋆ Bot should have Manage Server Permissions for this , otherwise it won't work.
```
''')
        return await ctx.send(embed=embed)

    # --------------------------logevents------------------------------
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if (
                before.author.bot
                or after.author.bot
                or after.author.id == 808690602358079508
        ):
            return
        elif before.guild is None:
            return
        count = await modlogsdb.count_documents({"guildid": str(before.guild.id), "msglogs": 1})
        if count == 0:
            return
        data = modlogsdb.find({"guildid": str(before.guild.id)})
        async for x in data:
            dict = x
        channel = self.client.get_channel(dict['msglogschannelid'])

        if before.pinned and not after.pinned:

            e = discord.Embed(colour=discord.Colour.purple(), description=f'''
Message Unpinned by {after.author.name} ({after.author.id})
[Message Link]({after.jump_url}) | {after.channel.mention} |{after.author.mention}
''')

            e.set_thumbnail(url="https://cdn.discordapp.com/attachments/860924948432027669/860925607553794058/pin.png")
            e.set_author(name="Message Unpinned", icon_url=after.author.display_avatar.url)
            try:
                await channel.send(embed=e)
            except Exception as e:
                pass
        elif not before.pinned and after.pinned:

            e = discord.Embed(colour=discord.Colour.purple(), description=f'''
Message Pinned by {after.author.name} ({after.author.id})
[Message Link]({after.jump_url}) | {after.channel.mention} |{after.author.mention}
''')
            e.set_thumbnail(url="https://cdn.discordapp.com/attachments/860924948432027669/860925607553794058/pin.png")
            e.set_author(name="Message Pinned", icon_url=after.author.display_avatar.url)
            try:
                await channel.send(embed=e)
            except Exception as e:
                pass
        else:
            if before.content != after.content:
                e = discord.Embed(colour=discord.Colour.purple())
                e.add_field(
                    name=f"Changes by - {after.author.name} ({after.author.id})",
                    value=f"From -> {before.content}\n to -> {after.content}\n**[Message link]({after.jump_url})**  | {after.channel.mention} | {after.author.mention}",
                    inline=False,
                )
                e.set_author(name="Message Edited", icon_url=after.author.display_avatar.url)
                e.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/860924948432027669/860924988193374218/message.png")
                try:
                    await channel.send(embed=e)
                except Exception as e:
                    pass
            else:
                return
        return

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        invcheck = await modlogsdb.count_documents({"guildid": str(invite.guild.id), "invlogs": 1})
        if invcheck!=0:
            invdata = invitetrack.find({"guildid":str(invite.guild.id)})
            async for x in invdata:
                invites = x['invites']
            invites[invite.id]=invite.uses
            invnew = {
                "guildid":str(invite.guild.id),
                "invites":invites
            }

            await invitetrack.replace_one({"guildid":str(invite.guild.id)},invnew)
        count = await modlogsdb.count_documents({"guildid": str(invite.guild.id), "modlogs": 1})
        if count == 0:
            return
        data = modlogsdb.find({"guildid": str(invite.guild.id)})
        async for x in data:
            dict = x
        channel = self.client.get_channel(dict['modlogschannelid'])
        e = discord.Embed(colour=discord.Colour.purple(),
                          description=f"{invite} in {invite.channel.mention}\n\nCreated By:- {invite.inviter.mention}")
        e.set_author(name="Invite Created")
        e.set_thumbnail(url="https://cdn.discordapp.com/attachments/860924948432027669/860924982808018965/invite.png")
        try:
            await channel.send(embed=e)
        except Exception:
            pass
        


        return

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        invcheck = await modlogsdb.count_documents({"guildid": str(invite.guild.id), "invlogs": 1})
        if invcheck!=0:
            invdata = invitetrack.find({"guildid":str(invite.guild.id)})
            async for x in invdata:
                invites = x['invites']
            invites.pop(invite.id)
            invnew = {
                "guildid":str(invite.guild.id),
                "invites":invites
            }
            await invitetrack.replace_one({"guildid":str(invite.guild.id)},invnew)
        
        count = await modlogsdb.count_documents({"guildid": str(invite.guild.id), "modlogs": 1})
        if count == 0:
            return
        data = modlogsdb.find({"guildid": str(invite.guild.id)})
        async for x in data:
            dict = x
        channel = self.client.get_channel(dict['modlogschannelid'])

        e = discord.Embed(colour=discord.Colour.purple(), description=f"{invite.url}")
        e.set_author(name="Invite Deleted")
        e.set_thumbnail(url="https://cdn.discordapp.com/attachments/860924948432027669/860924982808018965/invite.png")
        try:
            await channel.send(embed=e)
        except Exception:
            pass
        
        return

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild is None:
            return
        count = await modlogsdb.count_documents({"guildid": str(message.guild.id), "msglogs": 1})
        if count == 0:
            return
        data = modlogsdb.find({"guildid": str(message.guild.id)})
        async for x in data:
            dict = x
        channel = self.client.get_channel(dict['msglogschannelid'])
        if len(message.attachments)!=0:
            if len(message.attachments)!=1:
                
                e = discord.Embed(title="Message Deleted", colour=discord.Colour.purple())
                if len(message.content)==0:
                    messagevalue = "\u202b"
                else:
                    messagevalue = message.content
                    if len(messagevalue)>1020:
                        messagevalue = messagevalue[:1020] + "..."
                other = ""
                c=2
                for i in message.attachments[1:]:
                    other = other + f"[Attachment {c}]({i.proxy_url}) "
                    c+=1
                
                if message.attachments[0].content_type[:5] =="image":
                    e.set_image(url = message.attachments[0].url)
                else:
                    other = f"[Attachment 1]({message.attachments[0].proxy_url}) " + other
                e.add_field(name='Message',value = f"{messagevalue}",inline = False)
                e.add_field(name = "Message Id",value = message.id)
                e.add_field(name = "Message Author",value =f"{message.author.mention} ({message.author.name}#{message.author.discriminator})",inline = False)
                e.add_field(name = "Channel",value = message.channel.mention)
                e.add_field(name= f"Attachments[{len(message.attachments)}]",value = other,inline = False)

            else:
                if len(message.content)==0:
                    messagevalue = "\u202b"
                else:
                    messagevalue = message.content
                    if len(messagevalue)>1020:
                        messagevalue = messagevalue[:1020] + "..."
                e = discord.Embed(title="Message Deleted", colour=discord.Colour.purple())    
                e.add_field(name='Message',value = f"{messagevalue}",inline = False)
                e.add_field(name = "Message Id",value = message.id)
                e.add_field(name = "Message Author",value =f"{message.author.mention} ({message.author.name}#{message.author.discriminator})",inline = False)
                e.add_field(name = "Channel",value = message.channel.mention)
                attachvalue = "\u202b"
                if message.attachments[0].content_type[:5] =="image":
                    e.set_image(url = message.attachments[0].url)
                else:
                    attachvalue = f"[Attachment 1]({message.attachments[0].proxy_url}) "

                e.add_field(name= f"Attachments[1]",value = attachvalue,inline = False)

        else:
            if len(message.content)==0:
                messagevalue = "\u202b"
            else:
                messagevalue = message.content
                if len(messagevalue)>1020:
                    messagevalue = messagevalue[:1020] + "..."
            e = discord.Embed(title="Message Deleted", colour=discord.Colour.purple())
            e.add_field(name='Message',value = f"{messagevalue}",inline = False)
            e.add_field(name = "Message Id",value = message.id)
            e.add_field(name = "Message Author",value = f"{message.author.mention} ({message.author.name}#{message.author.discriminator})",inline = False)
            e.add_field(name = "Channel",value = message.channel.mention)
            e.add_field(name = "Attachments[0]",value="None",inline = False)
        e.set_thumbnail(url="https://cdn.discordapp.com/attachments/860924948432027669/860924980945223740/delete.png")
        try:
            await channel.send(embed=e)
        except Exception:
            pass
        return

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        if payload.guild_id is None:
            return
        count = await modlogsdb.count_documents({"guildid": str(payload.guild_id), "msglogs": 1})
        if count == 0:
            return
        data = modlogsdb.find({"guildid": str(payload.guild_id)})
        async for x in data:
            dict = x
        channel = self.client.get_channel(dict['msglogschannelid'])
        e = discord.Embed(title="Messages Deleted in Bulk", colour=discord.Colour.purple(),
                          description=f"{len(payload.message_ids)} messages got deleted in <#{payload.channel_id}>")
        e.set_thumbnail(url="https://cdn.discordapp.com/attachments/860924948432027669/860924980945223740/delete.png")
        try:
            await channel.send(embed=e)
        except Exception:
            pass
        return

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        count = await modlogsdb.count_documents({"guildid": str(role.guild.id), "modlogs": 1})
        if count == 0:
            return
        data = modlogsdb.find({"guildid": str(role.guild.id)})
        async for x in data:
            dict = x
        channel = self.client.get_channel(dict['modlogschannelid'])
        e = discord.Embed(title="Role Created", colour=discord.Colour.purple(),
                          description=f"{role.mention}\n\nRole-id- {role.id}")
        e.set_thumbnail(url="https://cdn.discordapp.com/attachments/860924948432027669/860924992668958740/role.png")
        try:
            await channel.send(embed=e)
        except Exception:
            pass
        return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        count = await modlogsdb.count_documents({"guildid": str(role.guild.id), "modlogs": 1})
        if count == 0:
            return
        data = modlogsdb.find({"guildid": str(role.guild.id)})
        async for x in data:
            dict = x
        channel = self.client.get_channel(dict['modlogschannelid'])
        e = discord.Embed(title="Role Deleted", colour=discord.Colour.purple(),
                          description=f"Role Name - {role.name}\nRole-id- {role.id}")
        e.set_thumbnail(url="https://cdn.discordapp.com/attachments/860924948432027669/860924992668958740/role.png")
        try:
            await channel.send(embed=e)
        except Exception:
            pass
        return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.nick != after.nick and not before.roles != after.roles:
            return
        count = await modlogsdb.count_documents({"guildid": str(before.guild.id), "memlogs": 1})
        if count == 0:
            return
        data = modlogsdb.find({"guildid": str(before.guild.id)})
        async for x in data:
            dict = x
        channel = self.client.get_channel(dict['memlogschannelid'])
        if before.nick != after.nick:

            e = discord.Embed(title="Nickname changed", colour=discord.Colour.purple(), description=f'''
Nickname changed of {after.mention}({after.id}),
**Before** -> {before.nick}\n**Now** -> {after.nick}''')
            e.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/860924948432027669/860924984855756810/member.png")
            try:
                await channel.send(embed=e)
            except Exception:
                pass
        elif before.roles != after.roles:
            if len(before.roles) < len(after.roles):
                role = list(set(after.roles) - set(before.roles))[0]
                e = discord.Embed(title="Role Added", colour=discord.Colour.purple(), description=f'''
{role.mention} role was given to {after.mention}''')
                e.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/860924948432027669/860924992668958740/role.png")
                try:
                    await channel.send(embed=e)
                except Exception:
                    pass
            else:
                role = list(set(before.roles) - set(after.roles))[0]
                e = discord.Embed(title="Role Removed", colour=discord.Colour.purple(), description=f'''
{role.mention} role was removed from {after.mention}''')
                e.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/860924948432027669/860924992668958740/role.png")
                try:
                    await channel.send(embed=e)
                except Exception:
                    pass
        return



async def setup(client):
    await client.add_cog(Logging(client))