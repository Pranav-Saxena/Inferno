'''
Random Fun Commands
'''

import discord
from discord.ext import commands,tasks
import random
import asyncpraw
import requests
import urllib.parse
import re
import aiohttp
import io
import art
# import shutil
class Fun(commands.Cog):
  def __init__(self,client):
    self.client = client
  
  @commands.command()
  async def editglitch(self,ctx,*,text):
    try:
      text.replace("`","")
      a = text.split(" (edited) ")
      x = "‫ "

      if len(a)==2:
        z=x+a[1]+" "+x+a[0]
        msg = await ctx.send(text) 
        await msg.edit(content = z)
        return
      elif text[-8:]=="(edited)"and len(text[:-8])!=0:
        z=text[:-8]+" "+x
        msg = await ctx.send(text) 
        await msg.edit(content = z)
        return
      elif text=="(edited)":
        z= " "+x
        msg = await ctx.send(text) 
        await msg.edit(content = z)
        return
      else:
        raise Exception   

    except Exception as e:
      await ctx.send('''type it in the following format:-```This is gonna be (edited) here```type the word ```(edited)``` where you want the edited symbol

Other accepted inputs are like:-```hello (edited)``` or only the ```(edited)``` word.
**Don't forget to write the command name and prefix before the text!!**''')
      await ctx.send(e)
      return
      
  @editglitch.error
  async def editglitch_error(self,ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send('''type the text as well in the following format:-```This is gonna be (edited) here```type the word ```(edited)``` where you want the edited symbol

Other accepted inputs are like:-```hello (edited)``` or only the ```(edited)``` word.
**Don't forget to write the command name and prefix before the text!!**''')
#----say-----------------
  @commands.command(aliases=["repeat"],description = "Makes the bot repeat the text")
  async def say(self,ctx,*,text):
    m = re.findall(r"<@&([0-9]+)>", text)
    if len(m) != 0 :
        await ctx.send("You can't mention any role using this command")
        return
    elif "@everyone" in text:
        await ctx.send("You can't mention everyone using this command")
        return
    elif "@here" in text:
        await ctx.send("You can't mass ping people using this command")
        return
    else:
        await ctx.send(text)
        return

#----8ball---------------
  @commands.command(aliases = ['8ball','8Ball',"8BALL"],description = "Ask the bot some question and it will reply from a list of 8 possible replies")
  async def _8ball(self,ctx,*,question):
    responses = [ 'It is certain.',
                    'It is decidedly so.',
                    'Without a doubt.',
                    'Yes – definitely.',
                    'You may rely on it.',
                    'As I see it, yes.',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    'Signs point to yes.',
                    'Reply hazy, try again.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    "Don't count on it.",
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good.',
                    'Very doubtful.']
    # await ctx.send(f"Question - {question} \nAnswer - {random.choice(responses)}")
    answer = random.choice(responses)
    embed = discord.Embed(title='**__8Ball__**',colour=discord.Colour.purple())
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/808689576461074447/826460581530697759/73957a992aacc9257881dda7b5d3df24.png')
    embed.add_field(name='Question',value=question,inline=False)
    embed.add_field(name='Answer',value=answer,inline=False)

    embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=f'{ctx.author.avatar.url}')
    await ctx.send(embed=embed)
    return
