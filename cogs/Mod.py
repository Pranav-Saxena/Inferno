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
import datetime

nest_asyncio.apply()
cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb_cluster_auth")
modcasecounter = cluster["modlogs"]["modcase_counter"]
modcases = cluster["modlogs"]["modcases"]
modlogsdb = cluster['modlogs']['modlogs']

def is_it_me(ctx):
  return ctx.author.id == 704174691757064304

class Mod(commands.Cog):
  def __init__(self,client):
    self.client = client 
  
  @commands.command(aliases = ["del","purge"],description= "Deletes messages from the channel")
  @commands.guild_only()
  @commands.has_permissions(manage_messages = True)
  @commands.bot_has_permissions(manage_messages  =True)
  # @commands.check_any(commands.has_permissions(manage_messages=True), commands.check(is_it_me))
  async def clear(self,ctx,amount=1):
    if amount>100:
      await ctx.send("You can't delete more than 100 messages")
      return
    else:
      await ctx.channel.purge(limit = amount+1)
      if amount==1:
        msg = await ctx.send(f"Deleted {amount} message successfully")
      else:
        msg =await ctx.send(f"Deleted {amount} messages successfully")
      await asyncio.sleep(2)
      await msg.delete()
      return


  @commands.command(description = "Kicks a member from the server")
  @commands.has_permissions(kick_members = True)
  @commands.bot_has_permissions(kick_members=True)
  @commands.guild_only()
  # @commands.check_any(commands.has_permissions(kick_members=True), commands.check(is_it_me))
  async def kick(self,ctx, member : discord.Member,*,reason = None):
    if member == self.client.user:
      await ctx.send("**You can't kick me**")
      return
    elif member == ctx.guild.owner:
      await ctx.send("The Server Owner can't be kicked")
      return
    elif ctx.guild.me.top_role < member.top_role:
      await ctx.send("**Member is higher than me in hierarchy**")
      return
    elif member == ctx.author:
      await ctx.send("**You cannot kick yourself**")    
      return
    await member.kick(reason = reason)
    
    if reason ==None:
      await ctx.send(f"{member.mention} got kicked successfully <a:tick:844553824991313961>")
    else:
      await ctx.send(f"{member.mention} got kicked successfully <a:tick:844553824991313961>. Reason - {reason}")

#mod-history
    if len(str(reason))>100:
      reason = reason[:96]+"..."
    checkmodcaseno = await modcasecounter.count_documents({'guildid': f"{ctx.guild.id}"})
    if checkmodcaseno ==0:
      modcaseno = 1
      casenoinfo = {
        "guildid":f"{ctx.guild.id}",
        "modcaseno":1
      }
      await modcasecounter.insert_one(casenoinfo)
    else:
      findmodcaseno = modcasecounter.find({'guildid': f"{ctx.guild.id}"})
      async for x in findmodcaseno:
        tempmodcaseno = x["modcaseno"]
      modcaseno = tempmodcaseno +1
    modinfo = {
      "guilid": f"{ctx.guild.id}",
      "memberid": member.id,
      "membername" : f"{member.name}#{member.discriminator}",
      "type":"kick",
      "moderatorid" : ctx.author.id,
      "moderatorname": f"{ctx.author.name}#{ctx.author.discriminator}",
      "reason" : str(reason),
      "modcase" : modcaseno,
      "date" : f"{datetime.datetime.now().day} {datetime.datetime.now().strftime('%b')} {datetime.datetime.now().year} {datetime.datetime.now().strftime('%H')}:{datetime.datetime.now().strftime('%M')}:{datetime.datetime.now().strftime('%S')}",
      "datetimeobject": datetime.datetime.now()
    }    
    r = await modcases.insert_one(modinfo)
    newmodcasecounter = {
      "guildid":f"{ctx.guild.id}",
      "modcaseno":modcaseno
    }
    await modcasecounter.replace_one({"guildid":f"{ctx.guild.id}"},newmodcasecounter)
#kick-logs
    count = await modlogsdb.count_documents({"guildid":str(ctx.guild.id),"modlogs":1})
    if count ==0:
      return
    data = modlogsdb.find({"guildid":str(ctx.guild.id)})
    async for x in data:
      dict = x
    channel = self.client.get_channel(dict['modlogschannelid'])
    e = discord.Embed(title = "Member Kicked",colour=discord.Colour.purple(),description=f"{member.mention} was kicked from the server\n\nReason - {str(reason)}\nModerator - {ctx.author.mention}")
    e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/860924948432027669/861492310390472714/kick.png")
    try:
      await channel.send(embed=e)
    except Exception:
      pass    
    return
  @commands.command(description = "Bans a member from the server")
  # @commands.has_permissions(ban_members = True)
  @commands.has_permissions(ban_members=True)
  @commands.bot_has_permissions(ban_members=True)
  @commands.guild_only()
  async def ban(self,ctx, member : discord.Member,*,reason = None):
    if member == self.client.user:
      await ctx.send("**You can't ban me**")
      return
    elif member == ctx.guild.owner:
      await ctx.send("The Server Owner can't be banned")
      return
    elif ctx.guild.me.top_role <= member.top_role:
      await ctx.send("**Member is higher than or equal to me in hierarchy**")
      return
    elif member == ctx.author:
      await ctx.send("**You cannot ban yourself**")
      return 
    await member.ban(reason = reason)
    if reason ==None:
      await ctx.send(f"{member.mention} got banned successfully <a:tick:844553824991313961> ")
    else:
      await ctx.send(f"{member.mention} got banned successfully <a:tick:844553824991313961>. Reason - {reason}")
