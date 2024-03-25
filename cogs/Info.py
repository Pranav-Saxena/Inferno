import discord
from discord.ext import commands
import random
from datetime import datetime
from typing import Optional
from discord import Member
import time
import psutil
from utils import default
import requests
import os
import aiohttp

def is_it_me(ctx):
  return ctx.author.id == 704174691757064304

class Info(commands.Cog):
  def __init__(self,client):
    self.client = client
    
    self.process = psutil.Process(os.getpid())
  @commands.Cog.listener() # decorator for an event function
  async def on_ready(self):#self should be there as it's a class
    self.client.starttime = datetime.now()  
    
  @commands.command(description = "sends the bot invite")
  async def invite(self,ctx):
    embed=discord.Embed(title='Invite Me here',description='[Click Here](https://discord.com/api/oauth2/authorize?client_id=808690602358079508&permissions=261926419703&scope=bot%20applications.commands)',colour=discord.Colour.purple())  
    embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=f'{ctx.author.avatar.url}')
    button = discord.ui.Button(label="INVITE ME",style = discord.ButtonStyle.link,url = "https://discord.com/api/oauth2/authorize?client_id=808690602358079508&permissions=261926419703&scope=bot%20applications.commands",emoji = "<:invite:848985576731312128>")
    view = discord.ui.View() #this is the view object that holds all the components
    view.add_item(button)
    await ctx.send(embed=embed,view=view)
    return
  @commands.command(aliases=['BI','bi','Bi','BOTINFO','BotInfo'],description = "Sends information about bot")
  async def botinfo(self,ctx):

    embed=discord.Embed(title='Bot Information',colour=discord.Colour.purple())

    embed.set_thumbnail(url=self.client.user.avatar.url)
    mh = 0
    for i in self.client.guilds:
      mh += len([m for m in i.members if not m.bot])
           
    fields = [("<a:idbot:833314713499992104>ID", 808690602358079508, True),
              ("<a:crownowner:833356372984463360>Owner",'<@!704174691757064304>', True),
              ("<a:glitchinf:833357737596813322>Name", "\t\t**Inferno**",True),
              ("Default Prefix","<a:prefix:833360457057959946>",True),
              ("<a:server:833339676948430878>No. of servers", f"\t{int(len(list(self.client.guilds)))}",True),
              ("<a:watching:833359692046401537>Watching",f"{mh} members",True),
              ("<a:dsclogo:833343400911700080> Invite Me Here!","[Click Here to Add Me](https://discord.com/api/oauth2/authorize?client_id=808690602358079508&permissions=261926419703&scope=bot%20applications.commands)",True),
              ("<:support:849646432138559488> Join My Support Server","[Support Server](https://discord.gg/tTr6DvyRCH)",True)
              ]
              

    for name,value,inline in fields:
      embed.add_field(name=name,value=value,inline=inline)

    embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=f'{ctx.author.avatar.url}')
    await ctx.send(embed=embed)
    return
    
  @commands.command(description= "Tell's about the bot's latency")
  async def ping(self,ctx):
    embed = discord.Embed(title="Pong!",colour=discord.Colour.purple())
    before = time.monotonic()
    before_ws = int(round(self.client.latency * 1000, 1))
    message = await ctx.send(embed=embed)
    ping1 = (time.monotonic() - before) * 1000
    embednew = discord.Embed(title = "Pong!",description=f'''
    <a:ping3:843083143934509067> WS: {before_ws}ms  |  REST: {int(ping1)}ms''',colour=discord.Colour.purple())
    await message.edit(embed=embednew)
    return

  @commands.command(aliases=['UI',"ui","whois"],description= "Sends information about the user")
  async def userinfo(self,ctx, user: discord.Member=None):
    target = user
    if target is None:
      target = ctx.author
   
    embed=discord.Embed(title="",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
    embed.set_author(name = f"{target.name}'s Information",icon_url=target.avatar.url)
    embed.set_thumbnail(url=target.avatar.url)

    embed.add_field(name="User",value=f"{target.mention}",inline=True)
    embed.add_field(name="Discriminator",value=f"#`{target.discriminator}`",inline=True)
    embed.add_field(name="ID",value=f"`{target.id}`",inline=True)
    embed.add_field(name="Bot?",value=f"`{target.bot}`",inline=True)
    embed.add_field(name="Created",value=f"`{str(target.created_at)[0:11]}`",inline=True)
    embed.add_field(name="Joined",value=f"`{str(target.joined_at)[0:11]}`",inline=True)
    # embed.add_field()
    # statusdic= {"dnd":"<:dndstatus:834842734971715615> `Do Not Disturb`","online":"<:onlinestatus:834843265877540874> `Online`","offline":"<:offlinestatus:834843355871182848> `Offline`","idle":"<:idlestatus:834843368676392962> `Idle`"}
    # embed.add_field(name = "Status",value=f"{statusdic[str(target.status)]}",inline=True)
    # act = {"custom":"Custom Status","playing":"Playing","listening":"Listening","watching":"Watching","streaming":"Streaming","competing":"Competing"}
    # for i in target.activities:
    #   if str(i.type.name)=="streaming" or str(i.type.name)=="competing":
    #     embed.add_field(name=f"{act[str(i.type.name)]}",value=f"`{i.name}`",inline=True)
    #     continue
    #   try:
    #     if i.emoji is not None:
    #       embed.add_field(name=f"{act[str(i.type.name)]}",value=f"{i.emoji}`{i.name}`",inline=True)
    #     else:
    #       embed.add_field(name=f"{act[str(i.type.name)]}",value=f"`{i.name}`",inline = True)
    #   except:
    #     embed.add_field(name=f"{act[str(i.type.name)]}",value=f"`{i.name}`",inline = True)

    # if not target.bot:
    #   if target.is_on_mobile() and "offline" not in str(target.desktop_status):
    #     embed.add_field(name = "Platform" , value = "<:mobileapp:851510558528110600>& <:desktopapp:851513518288535562>")
    #   elif target.is_on_mobile() and "offline" not in str(target.web_status):
    #     embed.add_field(name = "Platform" , value = "<:mobileapp:851510558528110600>& <:webbrowser:851510384807510017>")
    #   elif target.is_on_mobile() and "offline" in str(target.desktop_status) and "offline" in str(target.web_status):
    #     embed.add_field(name = "Platform" , value = "<:mobileapp:851510558528110600>")
    #   elif "offline" not in str(target.desktop_status):
    #     embed.add_field(name = "Platform", value = "<:desktopapp:851513518288535562>")
    #   elif "offline" not in str(target.web_status):
    #     embed.add_field(name = "Platform", value = "<:webbrowser:851510384807510017>")
    #   else:
    #     pass

    if target.public_flags.hypesquad_bravery:
      embed.add_field(name="Hypesquad House",value="<:braveryhypesquad:835025805805092865> `House of Bravery`",inline=True)
    if target.public_flags.hypesquad_brilliance:
      embed.add_field(name="Hypesquad House",value="<:brilliancehypesquad:835025805552779276> `House of Brilliance`",inline=True)
    if target.public_flags.hypesquad_balance:
      embed.add_field(name="Hypesquad House",value="<:balancehypesquad:835025805951238174> `House of Balance`",inline=True)

    x = target.roles[1:]
    l=[]
    for i in x:
      l.append(i.mention)
    x=target.guild_permissions
    tempperms =[]
    for i in iter(x):
      if i[1]==True:
        tempperms.append(i[0])
    # print(iter(x))
    
    key_perms={"administrator":"Administrator","manage_guild":"Manage Server","manage_roles":"Manage Roles","manage_channels":"Manage Channels","manage_messages":"Manage Messages","manage_webhooks":"Manage Webhooks","manage_nicknames":"Manage Nicknames","manage_emojis":"Manage Emojis","kick_members":"Kick Members","ban_members":"Ban Members","mention_everyone":"Mention Everyone"}

    keyperms = []
    for i in key_perms:
      if i in tempperms:
        keyperms.append(key_perms[str(i)]) 

    if len(target.roles)!=1:
      embed.add_field(name="<a:crownowner:833356372984463360>Top role",value = target.top_role.mention, inline=False)    
      embed.add_field(name=f"Roles[{len(l)}]",value=f"{str(' '.join(l))}",inline=False)
    if len(target.roles)==1:
      embed.add_field(name=f"Roles[0]",value=f"`None`",inline=False)
    if len(keyperms)!=0:
      embed.add_field(name="Key Permissions:-",value=f"{str(', '.join(keyperms))}",inline=False)
    
    if not target.bot:
      if target == ctx.guild.owner:
        embed.add_field(name="Server Acknowledgements:-",value="Server Owner",inline=False)
      elif "Administrator" in keyperms:
        embed.add_field(name="Server Acknowledgements:-",value="Server Co-Admin",inline=False)
      elif "Manage Server" in keyperms or "Manage Channels" in keyperms:
        embed.add_field(name="Server Acknowledgements:-",value="Server Manager",inline=False)
      elif "Kick Members" in keyperms or "Ban Members" in keyperms:
        embed.add_field(name="Server Acknowledgements:-",value="Server Moderator",inline=False)


    embed.set_footer(text=f"Requested by {ctx.author.name}",icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)
    return
  @commands.command(aliases = ["mem","memcount","memberscount"],description="Sends the no. of members and bots in the server")
  async def members(self,ctx):
    server = ctx.guild
    l=[]
    x=server.members
    for i in x:
      if i.bot:
        l.append(i)
    embed = discord.Embed(title="Members Count",colour=discord.Colour.purple(),description=f'''**Members :** `{len(server.members)-len(l)}` \n**Bots :** `{len(l)}` \n**Total Members :** `{len(server.members)}`
    ''')
    await ctx.send(embed=embed)
    return
  @commands.command(aliases=["si","SI"],description = "Sends information about the server")
  async def serverinfo(self,ctx):
    server = ctx.guild
    embed=discord.Embed(title="",colour=discord.Colour.purple(),timestamp=datetime.utcnow())
    try:
      embed.set_author(name=f"{server.name}",icon_url=server.icon.url)
    except:
      embed.set_author(name=f"{server.name}")
    try:
      embed.set_thumbnail(url=server.icon.url)
    except:
      pass
    embed.add_field(name="Server Owner",value=f"{server.owner.mention}")
    # embed.add_field(name="Region",value=f"{server.region}")
    embed.add_field(name="ID",value=f"{server.id}")
    embed.add_field(name="Categories",value=f"{len(server.categories)}")
    embed.add_field(name="Text Channels",value=f"{len(server.text_channels)}")
    embed.add_field(name="Voice Channels",value=f"{len(server.voice_channels)}")
    l=[]
    x=server.members
    for i in x:
      if i.bot:
        l.append(i)

    embed.add_field(name="Members",value=f"{len(server.members)-len(l)}")
    embed.add_field(name="Bots",value=f"{len(l)}")
    embed.add_field(name="Roles",value=f"{len(server.roles)}")
    embed.add_field(name="Emojis",value=f"{len(server.emojis)}")
    embed.add_field(name="Created",value=f"{str(server.created_at)[:11]}")
    embed.add_field(name="Verification Level",value=f"{server.verification_level}",inline=True)
    try:
      embed.add_field(name="System Channel",value=f"<#{server.system_channel.id}>",inline=True)
    except:
      pass
    if "COMMUNITY" in server.features:
      try:
        embed.add_field(name="Community Updates Channel",value=f"<#{server.public_updates_channel.id}>",inline=True)
      except Exception as e:
        pass
      try:
        embed.add_field(name="Rules Channel",value=f"<#{server.rules_channel.id}>",inline=True)
      except Exception as e:
        pass
    embed.set_footer(text=f"Requested by {ctx.author.name}",icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)
    return
  
  @commands.command(hidden=True)
  @commands.check(is_it_me)
  async def listguilds(self,ctx):
    g =''
    index =1
    
    for guild in self.client.guilds:
      g= g + f'**{index})** *{guild.name}* \n({guild.id}) - {guild.member_count}\n'
      index+=1
    embed = discord.Embed(title=f"{self.client.user.display_name}'s Servers", colour=discord.Colour.purple(), description=g)
    await ctx.send(embed=embed)
    return 
  @commands.command(hidden=True)
  @commands.check(is_it_me)
  async def guildinfo(self,ctx,guildid:int):
    server = self.client.get_guild(guildid)
    l=[]
    x=server.members
    for i in x:
      if i.bot:
        l.append(i)
    embed = discord.Embed(title="Members Count",colour=discord.Colour.purple(),description=f'''**{server.name}**\n Owner - {server.owner.mention}({server.owner.name}#{server.owner.discriminator})\n **Members :** `{len(server.members)-len(l)}` \n**Bots :** `{len(l)}` \n**Total Members :** `{len(server.members)}`
    ''')
    await ctx.send(embed=embed)
    return 


  @commands.command(aliases = ["stats"],description = "Returns basic Information and Statistics about Inferno")
  async def about(self,ctx):
    mh = 0
    for i in self.client.guilds:
      mh += len([m for m in i.members if not m.bot])
    ramUsage = self.process.memory_full_info().rss / 1024**2 #self.process.memory_percent()
    cpuusage = self.process.cpu_percent()
    # avgmembers = sum(g.member_count for g in self.client.guilds) / len(self.client.guilds)
    # members = sum(g.member_count for g in self.client.guilds)
    embed = discord.Embed(colour=discord.Colour.purple())
    embed.set_author(name = "About Inferno#5047")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/808690602358079508/fee29f558273236f8e07ef4774152a31.png?size=256")
    # embed.add_field(name="Last boot", value=default.timeago(datetime.now() - self.client.uptime), inline=False)
    embed.add_field(
            name=f"Developer : catto_13",
            value='''\u202b 
**Language** : Python 3.8.5
**Library** : discord.py 2.0 (Master Branch)''',
            inline=False)
    # embed.add_field(name="Language", value="Python 3.8.5", inline=False)
    # embed.add_field(name="Library", value="discord.py 2.0 (Master Branch)", inline=False)
    embed.add_field(name="**Bot Info**", value=f'''```Last boot : {default.timeago(datetime.now() - ctx.bot.starttime)}
Servers : {len(self.client.guilds)}
Members : {mh}
Commands loaded : {len([x.name for x in self.client.commands])-17}```''', inline=False)
    embed.add_field(name="System Info", value=f'''```RAM : {round(ramUsage,2)} MB
CPU : {psutil.cpu_percent()}%```''', inline=False)
    embed.set_footer(text="Inferno",icon_url="https://cdn.discordapp.com/avatars/808690602358079508/fee29f558273236f8e07ef4774152a31.png?size=256")
    await ctx.send(embed=embed)    
    return 
  
  @commands.command(description = "Vote for Inferno")
  async def vote(self,ctx):
    embed = discord.Embed(colour = discord.Colour.purple(),description = '''
[top.gg](https://top.gg/bot/808690602358079508)
[Void Bots](https://voidbots.net/bot/808690602358079508/)''')
    embed.set_author(name = "Vote Me Here")
    button = discord.ui.Button(label="VOID BOTS",style = discord.ButtonStyle.link,url = "https://voidbots.net/bot/808690602358079508/",emoji = "<:voidbots:849563416830148619>")
    buttontop = discord.ui.Button(label="TOP.GG",style = discord.ButtonStyle.link,url = "https://top.gg/bot/808690602358079508",emoji = "<:topgg2:854604720160243732>")

    view = discord.ui.View()
    view.add_item(button)
    view.add_item(buttontop)
    await ctx.send(embed = embed,view=view)
# r = requests.post(url, headers=headers, json=json)
  @commands.command(description = "Sends invite of Inferno's Official Support Server")
  async def support(self,ctx):
    embed = discord.Embed(colour = discord.Colour.purple(),description='''
    
[Support Server](https://dsc.gg/infernocommunity)''')
    embed.set_author(name = "Join my Support Server")
    button = discord.ui.Button(label="SUPPORT SERVER",style = discord.ButtonStyle.link,url = "https://discord.gg/tTr6DvyRCH",emoji = "<:support:849646432138559488>")
    view = discord.ui.View() #this is the view object that holds all the components
    view.add_item(button) #this adds the button onto the view
    await ctx.send(embed=embed,view=view)
  
  @commands.command(cooldown_after_parsing=True, description="Suggest Some Features in Inferno/Inferno Community Server")
  @commands.cooldown(1, 60, commands.BucketType.user)
  async def suggest(self, ctx, *, msg):
    channel_only = self.client.get_channel(862224907709710346)
    up = "\U0001f44d"
    down = "\U0001f44e"

    embed = discord.Embed(
            timestamp=ctx.message.created_at, title=f"Suggestion By {ctx.author}",colour = discord.Colour.purple()
        )
    embed.add_field(name="Suggestion", value=msg)
    embed.set_footer(
            text=f"Wait until your suggestion is approved",
            icon_url=f"{ctx.author.avatar.url}",
        )
    message = await channel_only.send(embed=embed)
    await message.add_reaction(up)
    await message.add_reaction(down)
    await ctx.send("**Your Suggestion Has Been Recorded**")
    return


async def setup(client):
  await client.add_cog(Info(client))