#---Memes------
  @commands.command(description="sends a random reddit meme")
  async def meme(self,ctx):
    reddit = asyncpraw.Reddit(
        client_id="client_id",
        client_secret="client_secret",
        user_agent="meme",
        username="user_name",
        password="password",
    )
    allsubs=[]
    subreddit = await reddit.subreddit("memes", fetch=True)
    async for submission in subreddit.hot(limit=70):
      allsubs.append(submission)
    randomsub= random.choice(allsubs)
    name = randomsub.title
    url = randomsub.url
    embed = discord.Embed(title=name,colour=discord.Colour.purple())
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    await reddit.close()
    return
  @commands.command(aliases=['AVATAR','Avatar',"av"],description="sends the avatar of the user")
  async def avatar(self,ctx,member:discord.Member=None):
    if member is None:
      member=ctx.author
      embed=discord.Embed(title='Avatar',colour=discord.Colour.purple())
      embed.set_image(url = member.avatar.url)
      embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=f'{ctx.author.avatar.url}')
      await ctx.reply(embed=embed)
      return
    else:
      embed=discord.Embed(title='Avatar',description=f"{member.mention}",colour=discord.Colour.purple())
      # embed.description(f"{member.mention}")
      embed.set_image(url = member.avatar.url)
      embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=f'{ctx.author.avatar.url}')
      await ctx.reply(embed=embed)
      return
  #-----------------snipe and edits-------------
  @commands.Cog.listener()
  async def on_message_delete(self, message):
    if message.guild is None:
      return
    snipe[message.guild.id] = (message.content,message.author,message.created_at,message.channel.name)
    return  
    

    #await message.channel.send(f'I sniped : \"{snipe[message.guild.id][0]}\" from {snipe[message.guild.id][1]} :smile:')

  @commands.Cog.listener()
  async def on_message_edit(self,before,after):
    # if before.author.bot:
    #   return
    if before.guild is None:
      return
    edit[before.guild.id]= (before.content,before.author,before.channel.name,before.created_at,after.content)
    return

  @commands.command(description = "returns the last deleted message")
  @commands.guild_only()
  async def snipe(self,ctx):
    try:
 
      content,author,timee,channel = snipe[ctx.guild.id]
      embed=discord.Embed(description = content, colour=discord.Colour.purple(),timestamp=timee)
      embed.set_author(name=f'{author.name}#{author.discriminator}',icon_url=author.avatar.url)
      embed.set_footer(text=f'Deleted in : #{channel}')
      await ctx.send(f'{author.name} has been sniped <a:nerfemoji:834075302246350858>',embed=embed)
      
      # await ctx.send(f'{author.name} has been sniped <a:nerfemoji:834075302246350858>')
      return
    except KeyError:
      embed=discord.Embed(colour=discord.Colour.purple())
      embed.set_author(name='There is no message to snipe',icon_url=ctx.author.avatar.url)
      await ctx.send(embed=embed)
      return
  @commands.command(aliases=['editss',"Edits","edits","esnipe"],description = "returns the last edited message")
  @commands.guild_only()
  async def editsnipe(self,ctx):

    try:
      messagelink = ctx.message.jump_url
      content,author,channel,timee,after = edit[ctx.guild.id]
      embed=discord.Embed(description =f'''**Changes made by** --> {author.mention}
      **From** --> {content}
      **To** --> {after}
      **Edited in :** #{channel} | [Message Link]({str(messagelink)})
      ''',colour=discord.Colour.purple())
      embed.set_author(name=f'Message edited',icon_url=author.avatar.url)
      # embed.set_footer(text=f'')
      await ctx.send(embed=embed)
      return
    except KeyError:
     
      embed=discord.Embed(colour=discord.Colour.purple())
      embed.set_author(name=f'There is no message to check',icon_url=ctx.author.avatar.url)
      await ctx.send(embed=embed)
      return
  @commands.command(description="Sends a random lenny face")
  async def lenny(self, ctx):
    lenny = random.choice([
                "( ͡° ͜ʖ ͡°)",
                "( ͠° ͟ʖ ͡°)",
                "ᕦ( ͡° ͜ʖ ͡°)ᕤ",
                "( ͡~ ͜ʖ ͡°)",
                "( ͡o ͜ʖ ͡o)",
                "͡(° ͜ʖ ͡ -)",
                "( ͡͡ ° ͜ ʖ ͡ °)﻿",
                "(ง ͠° ͟ل͜ ͡°)ง",
                "ヽ༼ຈل͜ຈ༽ﾉ",
            ]
        )
    return await ctx.send(lenny)

  @commands.command(
        description="Sends you a activity which you can do while you are bored"
    )
  async def bored(self, ctx, persons=1):
    if persons == None:
      return await ctx.send("You forgot person value")
    else:
      persons = str(persons)
      URL = f"https://www.boredapi.com/api/activity/?participants={persons}"

      async def check_valid_status_code(request):
        if request.status == 200:
          return await request.json()

        return False

      async def get_activity():
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as resp:
            
              data = await check_valid_status_code(resp)

              return data


      activity = await get_activity()
      temp_check = int(persons)
      if not activity or temp_check > 8:
        return await ctx.channel.send(
                    "Couldn't get activity at the moment. Try again later."
                )

      else:
          acti = activity["activity"]
          typee = activity["type"].capitalize()
          embed = discord.Embed(
                    timestamp=ctx.message.created_at,
                    title="Feeling Bored?",
                    description="Don't Worry, I am here to tell something you can do :)",
                    color=0xFF0000,
                )
          embed.add_field(name="Activity", value=f"{acti}", inline=False)
          embed.add_field(name="Type", value=f"{typee}", inline=False)
          embed.set_footer(
                    text=f"Requested By: {ctx.author.name}",
                    icon_url=f"{ctx.author.avatar.url}",
                )
          await ctx.send(embed=embed)
    return    
    
  @commands.command(description="sends a random dog image")
  async def dog(self,ctx):

    url = "https://some-random-api.ml/img/dog"

    async with aiohttp.ClientSession() as session:
      async with session.get(url) as data:
        response = await data.json()
        

    dogpic =  response['link']
    embed=discord.Embed(title='Dog',colour=discord.Colour.purple())
    embed.set_image(url=dogpic)
    embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=f'{ctx.author.avatar.url}')

    await ctx.send(embed=embed)
    return
  @commands.command(description="sends a random panda image")
  async def panda(self,ctx):

    url = "https://some-random-api.ml/img/panda"

    async with aiohttp.ClientSession() as session:
      async with session.get(url) as data:
        response = await data.json()

    pandapic =  response['link']
    embed=discord.Embed(title='Panda',colour=discord.Colour.purple())
    embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=f'{ctx.author.avatar.url}')

    embed.set_image(url=pandapic)
    await ctx.send(embed=embed)
    return
  @commands.command(description="sends a random cat image",aliases = ["catto"])
  async def cat(self,ctx):

    url = "https://some-random-api.ml/img/cat"

    async with aiohttp.ClientSession() as session:
      async with session.get(url) as data:
        response = await data.json()

    catpic =  response['link']
    embed=discord.Embed(title='Cat',colour=discord.Colour.purple())
    embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=f'{ctx.author.avatar.url}')

    embed.set_image(url=catpic)
    await ctx.send(embed=embed)
    return

  @commands.command(description="sends a random fox image")
  async def fox(self,ctx):

    url = "https://some-random-api.ml/img/fox"

    async with aiohttp.ClientSession() as session:
      async with session.get(url) as data:
        response = await data.json()

    foxpic =  response['link']
    embed=discord.Embed(title='Fox',colour=discord.Colour.purple())
    embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=f'{ctx.author.avatar.url}')

    embed.set_image(url=foxpic)
    await ctx.send(embed=embed)
    return

  @commands.command(alisases=["birb"],description="sends a random bird image")
  async def bird(self,ctx):

    url = "https://some-random-api.ml/img/birb"

    async with aiohttp.ClientSession() as session:
      async with session.get(url) as data:
        response = await data.json()

    birb =  response['link']
    embed=discord.Embed(title='Bird',colour=discord.Colour.purple())
    embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=f'{ctx.author.avatar.url}')

    embed.set_image(url=birb)
    await ctx.send(embed=embed)
    return
  @commands.command(description = "Sends a triggered GIF using the user's avatar")
  async def triggered(self,ctx,member:discord.Member=None):
    if member is None:
      member=ctx.author
    getVars = {'avatar': member.avatar.with_format("png").with_size(1024)}
    url = f'https://some-random-api.ml/canvas/triggered/?'
    async with aiohttp.ClientSession() as trigSession:
      async with trigSession.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar.with_format("png").with_size(1024)}') as trigImg: # get users avatar as png with 1024 size
        imageData = io.BytesIO(await trigImg.read()) # read the image/bytes
            
        await trigSession.close()
    f = discord.File(imageData, filename="triggered.gif")
    embed = discord.Embed(title="TRIGGERED!!",colour=discord.Colour.purple())
    embed.set_image(url="attachment://triggered.gif")
    await ctx.send(file=f,embed=embed)
    # os.remove("triggered.gif")
    return
  @commands.command(description = "returns song lyrics")
  async def lyrics(self,ctx,artist,*,song):
    
    url = f'https://api.lyrics.ovh/v1/{artist}/{song}'
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as data:
        response = await data.json()
    # print(response)
    lyrics = response['lyrics']
    embed = discord.Embed(title=f"{song.title()}",colour=discord.Colour.purple(),description=f"{lyrics[:1021]}...")
    await ctx.send(embed=embed)
    # os.remove("triggered.gif")
    return
  
  #----asciii
  @commands.command(description = "Converts text to ascii font")
  async def ascii(self,ctx,*,text):
    if len(text)>12:
      return await ctx.send("Limit the no. of characters to 12")
    text = art.text2art(text)
    return await ctx.send(f'''```
{text}
```''')


snipe={}
edit={}

async def setup(client):
  await client.add_cog(Fun(client))