#mod-history
    if len(str(reason))>100:
      reason = reason[:96]+"..."
    checkmodcaseno = await modcasecounter.count_documents({'guildid': f"{ctx.guild.id}"})
    if checkmodcaseno ==0:
      modcaseno = 1
      casenoinfo = {
        "guildid":f"{ctx.guild.id}",
        "modcaseno":1
      }
      await modcasecounter.insert_one(casenoinfo)
    else:
      findmodcaseno = modcasecounter.find({'guildid': f"{ctx.guild.id}"})
      async for x in findmodcaseno:
        tempmodcaseno = x["modcaseno"]
      modcaseno = tempmodcaseno +1
    modinfo = {
      "guilid": f"{ctx.guild.id}",
      "memberid": member.id,
      "membername" : f"{member.name}#{member.discriminator}",
      "type":"ban",
      "moderatorid" : ctx.author.id,
      "moderatorname": f"{ctx.author.name}#{ctx.author.discriminator}",
      "reason" : str(reason),
      "modcase" : modcaseno,
      "date" : f"{datetime.datetime.now().day} {datetime.datetime.now().strftime('%b')} {datetime.datetime.now().year} {datetime.datetime.now().strftime('%H')}:{datetime.datetime.now().strftime('%M')}:{datetime.datetime.now().strftime('%S')}",
      "datetimeobject": datetime.datetime.now()
    }    
    r = await modcases.insert_one(modinfo)
    newmodcasecounter = {
      "guildid":f"{ctx.guild.id}",
      "modcaseno":modcaseno
    }
    await modcasecounter.replace_one({"guildid":f"{ctx.guild.id}"},newmodcasecounter)
#ban-logs
    count = await modlogsdb.count_documents({"guildid":str(ctx.guild.id),"modlogs":1})
    if count ==0:
      return
    data = modlogsdb.find({"guildid":str(ctx.guild.id)})
    async for x in data:
      dict = x
    channel = self.client.get_channel(dict['modlogschannelid'])
    e = discord.Embed(title = "Member Banned",colour=discord.Colour.purple(),description=f"{member.mention} was Banned from the server\n\nReason - {str(reason)}\nModerator - {ctx.author.mention}")
    e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/860924948432027669/861492445153984522/750371618584395877.png")
    try:
      await channel.send(embed=e)
    except Exception:
      pass    
    return  
  
  @commands.command(description = "Unbans a user from the server")
  @commands.has_permissions(ban_members = True)
  @commands.bot_has_permissions(ban_members =True)
  @commands.guild_only()
  # @commands.check_any(commands.has_permissions(ban_members=True), commands.check(is_it_me))
  async def unban(self,ctx,*,id=None):
    if not id.isnumeric():
      id = id.replace("<","")
      id = id.replace(">","")
      id = id.replace("@","")
      id = id.replace("!","")
    id = int(id)
    user = await self.client.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(f"{user.mention} got unbanned successfully <a:tick:844553824991313961>")
#unban-logs
    count = await modlogsdb.count_documents({"guildid":str(ctx.guild.id),"modlogs":1})
    if count ==0:
      return
    data = modlogsdb.find({"guildid":str(ctx.guild.id)})
    async for x in data:
      dict = x
    channel = self.client.get_channel(dict['modlogschannelid'])
    e = discord.Embed(title = "Member Unbanned",colour=discord.Colour.purple(),description=f"{user.mention} got Unbanned from the server")
    e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/860924948432027669/861497031528808458/7191_unban_hammer.png")
    try:
      await channel.send(embed=e)
    except Exception:
      pass    
    return
