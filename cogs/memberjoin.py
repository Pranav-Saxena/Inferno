import discord 
from discord.ext import commands
import time
import asyncio
from typing import Union
import json
import re
import motor.motor_asyncio
import nest_asyncio
import datetime
import os
from datetime import datetime

nest_asyncio.apply()
cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb_cluster_url")
autorole = cluster["autorole"]["autorole"]
botar = cluster["botar"]["botar"]
modlogsdb = cluster["modlogs"]["modlogs"]
invitetrack = cluster["modlogs"]["invitetrack"]

def find_invite_by_code(invite_list, codeid):
    
    # Simply looping through each invite in an
    # invite list which we will get using guild.invites()

    for inv in invite_list:
        
        # Check if the invite code in this element
        # of the list is the one we're looking for
        
        if inv.id == codeid:
            # If it is, we return it.
            return inv

async def memjoinlogs(member,modlogsdb,client):
    data = modlogsdb.find({"guildid": str(member.guild.id)})
    async for x in data:
        dict = x
    channel = client.get_channel(dict['memjoinlogschannelid'])

    e = discord.Embed(title="Member Joined", colour=discord.Colour.purple(), description=f'''
{member.mention} ({member.name}#{member.discriminator})

**Member Id :** {member.id}

**Account Created On :-**
{str(member.created_at)[0:11]}''',timestamp = datetime.utcnow())
    e.set_thumbnail(url=member.display_avatar.url)
    try:
        await channel.send(embed=e)
    except Exception:
        pass
    return

async def memleavelogs(member,modlogsdb,client):
    data = modlogsdb.find({"guildid": str(member.guild.id)})
    async for x in data:
        dict = x
    channel = client.get_channel(dict['memjoinlogschannelid'])

    e = discord.Embed(title="Member Left", colour=discord.Colour.purple(), description=f'''
{member.mention} ({member.name}#{member.discriminator})

**Member Id :** {member.id}''',timestamp = datetime.utcnow())

    e.set_thumbnail(url=member.display_avatar.url)
    try:
        await channel.send(embed=e)
    except Exception:
        pass
    return

async def invlogs(member,modlogsdb,client):
    data = modlogsdb.find({"guildid": str(member.guild.id)})
    async for x in data:
        dict = x
    channel = client.get_channel(dict['invlogschannelid'])
#--------------------
    invdata = invitetrack.find({"guildid": str(member.guild.id)})
    async for x in invdata:
        invites = x['invites']
    invites_before_join = invites

    # Getting the invites after the user joining
    # so we can compare it with the first one, and
    # see which invite uses number increased

    try:
        invites_after_join = await member.guild.invites()
    except:
        return


    # Loops for each invite we have for the guild
    # the user joined.
    inviteneeded = None
    for invite in invites_before_join:

        # Now, we're using the function we created just
        # before to check which invite count is bigger
        # than it was before the user joined.

        inviteget2 =  find_invite_by_code(invites_after_join, invite)
        if inviteget2 is None:
            continue
        if invites_before_join[invite] < inviteget2.uses:
            
            # Now that we found which link was used,
            # we will print a couple things in our console:
            # the name, invite code used the the person
            # who created the invite code, or the inviter.
            
            # print(f"Member {member.name} Joined")
            # print(f"Invite Code: {invite.code}")
            # print(f"Inviter: {invite.inviter}")
            inviteneeded = inviteget2
            # We will now update our cache so it's ready
            # for the next user that joins the guild
            invites_before_join[inviteget2.id] = inviteget2.uses
            invnew = {
                "guildid":str(member.guild.id),
                "invites": invites_before_join
            }
    if inviteneeded is None:
        e = discord.Embed(title="Member Joined!", colour=discord.Colour.purple(), description=f'''
**Member :** {member.mention}({member.name}#{member.discriminator})
I couldn't find who invited {member.mention}, maybe a temporary invite''',timestamp = datetime.utcnow())
        e.set_thumbnail(url="https://cdn.discordapp.com/attachments/860924948432027669/860924982808018965/invite.png")
        try:
            await channel.send(embed=e)
        except Exception:
            pass
        return
    c= 0 
    try:
        inviteslist = await member.guild.invites()
    except:
        return
    for i in inviteslist:
        try:
            if i.inviter.id == inviteneeded.inviter.id:
                c+= i.uses
        except:
            pass
    e = discord.Embed(title="Member Joined!", colour=discord.Colour.purple(), description=f'''
**Member :** {member.mention}({member.name}#{member.discriminator})
**Invited By :** {inviteneeded.inviter.name}#{inviteneeded.inviter.discriminator}
**Invite Used :** {inviteneeded}

{inviteneeded.inviter.name}#{inviteneeded.inviter.discriminator} now has {c} invites!''',timestamp = datetime.utcnow())
    e.set_thumbnail(url="https://cdn.discordapp.com/attachments/860924948432027669/860924982808018965/invite.png")
    try:
        await channel.send(embed=e)
    except Exception:
        pass
    await invitetrack.replace_one({"guildid":str(member.guild.id)},invnew)
    return

async def aradd(member,autorole):
    if member.bot:
        return
    x = autorole.find({'guildid': f"{member.guild.id}"})
    async for i in x:
        role = member.guild.get_role(i["roleid"])
    try:
        await member.add_roles(role)
    except Exception as e:
        print(e)
    return

async def botaradd(member,botar):
    if not member.bot:
         return
    x = botar.find({'guildid': f"{member.guild.id}"})
    async for i in x:
        role = member.guild.get_role(i["roleid"])
    try:
        await member.add_roles(role)
    except Exception as e:
        print(e)
    return  
invites = {}
class joinevents(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.Cog.listener("on_member_join")
    async def memjoin(self,member):
        checkar = await autorole.count_documents({'guildid': f"{member.guild.id}"})
        checkbr = await botar.count_documents({'guildid': f"{member.guild.id}"})
        checkmemjoinlogs = await modlogsdb.count_documents({"guildid": str(member.guild.id), "memjoinlogs": 1})
        checkinvlogs = await modlogsdb.count_documents({"guildid": str(member.guild.id), "invlogs": 1})
        if checkar !=0:
            await aradd(member,autorole)
        if checkbr !=0:
            await botaradd(member,botar)    
        if checkmemjoinlogs !=0:
            await memjoinlogs(member,modlogsdb,self.client)
        if checkinvlogs !=0:
            await invlogs(member,modlogsdb,self.client)
        return
    @commands.Cog.listener("on_member_remove")
    async def memleave(self,member):
        checkmemjoinlogs = await modlogsdb.count_documents({"guildid": str(member.guild.id), "memjoinlogs": 1})
        if checkmemjoinlogs !=0:
            await memleavelogs(member,modlogsdb,self.client)
        return
            
async def setup(client):  # Cog setup command
    await client.add_cog(joinevents(client))
