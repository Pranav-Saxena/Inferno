import discord
from discord.ext import commands
from os import getenv
import aiohttp
import asyncio
import time


class ChatBot(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.command(aliases=['chaton','CHATENABLE','Chaton','Chatenable'])
	async def chatenable(self,ctx, *, message=None):
		if ctx.guild != None:
			if ctx.guild.id not in [833364768076988458,762138894590017577,782879664720576522]:
				await ctx.send("Sorry, but this command is only available in the support server as of now :pensive:")
				return
		def check(message):
			return (message.author == ctx.author) and (message.channel == ctx.channel)
		global chat, chat_author_id
		chat =1
		chat_author_id = ctx.author.id
		await ctx.message.add_reaction("<a:catdance:852093435607515136>")
		while chat == 1:
			try:
				message = await self.client.wait_for('message',check = check,timeout = 120)
			except:
				return await ctx.send("chaton timedout")
			if message.author == self.client.user:	
				return
			if message.author.bot:
				return
			if chat_author_id == message.author.id:
				if message.content.lower() in ["chatdisable","chatoff",">chatoff",">chatdisable"]:
					await message.add_reaction("<a:catdance:852093435607515136>")
					chat = 0
					chat_author_id = 0
					return
				
				else:
					async with ctx.typing():
						async with aiohttp.ClientSession() as session:
							async with session.get(f"brainshop_api_key") as data:
								rep = await data.json()
								response = rep["cnt"]
								try:
									await message.reply(response,allowed_mentions = discord.AllowedMentions(roles=False, users=True, everyone=False,replied_user = False))
									chat = 1
								except discord.errors.HTTPException:
									await message.channel.send("Sorry Some error occured")    
		return


async def setup(client):
  await client.add_cog(ChatBot(client))