#alt code for unban
# if not id.isnumeric():
#     for bad in ["<",">","@","!"]:
#         id = id.replace(bad,"")
  @commands.command(pass_context=True,alisases=["changenick","changenickname"],description = "Changes the nickname of the user in the server")
  @commands.has_permissions(manage_nicknames=True)
  @commands.bot_has_permissions(manage_nicknames  =True)
  @commands.guild_only()
  async def chnick(self,ctx, member: discord.Member,*, nick):
    x = member.name
    await member.edit(nick=nick)
    await ctx.send(f"{x}'s nickname changed to {nick} ")
    return  

  @commands.command(pass_context=True,aliases=["resetnickname","rstnick"],description = "Resets the nickname of the user in the server")
  @commands.has_permissions(manage_nicknames=True)
  @commands.bot_has_permissions(manage_nicknames  =True)
  @commands.guild_only()
  async def resetnick(self,ctx, member: discord.Member):
    x = member.name
    await member.edit(nick=x)
    await ctx.send(f"{x}'s nickname resetted successfully")
    return

  @commands.command(description = "Adds the role to the member in the server")
  @commands.has_permissions(manage_roles=True)
  @commands.bot_has_permissions(manage_roles  =True)
  @commands.guild_only()
  async def addrole(self,ctx,member:discord.Member,role:discord.Role,*, reason=None):
    if ctx.guild.me.top_role < role :
      await ctx.send("**the role is above my top role**")
      return
    elif ctx.guild.me.top_role == role :
      await ctx.send("**the role is my top role. I can't assign it to someone else**")
      return
    elif role> ctx.author.top_role and not ctx.author == ctx.guild.owner:
      await ctx.send("The role you are trying to add is higher than your top role in hierarchy")
      return 
    elif role == ctx.author.top_role and not ctx.author == ctx.guild.owner:
      await ctx.send("The role you are trying to add is your top role. You can't assign it to someone else")
      return 
    elif role.is_bot_managed():
      return await ctx.send("The role is associated with a bot you can't assign it to someone else")
    elif role.is_integration():
      return await ctx.send("The role is managed by an integration you can't assign it to someone else")
    elif role.managed:
      return await ctx.send("The role is managed by some integration you can't assign it to someone else")
    elif role.is_default():
      return await ctx.send("The role is the default role, you can't assign it to someone else")

    if reason is None:
    # if role in ctx.guild.roles():
      await member.add_roles(role, reason=reason)
      embed=discord.Embed(title='Role Added',description=f'{role} role was added to {member.mention} by {ctx.author.mention}',colour=discord.Colour.purple())
      await ctx.send(embed=embed)
    else:
      await member.add_roles(role, reason=reason)
      embed=discord.Embed(title='Role Added',description=f'{role} role was added to {member.mention} by {ctx.author.mention}. Reason - {reason}',colour=discord.Colour.purple())
      await ctx.send(embed=embed)
    return

  @commands.command(description = "Removes the role to the member in the server")
  @commands.has_permissions(manage_roles=True)
  @commands.bot_has_permissions(manage_roles  =True)
  @commands.guild_only()
  async def unrole(self,ctx,member:discord.Member,role:discord.Role,*, reason=None):
    if ctx.guild.me.top_role < role:
      await ctx.send("**the role is above my top role**")
      return
    elif ctx.guild.me.top_role == role :
      await ctx.send("**the role is my top role. I can't remove it from someone else**")
      return
    elif role> ctx.author.top_role and not ctx.author == ctx.guild.owner:
      await ctx.send("The role you are trying to remove is higher than your top role in hierarchy")
      return   
    elif role == ctx.author.top_role and not ctx.author == ctx.guild.owner:
      await ctx.send("The role you are trying to add is your top role. You can't remove it from someone else")
      return 
    elif role.is_bot_managed():
      return await ctx.send("The role is associated with a bot you can't remove it from someone else")
    elif role.is_integration():
      return await ctx.send("The role is managed by an integration you can't remove it from someone else")
    elif role.managed:
      return await ctx.send("The role is managed by some integration you can't remove it from someone else")
    elif role.is_default():
      return await ctx.send("The role is the default role, you can't remove it from someone else")
    else:
      if reason is None:
        await member.remove_roles(role,reason=reason) 
        embed=discord.Embed(title='Role Removed',description=f'{role} role was removed from {member.mention} by {ctx.author.mention}',colour=discord.Colour.purple())
        await ctx.send(embed=embed)
      else:
        await member.remove_roles(role,reason=reason) 
        embed=discord.Embed(title='Role Removed',description=f'{role} role was removed from {member.mention} by {ctx.author.mention} for {reason}',colour=discord.Colour.purple())
        await ctx.send(embed=embed)
    return

  @commands.command(description = "Mutes a person from chatting in the server")
  @commands.has_permissions(kick_members=True)
  @commands.bot_has_permissions(manage_roles = True)
  @commands.guild_only()
  async def mute(self,ctx,member : discord.Member,*,reason=None):
    
    if member == self.client.user:
      await ctx.send("**You can't mute me**")
      return
    
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if mutedRole in member.roles:
      embed = discord.Embed(description= "User is already muted")
      await ctx.send(embed=embed)
      return
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
        
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False)
    embed = discord.Embed(colour=discord.Colour.purple())
    embed.set_author(name=f"{member.name}#{member.discriminator} is now muted",icon_url=member.avatar.url)
    if reason is not None:
      embed.add_field(name=f"**reason :** ", value=f"{reason}", inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
#mod-history  
    checkmodcaseno = await modcasecounter.count_documents({'guildid': f"{ctx.guild.id}"})
    if checkmodcaseno ==0:
      modcaseno = 1
      casenoinfo = {
        "guildid":f"{ctx.guild.id}",
        "modcaseno":1
      }
      await modcasecounter.insert_one(casenoinfo)
    else:
      findmodcaseno = modcasecounter.find({'guildid': f"{ctx.guild.id}"})
      async for x in findmodcaseno:
        tempmodcaseno = x["modcaseno"]
      modcaseno = tempmodcaseno +1
    modinfo = {
      "guilid": f"{ctx.guild.id}",
      "memberid": member.id,
      "membername" : f"{member.name}#{member.discriminator}",
      "type":"mute",
      "moderatorid" : ctx.author.id,
      "moderatorname": f"{ctx.author.name}#{ctx.author.discriminator}",
      "reason" : str(reason),
      "modcase" : modcaseno,
      "date" : f"{datetime.datetime.now().day} {datetime.datetime.now().strftime('%b')} {datetime.datetime.now().year} {datetime.datetime.now().strftime('%H')}:{datetime.datetime.now().strftime('%M')}:{datetime.datetime.now().strftime('%S')}",
      "datetimeobject": datetime.datetime.now()
    }    
    r = await modcases.insert_one(modinfo)
    newmodcasecounter = {
      "guildid":f"{ctx.guild.id}",
      "modcaseno":modcaseno
    }
    await modcasecounter.replace_one({"guildid":f"{ctx.guild.id}"},newmodcasecounter)
#mute-logs
    count = await modlogsdb.count_documents({"guildid":str(ctx.guild.id),"modlogs":1})
    if count ==0:
      return
    data = modlogsdb.find({"guildid":str(ctx.guild.id)})
    async for x in data:
      dict = x
    channel = self.client.get_channel(dict['modlogschannelid'])
    e = discord.Embed(title = "Member Muted",colour=discord.Colour.purple(),description=f"{member.mention} was Muted\n\nReason - {str(reason)}\nModerator - {ctx.author.mention}")
    e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/860924948432027669/861492373753298974/585767366722584576.png")
    try:
      await channel.send(embed=e)
    except Exception:
      pass    
    return
  @commands.command(description = "Unmutes a person from chatting in the server")
  @commands.has_permissions(kick_members=True)
  @commands.bot_has_permissions(manage_roles = True)
  @commands.guild_only()
  async def unmute(self,ctx, member: discord.Member):
    if member == self.client.user:
      await ctx.send("**You can't unmute me**")
      return
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    if mutedRole not in member.roles:
      embed = discord.Embed(colour=discord.Colour.purple())
      embed.set_author(name=f"{member.name}#{member.discriminator} is already unmuted",icon_url=member.avatar.url)
      return await ctx.send(embed = embed)
    await member.remove_roles(mutedRole)
    embed = discord.Embed(colour=discord.Colour.purple(),)
    embed.set_author(name=f"{member.name}#{member.discriminator} is now unmuted",icon_url=member.avatar.url)
    await ctx.send(embed=embed)
#unmute-logs
    count = await modlogsdb.count_documents({"guildid":str(ctx.guild.id),"modlogs":1})
    if count ==0:
      return
    data = modlogsdb.find({"guildid":str(ctx.guild.id)})
    async for x in data:
      dict = x
    channel = self.client.get_channel(dict['modlogschannelid'])
    e = discord.Embed(title = "Member Unmuted",colour=discord.Colour.purple(),description=f"{member.mention} was Unmuted \n\nModerator - {ctx.author.mention}")
    e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/860924948432027669/861497403306410014/585788304210001920.png")
    try:
      await channel.send(embed=e)
    except Exception:
      pass    
    return
  @commands.command(description = "Blocks a person from chatting in the channel")
  @commands.has_permissions(kick_members=True)
  @commands.bot_has_permissions(manage_channels  =True)
  @commands.guild_only()
  async def block(self, ctx, user: discord.Member=None):
      """
        Blocks a user from chatting in current channel.
        
        Similar to mute but instead of restricting access
        to all channels it restricts in current channel.
      """
                                
      if not user: # checks if there is user
        return await ctx.send("You must specify a user")
      if user == self.client.user:
        await ctx.send("**You can't block me**")
        return
      # elif ctx.guild.me.top_role < user.top_role:
      #   await ctx.send("**Member is higher than me in hierarchy**")
      #   return                          
      await ctx.channel.set_permissions(user, send_messages=False) # sets permissions for current channel
      embed = discord.Embed(colour=discord.Colour.purple(),)
      embed.set_author(name=f"{user.name}#{user.discriminator} has been blocked",icon_url=user.avatar.url)
      await ctx.send(embed=embed)
      return
  @commands.command(description = "Blocks a person from chatting in the channel")
  @commands.has_permissions(kick_members=True)
  @commands.bot_has_permissions(manage_channels  =True)
  @commands.guild_only()
  async def unblock(self, ctx, user: discord.Member=None):
      """Unblocks a user from current channel"""
                                
      if not user: # checks if there is user
        return await ctx.send("You must specify a user")
      if user == self.client.user:
        await ctx.send("**You can't unblock me**")
        return
      # elif ctx.guild.me.top_role < user.top_role:
      #   await ctx.send("**Member is higher than me in hierarchy**")
      #   return      
      await ctx.channel.set_permissions(user, send_messages=True) # gives back send messages permissions
      embed = discord.Embed(colour=discord.Colour.purple(),)
      embed.set_author(name=f"{user.name}#{user.discriminator} has been unblocked",icon_url=user.avatar.url)
      await ctx.send(embed=embed)
      return
  @commands.command(description = "bans and immediately unbans user from the server(used to clear the members messages in the server)")
  @commands.has_permissions(ban_members=True)
  @commands.bot_has_permissions(ban_members  =True)
  @commands.guild_only()
  async def softban(self, ctx, user: discord.Member=None, reason=None):
        """Temporarily restricts access to a server.(Bans and immediately unbans a user to clear their messages) """
        
        if not user: # checks if there is a user
            return await ctx.send("You must specify a user")
        if user == self.client.user:
          await ctx.send("**You can't softban me**")
          return
        elif ctx.guild.me.top_role < user.top_role:
          await ctx.send("**Member is higher than me in hierarchy**")
          return    
        try: # Tries to soft-ban user
            await user.ban(reason=reason)
            await ctx.guild.unban(user)
            
            await ctx.send(f"{user.name}#{user.discriminator} has been softbanned successfully <a:tick:844553824991313961>")
        except discord.Forbidden:
            return await ctx.send("You trying to soft-ban someone higher than the bot")
  @commands.command(description = "Mutes a person from chatting in the server for a specific period of time")
  @commands.has_permissions(kick_members=True)
  @commands.bot_has_permissions(manage_roles  =True)
  @commands.guild_only()
  async def tempmute(self,ctx, member: discord.Member, timem: int, d, *, reason=None):
    if member == self.client.user:
      await ctx.send("**You can't block me**")
      return
    # elif ctx.guild.me.top_role < member.top_role:
    #   await ctx.send("**Member is higher than me in hierarchy**")
    #   return    
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if mutedRole in member.roles:
      embed = discord.Embed(description= "User is already muted")
      await ctx.send(embed=embed)
      return
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False)
    embed = discord.Embed(title="Tempmuted",colour=discord.Colour.purple())
    embed.set_author(name=f"{member.name}#{member.discriminator} has been tempmuted for {timem}{d}",icon_url=member.avatar.url)
    if reason is not None:
      embed.add_field(name=f"**reason :** ", value=f"{reason}", inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)

    if d == "s":
      await asyncio.sleep(timem)

    if d == "m":
      await asyncio.sleep(timem*60)

    if d == "h":
      await asyncio.sleep(timem*60*60)

    if d == "d":
      await asyncio.sleep(timem*60*60*24)
    
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if mutedRole in member.roles:
      await member.remove_roles(mutedRole)

