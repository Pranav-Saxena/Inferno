import discord
from discord.ext import commands
import random
from datetime import datetime
from typing import Optional
from discord import Member
import requests
import json
import qrcode
from PIL import Image, ImageFilter,ImageDraw
import os
import aiohttp
import io
import asyncio
import re
import motor.motor_asyncio
import nest_asyncio
import datetime
import time
nest_asyncio.apply()
cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb_cluster_auth")
notedb = cluster["notes"]["notes"]
class Utility(commands.Cog):
  def __init__(self,client):
    self.client = client
  
  @commands.command()
  async def raw(self,ctx):
    '''Reply to a message and type the cmd raw with prefix to get the text pasted in hastebin and get its link'''
    
    if ctx.message.reference is None:
      await ctx.reply("No message referenced/replied to . Pls reply to a message and then use this command")
      return
    else:
      repliedmsg = ctx.message.reference.cached_message.content
      
      async with aiohttp.ClientSession() as session:
        async with session.post('https://paste.pythondiscord.com//documents',data = f"{repliedmsg}") as req:
  
          reqcontent = await (req.text())


          key = json.loads(reqcontent)["key"]
          await ctx.reply(f"https://paste.pythondiscord.com//{key}")
      return

  @commands.command(aliases=["hbcode"])
  async def hastebin(self,ctx):
    '''Reply to a message and type the cmd hastebin(or hbcode) with prefix to extract the code from the replied message -->get it pasted on hastebin and get its link '''
    
    if ctx.message.reference is None:
      await ctx.reply("No message referenced/replied to . Pls reply to a message and then use this command")
      return
    
    # repliedmsg = ctx.message.reference.cached_message.content
    # x = repliedmsg.find("```")
    elif ctx.message.reference.cached_message.content.find("```")!=-1:
      repliedmsg = ctx.message.reference.cached_message.content
      x = repliedmsg.find("```")
      if x !=0:
        if repliedmsg[x-1]=="\\":
          await ctx.reply("code not found in the message. If the content you want to paste on hastebin is not a code use the command 'raw'")
          return
      a=repliedmsg.find("```")
      repliedmsg=repliedmsg[(a+3):]
      if repliedmsg.find("```")!=-1:
        a=repliedmsg.find("```")
        
        if repliedmsg[a-1]=="\\":
              await ctx.reply("code not found in the message. If the content you want to paste on hastebin is not a code use the command 'raw'")
              return
        else:      
          repliedmsg=repliedmsg[:a]
          text = repliedmsg #of replied msg 
                  
          if not text[0].isspace():
            x = text.find("\n")
            if len(text[:x].split()) == 1 and text[x-1]!=" ":
              if x!=-1:
                temp = text[x:].split()
                c= True
                for i in temp:
                  if i=="":
                    c = True
                  else:
                    c= False
                    break
                if c==True:
                  text = text[:x]
                if c==False:
                  if x!=-1 and not text[(x-1)].isspace():
                    a = text.find("\n")
                    text = text[(a+1):]
          if text.startswith("\n"):
            text = text[1:]
          if text.endswith("\n"):
            text = text[:(len(text)-1)]       
          
          
          async with aiohttp.ClientSession() as session:
            async with session.post('https://paste.pythondiscord.com//documents',data = f"{text}") as req:
              reqcontent = await (req.text())


              key = json.loads(reqcontent)["key"]
              await ctx.reply(f"https://paste.pythondiscord.com//{key}")
          return
    else:
      await ctx.reply("code not found in the message. If the content you want to paste on hastebin is not a code use the command 'raw'")
      return
  @commands.command(description = "Sends the id of the emoji")
  async def emoji(self, ctx, *, emoji):
    await ctx.send(f"\\{str(emoji)}")
  @commands.command(aliases=["qrcode","qrgen"],description = "Generates qr code for the text entered")
  async def qr(self,ctx,*,text):
    img = qrcode.make(str(text))
    img.save('/home/pranav/Inferno/Inferno/qrout.png')
    await ctx.send(file=discord.File('/home/pranav/Inferno/Inferno/qrout.png'))
    os.remove("/home/pranav/Inferno/Inferno/qrout.png")
    return
  
