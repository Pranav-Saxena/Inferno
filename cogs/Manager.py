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

nest_asyncio.apply()
cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb_cluster_auth")
autorole = cluster["autorole"]["autorole"]
botar = cluster["botar"]["botar"]

def is_it_me(ctx):
  return ctx.author.id == 704174691757064304

class Manager(commands.Cog):
    def __init__(self,client):
        self.client = client 
    @commands.command(description="Creates a role with the the specific name and colour and hoist(show members separately)(True/False)\n`>createrole [name] [colour] [hoist]`")
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles  =True)
    async def createrole(self,ctx,name,colour: Union[discord.Colour , int],hoist : bool =False):
      role = await ctx.guild.create_role(name = name,colour = colour,hoist = hoist)
      embed = discord.Embed(title = "Role Created",colour=discord.Colour.purple(),description=f"Role {role.mention} created successfully")
      await ctx.send(embed=embed)
      return
    @commands.command(description="Deletes the mentioned role")
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles  =True)
    async def delrole(self,ctx,role:discord.Role):
      if role > ctx.guild.me.top_role:
        return await ctx.send("I can't delete that role because it's higher than my top role")
      elif role == ctx.guild.me.top_role:
        return await ctx.send("I can't delete that role because it is at same level as my top role")
      elif role.is_default():
        return await ctx.send("You can't delete the default role")
      elif role.is_integration():
        return await ctx.send("That role can't be deleted because it's managed by an integration")
      elif role.is_bot_managed():
        return await ctx.send("That role can't be deleted because it's managed by a bot")
      elif role.is_premium_subscriber():
        return await ctx.send("That role can't be deleted because it's a premium subscriber role (Eg : Server Booster role)")
      else:
        await role.delete()
        embed = discord.Embed(title = "Role Deleted",colour=discord.Colour.purple(),description=f"Role {role.name} deleted successfully <a:tick:844553824991313961>")
        await ctx.send(embed=embed)
      return
    @commands.command(aliases = ["editrolecolour","rolecolour"],description="Changes the colour of the mentioned role")
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles  =True)
    async def changerolecolour(self,ctx,role:discord.Role,colour :discord.Colour):
      if role > ctx.guild.me.top_role:
        return await ctx.send("I can't edit that role because it's higher than my top role")
      elif role == ctx.guild.me.top_role:
        return await ctx.send("I can't edit that role because it is at same level as my top role")
      elif role.is_default():
        return await ctx.send("You can't edit the default role")
      elif role.is_integration():
        return await ctx.send("That role can't be edited because it's managed by an integration")
      elif role.is_bot_managed():
        return await ctx.send("That role can't be edited because it's managed by a bot")
      elif role.is_premium_subscriber():
        return await ctx.send("That role can't be edited because it's a premium subscriber role (Eg : Server Booster role)")
      else:
        await role.edit(colour = colour)
        embed = discord.Embed(title = "Role Updated",colour=discord.Colour.purple(),description=f"Role {role.mention}'s colour changed successfully <a:tick:844553824991313961>")
        await ctx.send(embed=embed)
      return
    
    @commands.command(aliases = ["emojiadd","add_emoji"],description="Adds emoji to the server")
    @commands.has_permissions(manage_emojis = True)
    @commands.bot_has_permissions(manage_emojis  =True)
    async def addemoji(self,ctx,name:str,emoji:discord.PartialEmoji):
      limit = ctx.guild.emoji_limit
      normal = 0
      animated = 0
      for i in ctx.guild.emojis:
        if i.animated:
          animated +=1
        else:
          normal +=1
      
      if emoji.animated and animated>=limit:
        embed =  discord.Embed(colour=discord.Colour.purple(),description = "You Have exhausted your server limit to add animated emojis")
        return await ctx.send(embed = embed)
      elif not emoji.animated and normal>=limit:
        embed =  discord.Embed(colour=discord.Colour.purple(),description = "You Have exhausted your server limit to add non-animated emojis")
        return await ctx.send(embed = embed)
      elif emoji.animated and animated<limit:
        img = await emoji.read()
        e = await ctx.guild.create_custom_emoji(name = name, image = img)
        embed =  discord.Embed(title="Emoji Added",colour=discord.Colour.purple(),description = f"Emoji {e} added successfully")
        return await ctx.send(embed = embed)
      elif not emoji.animated and normal<limit:
        img = await emoji.read()
        e = await ctx.guild.create_custom_emoji(name = name, image = img)
        embed =  discord.Embed(title="Emoji Added",colour=discord.Colour.purple(),description = f"Emoji {e} added successfully")
        return await ctx.send(embed = embed)
      else:
        pass
      return
    @commands.command(aliases = ["deleteemoji"],description="Deletes emoji from the server")
    @commands.has_permissions(manage_emojis = True)
    @commands.bot_has_permissions(manage_emojis  =True)
    async def delemoji(self,ctx,emoji:discord.Emoji):
      await ctx.guild.delete_emoji(emoji)
      embed= discord.Embed(title = "Emoji Deleted",colour=discord.Colour.purple(),description = "Emoji deleted successfully <a:tick:844553824991313961>")
      return await ctx.send(embed=embed)
    
    #---------------autorole----------------------------------------------------------------------------------------
    @commands.command(aliases = ["ar","autorolesetup","arsetup"],description="Sets up autorole in the server. The mentioned role is assigned to a member(human only) upon joining the server")
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles  =True)
    async def autorole(self,ctx,role:discord.Role):
      if role > ctx.author.top_role and not ctx.author == ctx.guild.owner:
        return await ctx.send("The role mentioned is above your top role, you can't create autorole for that.")
      elif role == ctx.author.top_role and not ctx.author == ctx.guild.owner:
        return await ctx.send("The role mentioned is your top role, you can't create autorole for that.")
      elif role>ctx.guild.me.top_role:
        await ctx.send("**the role is above my top role. I can't assign that role to someone**")
        return
      elif role == ctx.guild.me.top_role:
        await ctx.send("**The role you want to give is my top role. I can't assign it to someone else")
        return
      elif role.is_bot_managed():
        return await ctx.send("The role is associated with a bot, it can't be assigned to someone else")
      elif role.is_integration():
        return await ctx.send("The role is managed by an integration, it can't be assigned to someone else")
      elif role.managed:
        return await ctx.send("The role is managed by some integration, it can't be assigned to someone else")
      elif role.is_default():
        return await ctx.send("The role is the default role, it can't be assigned to someone else")

      count = await autorole.count_documents({'guildid': f"{ctx.guild.id}"})
      if count!=0:
        embed = discord.Embed(colour=discord.Colour.purple(),description = "Autorole is already setup on this server. Use `>arupdate` to update the existing autorole.") 
        return await ctx.send(embed = embed)

      rinfo = {
        "guildid":str(ctx.guild.id),
        "roleid":role.id
      }
      await autorole.insert_one(rinfo)
      embed2 = discord.Embed(title="Autorole Created",colour = discord.Colour.purple(),description = f"{role.mention} role will be given to the users upon joining this server.\n\n**Note-** This role will only be given to humans.To create autorole for bots use `>botautorole` command.")
      return await ctx.send(embed = embed2)

    @commands.command(aliases = ["arupdate"],description="Edits Autorole to a new role")
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles  =True)
    async def autoroleupdate(self,ctx,newrole:discord.Role):
      if newrole > ctx.author.top_role and not ctx.author == ctx.guild.owner:
        return await ctx.send("The role mentioned is above your top role, you can't create autorole for that.")
      elif newrole == ctx.author.top_role and not ctx.author == ctx.guild.owner:
        return await ctx.send("The role mentioned is your top role, you can't create autorole for that.")
      elif newrole>ctx.guild.me.top_role:
        await ctx.send("**the role is above my top role. I can't assign that role to someone**")
        return
      elif newrole == ctx.guild.me.top_role:
        await ctx.send("**The role you want to give is my top role. I can't assign it to someone else")
        return
      elif role.is_bot_managed():
        return await ctx.send("The role is associated with a bot, it can't be assigned to someone else")
      elif role.is_integration():
        return await ctx.send("The role is managed by an integration, it can't be assigned to someone else")
      elif role.managed:
        return await ctx.send("The role is managed by some integration, it can't be assigned to someone else")
      elif role.is_default():
        return await ctx.send("The role is the default role, it can't be assigned to someone else")

      count = await autorole.count_documents({'guildid': f"{ctx.guild.id}"})
      if count == 0 :
        embed = discord.Embed(colour=discord.Colour.purple(),description = "Autorole is not setup on this server. Use `>autorole` command to setup autorole")
        return await ctx.send(embed = embed)
      newdata = {
        "guildid":str(ctx.guild.id),
        "roleid":newrole.id
      }
      await autorole.replace_one({"guildid":f"{ctx.guild.id}"},newdata)
      embed2 = discord.Embed(title = "Autorole Updated",colour = discord.Colour.purple(),description = f"{newrole.mention} role will be given to users upon joining the server from now on.\n\n**Note-** This role will only be given to humans.To create autorole for bots use `>botautorole` command.")
      return await ctx.send(embed = embed2)

    @commands.command(aliases = ["delar","delautorole","removeautorole","removear"],description="Removes Autorole from the server")
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles  =True)
    async def deleteautorole(self,ctx):
      count = await autorole.count_documents({'guildid': f"{ctx.guild.id}"})
      if count ==0:
        embed = discord.Embed(colour=discord.Colour.purple(),description = "Autorole is not setup on this server. Use `>autorole` command to setup autorole first.")
        return await ctx.send(embed = embed)
      info = autorole.find({'guildid': f"{ctx.guild.id}"})
      async for x in info:
        await autorole.delete_one(x)
      embed2 = discord.Embed(title = "Autorole Deleted",colour = discord.Colour.purple(),description = "Autorole deleted successfully <a:tick:844553824991313961>")
      return await ctx.send(embed = embed2)

      #--------------------botautorole------------------
    @commands.command(aliases = ["botar","botautorolesetup","botarsetup"],description="Sets up botautorole in the server. The mentioned role is assigned to a bot upon joining the server")
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles  =True)
    async def botautorole(self,ctx,role:discord.Role):
      if role > ctx.author.top_role and not ctx.author == ctx.guild.owner:
        return await ctx.send("The role mentioned is above your top role, you can't create botautorole for that.")
      elif role == ctx.author.top_role and not ctx.author == ctx.guild.owner:
        return await ctx.send("The role mentioned is your top role, you can't create botautorole for that.")
      elif role>ctx.guild.me.top_role:
        await ctx.send("**the role is above my top role. I can't assign that role to someone**")
        return
      elif role == ctx.guild.me.top_role:
        await ctx.send("**The role you want to give is my top role. I can't assign it to someone else")
        return
      elif role.is_bot_managed():
        return await ctx.send("The role is associated with a bot, it can't be assigned to someone else")
      elif role.is_integration():
        return await ctx.send("The role is managed by an integration, it can't be assigned to someone else")
      elif role.managed:
        return await ctx.send("The role is managed by some integration, it can't be assigned to someone else")
      elif role.is_default():
        return await ctx.send("The role is the default role, it can't be assigned to someone else")

      count = await botar.count_documents({'guildid': f"{ctx.guild.id}"})
      if count!=0:
        embed = discord.Embed(colour=discord.Colour.purple(),description = "BotAutorole is already setup on this server. Use `>botarupdate` to update the existing botautorole.") 
        return await ctx.send(embed = embed)

      rinfo = {
        "guildid":str(ctx.guild.id),
        "roleid":role.id
      }
      await botar.insert_one(rinfo)
      embed2 = discord.Embed(title="BotAutorole Created",colour = discord.Colour.purple(),description = f"{role.mention} role will be given to bots upon joining this server.\n\n**Note-** This role will only be given to bots.To create autorole for humans use `>autorole` command.")
      return await ctx.send(embed = embed2)

    @commands.command(aliases = ["botarupdate"],description="Updates botautorole setup in the server.")
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles  =True)
    async def botautoroleupdate(self,ctx,newrole:discord.Role):
      if newrole > ctx.author.top_role and not ctx.author == ctx.guild.owner:
        return await ctx.send("The role mentioned is above your top role, you can't create botautorole for that.")
      elif newrole == ctx.author.top_role and not ctx.author == ctx.guild.owner:
        return await ctx.send("The role mentioned is your top role, you can't create botautorole for that.")
      elif newrole>ctx.guild.me.top_role:
        await ctx.send("**the role is above my top role. I can't assign that role to someone**")
        return
      elif newrole == ctx.guild.me.top_role:
        await ctx.send("**The role you want to give is my top role. I can't assign it to someone else")
        return
      elif role.is_bot_managed():
        return await ctx.send("The role is associated with a bot, it can't be assigned to someone else")
      elif role.is_integration():
        return await ctx.send("The role is managed by an integration, it can't be assigned to someone else")
      elif role.managed:
        return await ctx.send("The role is managed by some integration, it can't be assigned to someone else")
      elif role.is_default():
        return await ctx.send("The role is the default role, it can't be assigned to someone else")
      count = await botar.count_documents({'guildid': f"{ctx.guild.id}"})
      if count == 0 :
        embed = discord.Embed(colour=discord.Colour.purple(),description = "BotAutorole is not setup on this server. Use `>botautorole` command to setup BotAutorole")
        return await ctx.send(embed = embed)
      newdata = {
        "guildid":str(ctx.guild.id),
        "roleid":newrole.id
      }
      await botar.replace_one({"guildid":f"{ctx.guild.id}"},newdata)
      embed2 = discord.Embed(title = "BotAutorole Updated",colour = discord.Colour.purple(),description = f"{newrole.mention} role will be given to bots upon joining the server from now on.\n\n**Note-** This role will only be given to bots.To create autorole for humans use `>autorole` command.")
      return await ctx.send(embed = embed2)
    
    
    @commands.command(aliases = ["delbotar","delbotautorole","removebotautorole","removebotar"],description="Removes BotAutorole from the server")
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles  =True)
    async def deletebotautorole(self,ctx):
      count = await botar.count_documents({'guildid': f"{ctx.guild.id}"})
      if count ==0:
        embed = discord.Embed(colour=discord.Colour.purple(),description = "BotAutorole is not setup on this server. Use `>botautorole` command to setup botautorole first.")
        return await ctx.send(embed = embed)
      info = botar.find({'guildid': f"{ctx.guild.id}"})
      async for x in info:
        await botar.delete_one(x)
      embed2 = discord.Embed(title = "BotAutorole Deleted",colour = discord.Colour.purple(),description = "BotAutorole deleted successfully <a:tick:844553824991313961>")
      return await ctx.send(embed = embed2)



async def setup(client):
  await client.add_cog(Manager(client))