#mod-history  
    checkmodcaseno = await modcasecounter.count_documents({'guildid': f"{ctx.guild.id}"})
    if checkmodcaseno ==0:
      modcaseno = 1
      casenoinfo = {
        "guildid":f"{ctx.guild.id}",
        "modcaseno":1
      }
      await modcasecounter.insert_one(casenoinfo)
    else:
      findmodcaseno = modcasecounter.find({'guildid': f"{ctx.guild.id}"})
      async for x in findmodcaseno:
        tempmodcaseno = x["modcaseno"]
      modcaseno = tempmodcaseno +1
    modinfo = {
      "guilid": f"{ctx.guild.id}",
      "memberid": member.id,
      "membername" : f"{member.name}#{member.discriminator}",
      "type":"tempmute",
      "moderatorid" : ctx.author.id,
      "moderatorname": f"{ctx.author.name}#{ctx.author.discriminator}",
      "reason" : str(reason),
      "modcase" : modcaseno,
      "duration" : f"{timem}{d}",
      "date" : f"{datetime.datetime.now().day} {datetime.datetime.now().strftime('%b')} {datetime.datetime.now().year} {datetime.datetime.now().strftime('%H')}:{datetime.datetime.now().strftime('%M')}:{datetime.datetime.now().strftime('%S')}",
      "datetimeobject": datetime.datetime.now()
    }    
    r = await modcases.insert_one(modinfo)
    newmodcasecounter = {
      "guildid":f"{ctx.guild.id}",
      "modcaseno":modcaseno
    }
    await modcasecounter.replace_one({"guildid":f"{ctx.guild.id}"},newmodcasecounter)
