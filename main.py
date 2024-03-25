import discord 
from discord.ext import commands
import os 
import random
import time
import asyncio
import json
import youtube_dl
import aiohttp
import aiofiles 
import urllib
import jishaku
#if we create a new cog and don't rerun the code we can use the load command to load the cog 


intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True,invites = True, message_content = True)

#---------------server prefixes----------------------------
def get_prefix(client,message):
  try:
    with open ("prefixes.json",'r') as f:
      prefixes = json.load(f)
        
    return commands.when_mentioned_or(prefixes[str(message.guild.id)])(client, message)
  except:
    return commands.when_mentioned_or(">")(client, message)

client = commands.Bot(command_prefix=commands.when_mentioned_or(">"), intents = intents)

from customhelp import MyHelp
client.help_command = MyHelp()
def is_it_me(ctx):
  return ctx.author.id == 704174691757064304

@client.event
async def on_guild_join(guild):
  with open("prefixes.json",'r') as f:
    prefixes = json.load(f)
  
  prefixes[str(guild.id)] = '>' #default value 

  with open("prefixes.json",'w') as f:
    json.dump(prefixes,f,indent=4)



@client.event
async def on_guild_remove(guild):
  with open("prefixes.json",'r') as f:
    prefixes = json.load(f)
  
  prefixes.pop(str(guild.id)) 

  with open("prefixes.json",'w') as f:
    json.dump(prefixes,f,indent=4)


# @client.command()
# @commands.check_any(commands.has_permissions(manage_guild=True), commands.check(is_it_me))
# async def changeprefix(ctx,prefix):
#   with open("prefixes.json",'r') as f:
#     prefixes = json.load(f)
    
#   prefixes[str(ctx.guild.id)] = prefix

#   with open("prefixes.json",'w') as f:
#     json.dump(prefixes,f,indent=4)
#   await ctx.send("prefix successfully changed to "+ prefix)

#--------------------ping to know prefix------------------------------
@client.event
async def on_message(ctx):
  if ctx.content == f"<@!{client.user.id}>" or ctx.content == f"<@{client.user.id}>":
    if ctx.author.bot:
      return
    with open("prefixes.json",'r') as f:
      prefixes = json.load(f)
      prefix = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(colour=discord.Colour.purple())
    embed.set_author(name =f'''My prefix is {prefix}. 
Type {prefix}help to know more''',icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author.name}",icon_url= client.user.avatar.url)
    await ctx.channel.send(embed=embed)
  await client.process_commands(ctx)


# @client.event
# async def on_command_error(ctx,error):
#   # if isinstance(error,commands.CommandNotFound):
#   #   await ctx.send(ctx.message.content[1:] + " is not a valid command")

@client.command()
@commands.check(is_it_me)
async def load(ctx,extension):
  try:
      await client.load_extension(f'cogs.{extension}')
  except Exception as e:
      print(f'Could not load cog {extension}: {str(e)}')
      await ctx.send(f"{extension} cog couldn't load")
  else:
      print(f'{extension} cog loaded successfully')
      await ctx.send(f'{extension} cog loaded successfully')
  # client.load_extension(f'cogs.{extension}')
@client.command()
@commands.check(is_it_me)
async def unload(ctx,extension):
  await client.unload_extension(f'cogs.{extension}')
  await ctx.send(f"Unloaded cog : {extension} successfully")
  print(f"Unloaded cog : {extension} successfully")
@client.command()
@commands.check(is_it_me) # to reload cog without the need of running whole code again
async def reload(ctx,extension):
  await client.unload_extension(f'cogs.{extension}')
  await client.load_extension(f'cogs.{extension}')
  await ctx.send(f"cog : {extension} reloaded successfully")
  print(f"cog : {extension} reloaded successfully")


# cog_list from all .py files in folder cogs
cogs = [fn[:-3] for fn in os.listdir(os.path.join(
        './', 'cogs')) if fn.endswith('.py')]

# cog loader
@client.event
async def setup_hook():
  # await client.load_extension("jishaku")
  
  for cog in cogs:
    try:
        await client.load_extension(f'cogs.{cog}')
    except Exception as e:
        print(f'Could not load cog {cog}: {str(e)}')
    else:
        print(f'{cog} cog loaded')




client.run("bot_token") 