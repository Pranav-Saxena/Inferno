'''
This code was to access discord-together activities when they weren't rolled out properly in 2021-22
'''


import discord
from discord.ext import commands

class discordtogether(commands.Cog):
    def __int__(self,client):
        self.client = client
    @commands.command(aliases = ["yttogether","youtubetogether","Ytstream"],description = "Watch youtube videos with your friends in vc with an interactive ui")
    @commands.bot_has_permissions(create_instant_invite=True)
    async def ytstream(self,ctx,channel:discord.VoiceChannel):
        invite  = await channel.create_invite(target_type=discord.InviteTarget.embedded_application,target_application_id=755600276941176913)
        embed = discord.Embed(title = "Youtube Together",colour = discord.Colour.purple(),description=f'''
[Click here]({invite}) to join ytstream in vc
**Note -** This feature will only work on desktop client or web app''')
        await ctx.send(embed = embed)

    @commands.command(aliases = ["chesstogether"],description= "play chess in vc with an interactive ui")
    async def chess(self, ctx, channel: discord.VoiceChannel):
        invite = await channel.create_invite(target_type=discord.InviteTarget.embedded_application,
                                             target_application_id=832012586023256104)
        embed = discord.Embed(title="Chess", colour=discord.Colour.purple(), description=f'''
[Click here]({invite}) to play chess in vc
**Note -** This feature will only work on desktop client or web app''')
        await ctx.send(embed=embed)

    @commands.command(aliases = ["poker"],description="play pokernight with your friends in vc with an interactive ui")
    async def pokernight(self, ctx, channel: discord.VoiceChannel):
        invite = await channel.create_invite(target_type=discord.InviteTarget.embedded_application,
                                             target_application_id=755827207812677713)
        embed = discord.Embed(title="Poker Night", colour=discord.Colour.purple(), description=f'''
[Click here]({invite}) to play Poker Night in vc
**Note -** This feature will only work on desktop client or web app''')
        await ctx.send(embed=embed)

    @commands.command(description = "play betrayal.io in vc with an interactive ui")
    async def betrayal(self, ctx, channel: discord.VoiceChannel):
        invite = await channel.create_invite(target_type=discord.InviteTarget.embedded_application,
                                             target_application_id=773336526917861400)
        embed = discord.Embed(title="Betrayal", colour=discord.Colour.purple(), description=f'''
[Click here]({invite}) to join Betrayal.io in vc
**Note -** This feature will only work on desktop client or web app''')
        await ctx.send(embed=embed)

    @commands.command(aliases = ["fishing"],description= "play fishington.io in vc with an interactive ui")
    async def fishington(self, ctx, channel: discord.VoiceChannel):
        invite = await channel.create_invite(target_type=discord.InviteTarget.embedded_application,
                                             target_application_id=814288819477020702)
        embed = discord.Embed(title="FishingTon", colour=discord.Colour.purple(), description=f'''
[Click here]({invite}) to play fishington in vc

**Note -** This feature will only work on desktop client or web app''')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(discordtogether(client))