#tempmute-logs
    count = await modlogsdb.count_documents({"guildid":str(ctx.guild.id),"modlogs":1})
    if count ==0:
      return
    data = modlogsdb.find({"guildid":str(ctx.guild.id)})
    async for x in data:
      dict = x
    channel = self.client.get_channel(dict['modlogschannelid'])
    e = discord.Embed(title = "Member Tempmuted",colour=discord.Colour.purple(),description=f"{member.mention} was Tempmuted\nDuration - {timem}{d}\n\nReason - {str(reason)}\nModerator - {ctx.author.mention}")
    e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/860924948432027669/861492373753298974/585767366722584576.png")
    try:
      await channel.send(embed=e)
    except Exception:
      pass    


    return
  @commands.command(description = "Locks the channel by disabling everyone to type")
  @commands.has_permissions(manage_channels=True)
  @commands.bot_has_permissions(manage_channels  =True)
  @commands.guild_only()
  async def lock(self,ctx):
    guild = ctx.guild 
    role = guild.default_role
    await ctx.channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=True)
    embed = discord.Embed(description=f"Locked channel {ctx.channel.mention} successfully")
    await ctx.send(embed=embed)
    return 
  @commands.command(description = "Unlocks the channel")
  @commands.has_permissions(manage_channels=True)
  @commands.bot_has_permissions(manage_channels  =True)
  @commands.guild_only()
  async def unlock(self,ctx):
    guild = ctx.guild 
    role = guild.default_role
    await ctx.channel.set_permissions(role, speak=True, send_messages=True, read_message_history=True, read_messages=True)
    embed = discord.Embed(description=f"unlocked channel {ctx.channel.mention} successfully")
    await ctx.send(embed=embed)
    return 
  @commands.command(description = "Enables slowmode in the channel")
  @commands.has_permissions(manage_channels=True)
  @commands.bot_has_permissions(manage_channels  =True)
  @commands.guild_only()
  async def enable_slowmode(self,ctx,duration):

    if not duration.isnumeric():
      embed = discord.Embed(title="Wrong Input",description="Please enter an integer between 0 and 21600 (denotes seconds)",colour= discord.Colour.purple())
      await ctx.send(embed = embed)
      return
    if int(duration)<=0 or int(duration)>21600:
      embed = discord.Embed(title="Wrong Input",description="Please enter an integer between 0 and 21600 (denotes seconds)",colour= discord.Colour.purple())
      await ctx.send(embed = embed)
      return 
    await ctx.channel.edit(slowmode_delay=int(duration))
    embed = discord.Embed(title="Slowmode enabled",description=f"Slowmode has been enabled in {ctx.channel.mention} for {duration} seconds\n. Use command `disable_slowmode` to disable slowmode",colour=discord.Colour.purple())
    await ctx.send(embed=embed)
    return
  @commands.command(description = "Disables slowmode in the channel")
  @commands.has_permissions(manage_channels=True)
  @commands.bot_has_permissions(manage_channels  =True)
  @commands.guild_only()
  async def disable_slowmode(self,ctx):
    await ctx.channel.edit(slowmode_delay=None)
    embed = discord.Embed(title="Slowmode Disabled",description=f"Slowmode has been disabled in {ctx.channel.mention}",colour=discord.Colour.purple())
    await ctx.send(embed=embed)
    return
  @commands.command(description = "deletes the specified channel(or the current channel by default if no other channel specified) ")
  @commands.has_permissions(manage_guild=True)
  @commands.bot_has_permissions(manage_guild  =True)
  @commands.guild_only()
  async def delete_channel(self,ctx,channeld:discord.TextChannel=None):
    if ctx.guild.id ==787337373486284850:
      await ctx.send("This command has been disabled for your server")
      return
    if channeld is None:
      await ctx.channel.delete()
      return
    else:
      await channeld.delete()
      embed = discord.Embed(title="Channel Deleted",description = f"Deleted Channel `{channeld.name}` successfully",colour = discord.Colour.purple())
      await ctx.send(embed=embed)
      return 
  @commands.command(description = "creates a new channel with the same settings and deletes the original one")
  @commands.has_permissions(manage_guild=True)
  @commands.bot_has_permissions(manage_guild=True)
  @commands.guild_only()
  async def clean_channel(self,ctx):
    if ctx.guild.id in [787337373486284850,705087194569769010]:
      await ctx.send("This command has been disabled for your server")
      return
    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel
    await ctx.send("Are you sure you want to clean this channel? Reply with y/yes to confirm and any other word to cancel.\nThis Is A dangerous command as it will delete the whole channel ie. all chats and media.\nThis action can't be undone")
    try:
      response = await self.client.wait_for("message",check = check , timeout = 30)
    except:
      await ctx.send("Command cleanchannel timed out")
      return
    if response.content.lower() in ["yes",'y']:
      channel = await ctx.channel.clone()
      await channel.move(after= ctx.channel)
      await ctx.channel.delete()
      await channel.send("**This Channel has been Cleaned!!** \n https://tenor.com/view/cats-clean-house-crazy-gato-gif-14747569")
      return
    else:
      return await ctx.send("Channel will not be cleaned!!")

 #-----------------Warning system-----------------------

