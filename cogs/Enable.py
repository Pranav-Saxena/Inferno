'''
To enable CodeToImage in a server
'''

import discord
from discord.ext import commands
import json
def is_it_me(ctx):
  return ctx.author.id == 704174691757064304
class En(commands.Cog):
  def __init__(self,client):
    self.client= client
  @commands.command()
  @commands.has_permissions(manage_guild = True)
  # @commands.check_any(commands.has_permissions(manage_guild=True), commands.check(is_it_me))
  @commands.guild_only()
  async def enable(self,ctx,*,cmd):
    if str(cmd).lower() =="cti":
      with open("CTI.json","r") as f:
        m = json.load(f)
      
      c = str(ctx.guild.id) not in m
      f.close()
      
      if c == True:
        
        with open("CTI.json","r") as f:
          z = json.load(f)
        z[str(ctx.guild.id)]=str(ctx.guild.name)
        
        with open("CTI.json",'w') as x:
          json.dump(z,x,indent=4)
        await ctx.send("CTI Event enabled successfully")
      else:
        await ctx.send("CTI Event is already enabled")
    return
  @commands.command()
  @commands.has_permissions(manage_guild = True)
  # @commands.check_any(commands.has_permissions(manage_guild=True), commands.check(is_it_me))
  @commands.guild_only()
  async def disable(self,ctx,*,cmd):
    if str(cmd).lower() =="cti":
      with open("CTI.json","r") as f:
        m = json.load(f)
      
      c = str(ctx.guild.id) in m
      f.close()
      
      if c == True:
        
        with open("CTI.json","r") as f:
          z = json.load(f)
        z.pop(str(ctx.guild.id))
        with open("CTI.json",'w') as x:
          json.dump(z,x,indent=4)
        await ctx.send("CTI Event disabled successfully")
      else:
        await ctx.send("CTI Event is already disabled")
    return
  
async def setup(client):
  await client.add_cog(En(client))