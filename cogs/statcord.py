from discord.ext import commands

import statcord


class StatcordPost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = "statkey"
        self.api = statcord.Client(self.bot,self.key)
        self.api.start_loop()


    @commands.Cog.listener()
    async def on_command(self,ctx):
        self.api.command_run(ctx)


async def setup(bot):
    await bot.add_cog(StatcordPost(bot))