#clearwarns, warn , modlogs , modcase , warnings @mem , delwarn [modcase], delmodcase [modcase] , modhistory , updatemodlogschannel 
#create paginator
#modcases , modcasecounter
  @commands.command(description = "Warns a member")
  @commands.has_permissions(kick_members = True)
  async def warn(self,ctx,member:discord.Member ,*,reason = None):
    if len(str(reason))>100:
      embed = discord.Embed(colour=discord.Colour.purple(),description="Limit the reason to 100 characters")
      return await ctx.send(embed = embed)
    checkmodcaseno = await modcasecounter.count_documents({'guildid': f"{ctx.guild.id}"})
    if checkmodcaseno ==0:
      modcaseno = 1
      casenoinfo = {
        "guildid":f"{ctx.guild.id}",
        "modcaseno":1
      }
      await modcasecounter.insert_one(casenoinfo)
    else:
      findmodcaseno = modcasecounter.find({'guildid': f"{ctx.guild.id}"})
      async for x in findmodcaseno:
        tempmodcaseno = x["modcaseno"]
      modcaseno = tempmodcaseno +1
    
    checkwarnsno = await modcases.count_documents({"guildid":f"{ctx.guild.id}","type":"warn","memberid":member.id})
    warnno = checkwarnsno + 1

    embed = discord.Embed(colour = discord.Colour.purple(),description = f'''
{member.mention} has been warned <a:tick:844553824991313961>.
''')
    await ctx.send(embed = embed)
    modinfo = {
      "guilid": f"{ctx.guild.id}",
      "memberid": member.id,
      "membername" : f"{member.name}#{member.discriminator}",
      "type":"warn",
      "moderatorid" : ctx.author.id,
      "moderatorname": f"{ctx.author.name}#{ctx.author.discriminator}",
      "reason" : str(reason),
      "modcase" : modcaseno,
      "date" : f"{datetime.datetime.now().day} {datetime.datetime.now().strftime('%b')} {datetime.datetime.now().year} {datetime.datetime.now().strftime('%H')}:{datetime.datetime.now().strftime('%M')}:{datetime.datetime.now().strftime('%S')}",
      "datetimeobject": datetime.datetime.now()
    }    
    r = await modcases.insert_one(modinfo)
    newmodcasecounter = {
      "guildid":f"{ctx.guild.id}",
      "modcaseno":modcaseno
    }
    await modcasecounter.replace_one({"guildid":f"{ctx.guild.id}"},newmodcasecounter)