#----------------notes----------------------------
  @commands.group(invoke_without_command=True,cooldown_after_parsing=True,description = "Create, Edit, View or Remove Note(s) from your Notepad!",aliases = ["note","notepad","todo","todo-list"],extras = {"cooldown":"5 seconds"})
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def notes(self, ctx):
      embed = discord.Embed(colour=discord.Colour.purple(),description="The available subcommands are `add`,`view`,`edit`,`remove`\n\n**Sample Usage:-**\n`>notes view [notename]` or `>notes view`\n`>notes add <notename> <note>`\n`>notes edit <notename> <entrynumber> <newnote>`\n`>notes remove <notename> [entrynumber]`",timestamp=datetime.datetime.utcnow())
      embed.set_footer(text=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
      return await ctx.send(embed=embed)
  @notes.command(description = "Creates a New Note / Adds an Entry to a Note!\n\nIf a Note doesn't exist, a new Note is created\notherwise if a Note exists and if you use this command, a new entry will be created")
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def add(self,ctx,notename,*,note):
    stats = await notedb.find_one({"id": str(ctx.author.id),"notename":notename})
    if len(notename)>50:
        embed = discord.Embed(colour=discord.Colour.purple(),
                              description="<a:infernocross:844577707727388742> NoteName cannot be greater then 50 characters")
        return await ctx.send(embed=embed)

    if len(note) <= 100:
      if stats is None:
        countnotename = await notedb.count_documents({"id": str(ctx.author.id)})
        if countnotename ==15:
          embed = discord.Embed(colour=discord.Colour.purple(),description="<a:infernocross:844577707727388742>You can have max 15 Notes.")
          return await ctx.send(embed=embed)
        notevalue = {"1":note}
        newuser = {"id": str(ctx.author.id), "notename":notename,"note": notevalue}
        await notedb.insert_one(newuser)
        embed = discord.Embed(title="Note Added!",colour = discord.Colour.purple(),description=f'''
Your Note has been added!!

**{notename}**
{note}
''',timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=embed)

      else:
        data = notedb.find({"id": str(ctx.author.id),"notename":notename})
        async for x in data:
          num = len(x['note'])
          notedata = x['note']
        
        if num > 15:
            embed = discord.Embed(colour=discord.Colour.purple(),description="<a:infernocross:844577707727388742>You can have max 15 entries in a note.")
            return await ctx.send(embed=embed)
        else:
          notedata[str(num+1)] = note
          newdata = {"id": str(ctx.author.id),"notename":notename,"note":notedata}
          await notedb.replace_one({"id": str(ctx.author.id),"notename":notename},newdata)
          embed = discord.Embed(title="Note Updated!", colour=discord.Colour.purple(), description=f'''
A New Entry has been Added!!

**{notename}**
{note}
''', timestamp=datetime.datetime.utcnow())
          embed.set_footer(text = f"{ctx.author.name}#{ctx.author.discriminator}",icon_url=ctx.author.avatar.url)
          return await ctx.send(embed=embed)

    else:
      embed = discord.Embed(colour = discord.Colour.purple(),description="<a:infernocross:844577707727388742> Note cannot be greater then 100 characters")
      return await ctx.send(embed=embed)
    return
  @notes.command(description="Shows your Notes!\n\nIf no notename is mentioned, then list of notes will be shown, otherwise if a notename is mentioned then its entries will be shown!")
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def view(self, ctx , notename = None):
    if notename is None:
      count = await notedb.count_documents({"id": str(ctx.author.id)})
      if count ==0:
        embed = discord.Embed(
                    timestamp=ctx.message.created_at,
                    color=discord.Colour.purple(),description=f"<a:infernocross:844577707727388742> You don't have any Notes")
        return await ctx.send(embed=embed)

      else:
        data = notedb.find({"id": str(ctx.author.id)})
        desc = ''''''
        c=1
        async for x in data:
            desc = desc + f"**{c}.** {x['notename']}\n"
            c+=1
        embed = discord.Embed(
                    title="Here are your notes!\n", timestamp=datetime.datetime.utcnow(), description=f"{desc}\nUse `>notes view [notename]` to get the contents of the note", color=discord.Colour.purple()
                )
        embed.set_footer(text=f"{ctx.author.name}#{ctx.author.discriminator}",icon_url=ctx.author.avatar.url)
        return await ctx.send(embed=embed)
    else:
        count = await notedb.count_documents({"id": str(ctx.author.id),"notename":notename})
        if count ==0:
            embed = discord.Embed(
                color=discord.Colour.purple(),description=f"<a:infernocross:844577707727388742> Note **{notename}** not found.")
            return await ctx.send(embed=embed)
        else:
            data = await notedb.find_one({"id": str(ctx.author.id),"notename":notename})
            desc = ''''''
            c = 1
            for x in data['note']:
                desc = desc + f"**{c}.** {data['note'][x]}\n"
                c+=1
            embed = discord.Embed(
                title=f"Contents of {notename}!", timestamp=datetime.datetime.utcnow(),
                description=f"{desc}",
                color=discord.Colour.purple()
            )
            embed.set_footer(text=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
            return await ctx.send(embed=embed)

  @notes.command(description="Deletes the Notes!\n\nIf no entry is mentioned ,then whole note gets deleted, otherwise only a single entry is removed!")
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def remove(self, ctx , notename , entrynumber :int = None):
    count = await notedb.count_documents({"id":str(ctx.author.id),"notename":notename})
    if count ==0:
      embed = discord.Embed(
            color=discord.Colour.purple(),
            description=f"<a:infernocross:844577707727388742> Note **{notename}** not found.")
      return await ctx.send(embed=embed)

    if entrynumber is None:
      await notedb.delete_many({"id":str(ctx.author.id),"notename":notename})
      embed = discord.Embed(title = "Note has been deleted!",colour=discord.Colour.purple(),timestamp=datetime.datetime.utcnow(),description=f"Note **{notename}** has been deleted successfully <a:tick:844553824991313961>")
      embed.set_footer(text=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
      return await ctx.send(embed=embed)

    data = await notedb.find_one({"id":str(ctx.author.id),"notename":notename})
    if entrynumber<=0 or entrynumber>len(data['note']):
      embed = discord.Embed(
            color=discord.Colour.purple(),
            description=f"<a:infernocross:844577707727388742> No such Entry exists")
      return await ctx.send(embed=embed)
    tempnote = data['note']
    oldnotedata = tempnote[str(entrynumber)]
    newnote = {}
    for i in tempnote:
      if int(i)<int(entrynumber):
        newnote[str(i)] = tempnote[str(i)]
      if int(i)>entrynumber:
        newnote[str(int(i)-1)] = tempnote[str(i)]

    await notedb.replace_one({"id":str(ctx.author.id),"notename":notename},{"id":str(ctx.author.id),"notename":notename,"note":newnote})
    embed = discord.Embed(colour=discord.Colour.purple(),title = "Entry has been deleted!",timestamp=datetime.datetime.utcnow(),
                          description=f"Entry ** {entrynumber}**, in Note **{notename}** has been deleted successfully <a:tick:844553824991313961>\n\n**The entry was :**  {oldnotedata}")
    embed.set_footer(text=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
    return await ctx.send(embed=embed)

  @notes.command(description = "Edits an Entry in a Note")
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def edit(self,ctx,notename,entrynumber:int,*,newnote):
      data = await notedb.find_one({"id": str(ctx.author.id), "notename": notename})
      if data is None:
        embed = discord.Embed(
              color=discord.Colour.purple(),
              description=f"<a:infernocross:844577707727388742> Note **{notename}** not found.")
        return await ctx.send(embed=embed)
      if entrynumber <= 0 or entrynumber > len(data['note']):
          embed = discord.Embed(
              color=discord.Colour.purple(),
              description=f"<a:infernocross:844577707727388742> No such Entry exists")
          return await ctx.send(embed=embed)

      notedata = data['note']
      notedata[str(entrynumber)]=newnote
      await notedb.replace_one({"id": str(ctx.author.id), "notename": notename},
                               {"id": str(ctx.author.id), "notename": notename, "note": notedata})
      embed = discord.Embed(colour=discord.Colour.purple(), title="Entry has been Updated!",
                            timestamp=datetime.datetime.utcnow(),
                            description=f"Entry ** {entrynumber}**, in Note **{notename}** has been updated successfully <a:tick:844553824991313961>\n\n**The Updated Entry is :**  {newnote}")
      embed.set_footer(text=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
      return await ctx.send(embed=embed)





async def setup(client):
  await client.add_cog(Utility(client))
