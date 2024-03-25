import discord
from discord.ext import commands,tasks
from itertools import cycle 
#status = cycle(["Ping to Know Prefix","Inferno | Ping to Know More"])
from random import randint

# status = cycle(["Ping to Know Prefix!","Inferno | Ping to Know More!"])

class Basic(commands.Cog):
  def __init__(self,client):
    self.client = client
    self.change_status.start()
    self.update_serversmembers.start()
  #events
  @commands.Cog.listener() # decorator for an event function
  async def on_ready(self):#self should be there as it's a class
    print("We have logged in as {0.user}".format(self.client))
    mh = 0
    for i in self.client.guilds:
        mh += len([m for m in i.members if not m.bot])
    s = len(self.client.guilds)
    status = [discord.Activity(type=discord.ActivityType.watching, name=f"{mh} members | {s} servers"),discord.Game("Ping to Know Prefix!"),discord.Game("Inferno | Ping to Know More!")]
    self.client.s = status
    self.client.loopcounterinfernovar =0
    # await self.client.change_presence(status = discord.Status.online,activity = discord.Game("Ping to know prefix!")) 

  
  # mh = 0
  # for i in self.client.guilds:
  #     mh += len([m for m in i.members if not m.bot])

  # s = len(self.client.guilds)

  # status = cycle([discord.Game("Ping to Know Prefix!"),discord.Game("Inferno | Ping to Know More!")])
  @tasks.loop(seconds = 10)
  async def update_serversmembers(self):
    mh = 0
    for i in self.client.guilds:
        mh += len([m for m in i.members if not m.bot])
    s = len(self.client.guilds)
    status = [discord.Activity(type=discord.ActivityType.watching, name=f"{mh} members | {s} servers"),discord.Game("Ping to Know Prefix!"),discord.Game("Inferno | Ping to Know More!")]
    self.client.s = status



  @tasks.loop(seconds=20)
  async def change_status(self):
    await self.client.change_presence(activity = self.client.s[self.client.loopcounterinfernovar])
    
    if self.client.loopcounterinfernovar<2:
      self.client.loopcounterinfernovar+=1
    else:
      self.client.loopcounterinfernovar=0      
    

    
  # @tasks.loop(seconds=120)
  # async def change_status(self):
  #   await self.client.change_presence(activity = discord.Game(name = next(status)))
  
  @change_status.before_loop
  async def before_printer(self):
      print('waiting...')
      await self.client.wait_until_ready()
      print("Ready to change status")
  #commands
  # @commands.command()
  # async def ping(self,ctx):
  #   embed = discord.Embed(title="**PONG!!**",colour = discord.Colour.purple())
  #   embed.add_field(name="\u200b",value = f"<a:ping:829274410586079306> **Bot Latency - {round(self.client.latency * 1000)} ms**",inline=True)
  #   embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=f'{ctx.author.avatar_url}')
  #   await ctx.reply(embed=embed)

  @commands.command(hidden=True)
  @commands.is_owner()
  async def leaveguild(self,ctx,guildid:int):
    server = self.client.get_guild(guildid)
    await server.leave()
    await ctx.send(f"Left Guild {server.name} Successfully <a:tick:844553824991313961>")
    return


async def setup(client):
  await client.add_cog(Basic(client))