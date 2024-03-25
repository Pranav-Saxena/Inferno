import discord
from discord.ext import commands,tasks
import aiohttp
import asyncio
class BotStats(commands.Cog):
    def __init__(self,client):
        self.client=client
        self.poster.start()

    @tasks.loop(seconds=3600)
    async def poster(self):
        async with aiohttp.ClientSession() as session:
            #------voidbots--------------
            async with session.post("https://api.voidbots.net/bot/stats/808690602358079508", headers={
        "content-type":"application/json",
        "Authorization": "auth_key"
        }, json={"server_count": len(self.client.guilds), "shard_count": 0}) as data:
                embed = discord.Embed(title = f"{data.status}",color = discord.Colour.purple(),description = str(data))
                await self.client.get_channel(channel_id_for_updates).send(embed = embed) # replace channel_id_for_updates with the channel id where you want it to post
            
            #--------topgg--------------

            await asyncio.sleep(5)
            async with session.post("https://top.gg/api/bots/808690602358079508/stats", headers={
  "Authorization": "auth"
}, json={"server_count": len(self.client.guilds),"support": "tTr6DvyRCH",}) as data:
                embed = discord.Embed(title = f"{data.status}",color = discord.Colour.purple(),description = str(data))
                await self.client.get_channel(channel_id_for_updates).send(embed = embed) # replace channel_id_for_updates with the channel id where you want it to post

            #--------------------bfd---------------------
            await asyncio.sleep(5)        
            async with session.post("https://botsfordiscord.com/api/bot/808690602358079508", headers={
  "Authorization": "auth_key",
        "Content-Type":"application/json"
}, json={"server_count": len(self.client.guilds)}) as data:
                embed = discord.Embed(title = f"{data.status}",color = discord.Colour.purple(),description = str(data))
                await self.client.get_channel(channel_id_for_updates).send(embed = embed)# replace channel_id_for_updates with the channel id where you want it to post
        return
    @poster.before_loop
    async def before_printer(self):
        print('waiting for bot lists stats poster...')
        await self.client.wait_until_ready()
        print("Ready to post stats")
async def setup(client):
  await client.add_cog(BotStats(client))