import discord
import requests
import os
import urllib.parse
from discord.ext import commands
import aiohttp
import aiofiles
import json

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.owner = discord.ClientUser

    @commands.Cog.listener("on_message")
    async def reaction_stuff(self, message):
        if (message.author == self.client.user):  # Not the BOT
            return
        # Server Specific
        if (message.author.bot):
          return
        with open("CTI.json","r") as f:
          m = json.load(f)

        if message.guild is not None:
          if str(message.guild.id) not in m:
            return

        
        text = message.content
        x = text.find("```")
        if x!=-1:
          if x !=0:
            if text[x-1]=="\\":
              return
          a=text.find("```")
          text=text[(a+3):]
            

          if text.find("```")!=-1:
            a=text.find("```")
            text=text[:a]
            if text[a-1]=="\\":
              return
            else:            

              my_emoji = "<:logoreact:832153854492672011>"
              await message.add_reaction("<:logoreact:832153854492672011>")

              def check(reaction, user):
                  return (user == message.author) and (str(reaction.emoji) == my_emoji) and (reaction.message == message)

              try:
                  reaction, user = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
              except:
                  await message.remove_reaction("<:logoreact:832153854492672011>",self.client.user)
                  return  # Exit Function (Timed Out)

              # Author pressed correct emoji in time
              await message.remove_reaction("<:logoreact:832153854492672011>",self.client.user)
              getVars = {'code': code_for_url(text),
              "backgroundColor": "rgb(189, 16, 224, 93)", "exportSize": "4x", "fontFamily": "MonoLisa", "theme": "dracula-pro", "language": "auto"}

              url = 'https://ctiinferno.herokuapp.com/?'
              complete_url = url+urllib.parse.urlencode(getVars)

              async with aiohttp.ClientSession() as session:
                async with session.post(url, json = getVars) as data:
                  if data.status != 200:
                    await message.channel.send('Something wrong happened with your request')
                    return
                  file = await aiofiles.open('code.png', mode = 'wb')
                  await file.write(await data.read())
                  await file.close()


              outpath = "code.png"


              await message.channel.send(file=discord.File('code.png'))
              if os.path.exists(outpath):
                  os.remove(outpath)
              return


def code_for_url(text):
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
    text = urllib.parse.quote_plus(text)
    return text


async def setup(client):  # Cog setup command
    await client.add_cog(Events(client))