#warn - logs
    count = await modlogsdb.count_documents({"guildid":str(ctx.guild.id),"modlogs":1})
    if count ==0:
      return
    data = modlogsdb.find({"guildid":str(ctx.guild.id)})
    async for x in data:
      dict = x
    channel = self.client.get_channel(dict['modlogschannelid'])
    e = discord.Embed(title = "Member Warned",colour=discord.Colour.purple(),description=f"{member.mention} was Warned.\n\nReason - {str(reason)}\nModerator - {ctx.author.mention}\n\n{member.mention} now has {warnno} warns")    
    e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/860924948432027669/861498251727339551/849197654919610378.png")
    try:
      await channel.send(embed=e)
    except Exception:
      pass    
    return

  @commands.command(description = "Shows warnings of a member")
  @commands.has_permissions(kick_members=True)
  async def warnings(self, ctx, member: discord.Member,pageno : int =1):
    if pageno <1:
      embed = discord.Embed(colour=discord.Colour.purple(),description="The Page No. should be a natural no.")
      return await ctx.send(embed=embed)
    c = await modcases.count_documents({"guilid": f"{ctx.guild.id}", "memberid": member.id, "type": "warn"})
    if c == 0:
      embed = discord.Embed(colour=discord.Colour.purple(), description="User has no warns")
      return await ctx.send(embed=embed)
    data = modcases.find({"guilid": f"{ctx.guild.id}", "memberid": member.id, "type": "warn"})
    desc = ''''''

    l = []

    async for x in data:
      check = len(f"**ModCase#{x['modcase']}** | Moderator - <@{x['moderatorid']}>({x['moderatorname']})" + "\n" + f"***Reason :*** `{x['reason']}`\n***Date :*** {x['date']}" + "\n\n")
      if (len(desc) + check) > 1000:
        embed = discord.Embed(colour=discord.Colour.purple(),description =desc)
        embed.set_author(name = f"{c} Warnings for {member.name}#{member.discriminator}({member.id})")
        l.append(embed)
        desc = ""
      desc = desc + f"**ModCase#{x['modcase']}** | Moderator - <@{x['moderatorid']}>({x['moderatorname']})" + "\n" + f"***Reason :*** `{x['reason']}`\n***Date :*** {x['date']}" + "\n\n"
    if desc != "":
      embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
      embed.set_author(name=f"{c} Warnings for {member.name}#{member.discriminator}({member.id})")
      l.append(embed)

    if pageno > len(l):
      if len(l) ==1:
        embed = discord.Embed(colour=discord.Colour.purple(),description=f"There is only 1 page")
      else:
        embed = discord.Embed(colour=discord.Colour.purple(),description=f"The Page No. should be between 1 and {len(l)}")
      return await ctx.send(embed=embed)

    embed = l[pageno-1]
    embed.set_footer(text=f"Page {pageno}/{len(l)}\nYou can use >warnings <member> <pageno> to go to different pages\nUse >modcase [modcasenumber] to get details of a modcase")
    await ctx.send(embed=embed)
    return
  @commands.command(description = "Shows details of a modcase")
  @commands.has_permissions(kick_members=True)
  async def modcase(self,ctx,modcasenumber:int):
    data = modcases.find({"guilid": f"{ctx.guild.id}","modcase":modcasenumber})
    c = 0
    async for x in data:
      if x['type'] == "tempmute":
        desc = f"**Type :** {x['type']}\n**Member :** {x['membername']}({x['memberid']})\n**Duration**-{x['duration']}\n**Moderator :**{x['moderatorname']}\n**Reason :** {x['reason']}\n**Date :** {x['date']}"  
      else:
        desc = f"**Type :** {x['type']}\n**Member :** {x['membername']}({x['memberid']})\n**Moderator :**{x['moderatorname']}\n**Reason :** {x['reason']}\n**Date :** {x['date']}"
      c =1
    if c==0:
      embed =discord.Embed(colour=discord.Colour.purple(),description=f"Modcase#{modcasenumber} not found")
      return await ctx.send(embed = embed)
    embed = discord.Embed(colour=discord.Colour.purple(),title = f"Modcase#{modcasenumber}",description = desc)
    await ctx.send(embed=embed)
    return
  @commands.command(description = "Clears all warns of a member")
  @commands.has_permissions(kick_members=True)
  async def clearwarns(self,ctx,member:discord.Member):
    count = await modcases.count_documents({"guilid": f"{ctx.guild.id}","memberid":member.id,"type":"warn"})
    if count ==0:
      embed = discord.Embed(colour=discord.Colour.purple(),description = "User has no warns")
      return await ctx.send(embed= embed)
    await modcases.delete_many({"guilid": f"{ctx.guild.id}","memberid":member.id,"type":"warn"})
    embed = discord.Embed(colour=discord.Colour.purple(),description=f"Cleared all ({count}) warns of {member.mention} successfully <a:tick:844553824991313961>")
    return await ctx.send(embed=embed)

  @commands.command(description = "Removes a Warn with the specific modcase number")
  @commands.has_permissions(kick_members=True)
  async def delwarn(self,ctx,modcasenumber:int):
    count = await modcases.count_documents({"guilid": f"{ctx.guild.id}","modcase":modcasenumber,"type":"warn"})
    count2 = await modcases.count_documents({"guilid": f"{ctx.guild.id}","modcase":modcasenumber})
    if count ==0 and count2 ==0:
      embed =discord.Embed(colour=discord.Colour.purple(),description=f"Modcase#{modcasenumber} not found")
      return await ctx.send(embed = embed)
    elif count ==0 and count2!=0:
      embed =discord.Embed(colour=discord.Colour.purple(),description=f"Modcase#{modcasenumber} is of not of type : warn. Use `>delmodcase` to delete a non-warn modcase")
      return await ctx.send(embed = embed)
    await modcases.delete_many({"guilid": f"{ctx.guild.id}","modcase":modcasenumber,"type":"warn"})
    embed =discord.Embed(colour=discord.Colour.purple(),description=f"Modcase#{modcasenumber} of type : warn deleted successfully <a:tick:844553824991313961>")
    return await ctx.send(embed = embed)
  @commands.command(description = "Deletes a specific modcase")
  @commands.has_permissions(kick_members=True)
  async def delmodcase(self,ctx,modcasenumber:int):
    count = await modcases.count_documents({"guilid": f"{ctx.guild.id}","modcase":modcasenumber})
    if count ==0:
      embed =discord.Embed(colour=discord.Colour.purple(),description=f"Modcase#{modcasenumber} not found")
      return await ctx.send(embed = embed)
    await modcases.delete_many({"guilid": f"{ctx.guild.id}","modcase":modcasenumber})
    embed =discord.Embed(colour=discord.Colour.purple(),description=f"Modcase#{modcasenumber} deleted successfully <a:tick:844553824991313961>")
    return await ctx.send(embed = embed)

  @commands.command(description = "Shows Mod History of a Member")
  @commands.has_permissions(kick_members=True)
  async def modhistory(self, ctx, member: discord.Member,pageno:int=1):
    if pageno <1:
      embed = discord.Embed(colour=discord.Colour.purple(),description="The Page No. should be a natural no.")
      return await ctx.send(embed=embed)
    c = await modcases.count_documents({"guilid": f"{ctx.guild.id}", "memberid": member.id})
    if c == 0:
      embed = discord.Embed(colour=discord.Colour.purple(), description="User has no modhistory")
      return await ctx.send(embed=embed)

    data = modcases.find({"guilid": f"{ctx.guild.id}", "memberid": member.id})
    desc = ''''''
    warns = 0
    mute = 0
    tempmutes = 0
    kicks = 0
    bans = 0
    l=[]
    async for x in data:
      if x['type'] == "tempmute":
        check = len(f"**ModCase#{x['modcase']}** | Moderator - <@{x['moderatorid']}>({x['moderatorname']})" + "\n" + f"***Type :*** {x['type']}\n***Duration*** : {x['duration']}\n***Reason :*** `{x['reason']}`\n***Date***: {x['date']}" + "\n\n")
        if (len(desc) + check) > 1000:
          embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
          embed.set_author(name=f"{member.name}#{member.discriminator}'s Modhistory", icon_url=member.avatar.url)
          l.append(embed)
          desc = ""
        desc = desc + f"**ModCase#{x['modcase']}** | Moderator - <@{x['moderatorid']}>({x['moderatorname']})" + "\n" + f"***Type :*** {x['type']}\n***Duration*** : {x['duration']}\n***Reason :*** `{x['reason']}`\n***Date***: {x['date']}" + "\n\n"
      else:
        check = len(f"**ModCase#{x['modcase']}** | Moderator - <@{x['moderatorid']}>({x['moderatorname']})" + "\n" + f"***Type :*** {x['type']}\n***Reason :*** `{x['reason']}`\n***Date :*** {x['date']}" + "\n\n")
        if (len(desc) + check) > 1000:
          embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
          embed.set_author(name=f"{member.name}#{member.discriminator}'s Modhistory", icon_url=member.avatar.url)
          l.append(embed)
          desc = ""
        desc = desc + f"**ModCase#{x['modcase']}** | Moderator - <@{x['moderatorid']}>({x['moderatorname']})" + "\n" + f"***Type :*** {x['type']}\n***Reason :*** `{x['reason']}`\n***Date :*** {x['date']}" + "\n\n"
      if x['type'] == "mute":
        mute += 1
      elif x['type'] == "warn":
        warns += 1
      elif x['type'] == "tempmute":
        tempmutes += 1
      elif x['type'] == "kick":
        kicks += 1
      elif x['type'] == "ban":
        bans += 1
    if desc != "":
      embed = discord.Embed(colour=discord.Colour.purple(), description=desc)
      embed.set_author(name=f"{member.name}#{member.discriminator}'s Modhistory", icon_url=member.avatar.url)
      l.append(embed)

    if pageno > len(l):
      if len(l) ==1:
        embed = discord.Embed(colour=discord.Colour.purple(),description=f"There is only 1 page")
      else:
        embed = discord.Embed(colour=discord.Colour.purple(),description=f"The Page No. should be between 1 and {len(l)}")
      return await ctx.send(embed=embed)
    embed = l[pageno - 1]
    embed.set_footer(text=f"{warns} warning(s), {mute} mute(s), {tempmutes} tempmute(s), {kicks} kick(s) , {bans} ban(s)\nPage {pageno}/{len(l)}\nYou can use >modhistory <member> <pageno> to go to different pages")
    await ctx.send(embed=embed)
    return
  
  

async def setup(client):
  await client.add_cog(Mod(client))