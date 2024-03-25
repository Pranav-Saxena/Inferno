'''
dummy help commands to send help category message for `>help category`
'''

import discord
from discord.ext import commands

class dummy(commands.Cog):
    def __init__(self,client):
        self.client = client
    #"fun":"Fun","games":"Games","image":"Image","info":"Info","mod":"Mod","utility":"Utility","misc":"Misc","events":"Events"
    @commands.command()
    async def fun(self,ctx):
        return
    @commands.command()
    async def games(self,ctx):
        return
    @commands.command()
    async def image(self,ctx):
        return
    @commands.command()
    async def info(self,ctx):
        return
    @commands.command(aliases = ["moderation","Moderation"])
    async def mod(self,ctx):
        return
    @commands.command()
    async def utility(self,ctx):
        return
    @commands.command()
    async def manager(self,ctx):
        return
    @commands.command()
    async def logging(self,ctx):
        return
    @commands.command(aliases= ["miscellaneous","Miscellaneous"])
    async def misc(self,ctx):
        return
    @commands.command(aliases= ["CTI"])
    async def cti(self,ctx):
        return
    @commands.command(aliases= ["reactions","reaction_roles"])
    async def rr(self,ctx):
        return
    # @commands.command(aliases = ["Stream","discordtogether"])
    # async def stream(self,ctx):
    #     return
    @commands.command()
    async def coderunner(self,ctx):
        return
    @commands.command()
    async def welcome(self,ctx):
        return

async def setup(client):
  await client.add_cog(dummy(client))