import discord
from discord.ext import commands
import math
import os
import sys
import traceback



class Error(commands.Cog):
    def __init__(self,client):
      self.client=client

    def _get_error_embed(self, title: str, body: str):
        """Return an embed that contains the exception."""
        return discord.Embed(
            title=title,
            colour=discord.Colour.purple(),
            description=body
        )
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return
        # get the original exception
        error = getattr(error, "original", error)


        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send("This command cannot be used in direct messages.")
            except discord.Forbidden:
                
                raise error
            return
        elif isinstance(error, commands.BotMissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            if len(missing) > 2:
                fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)

            embed = discord.Embed(
                title="Missing Permissions",
                description=f"I am missing **{fmt}** permissions to run this command",
                color=discord.Colour.purple()
            )
            await ctx.send(embed=embed)
            return

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("This command has been disabled.")
            return

        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Cooldown",
                description=f"This command is on cooldown, please retry in {math.ceil(error.retry_after)}s.",
                color=discord.Colour.purple())
            await ctx.send(embed=embed)
            return

        elif isinstance(error, commands.MissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            if len(missing) > 2:
                fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)
            embed = discord.Embed(
                title="Insufficient Permission(s)",
                description=f"You need the **{fmt}** permission(s) to use this command.",
                color=discord.Colour.purple()
            )
            await ctx.send(embed=embed)
            return

        elif isinstance(error, commands.UserInputError):
            await self.handle_user_input_error(ctx, error)


        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title="Permissions Not Satisfied",
                color=discord.Colour.purple()
            )
            await ctx.send(embed=embed)
            return

        elif isinstance(error, commands.CommandNotFound):
            return      
        else:
            raise error
    async def handle_user_input_error(self, ctx, e) -> None:
        """
        Send an error message in `ctx` for UserInputError, sometimes invoking the help command too.
        * MissingRequiredArgument: send an error message with arg name and the help command
        * TooManyArguments: send an error message and the help command
        * BadArgument: send an error message and the help command
        * BadUnionArgument: send an error message including the error produced by the last converter
        * ArgumentParsingError: send an error message
        * Other: send an error message and the help command
        """
        if isinstance(e, commands.MissingRequiredArgument):
            embed = self._get_error_embed("Missing required argument", e.param.name)
            await ctx.send(embed=embed)
        elif isinstance(e, commands.TooManyArguments):
            embed = self._get_error_embed("Too many arguments", str(e))
            await ctx.send(embed=embed)
        elif isinstance(e, commands.BadArgument):
            embed = self._get_error_embed("Bad argument", str(e))
            await ctx.send(embed=embed)
        elif isinstance(e, commands.BadUnionArgument):
            embed = self._get_error_embed("Bad argument", f"{e}\n{e.errors[-1]}")
            await ctx.send(embed=embed)
        elif isinstance(e, commands.ArgumentParsingError):
            embed = self._get_error_embed("Argument parsing error", str(e))
            await ctx.send(embed=embed)
        else:
            embed = self._get_error_embed(
                "Input error",
                "Something about your input seems off. Check the arguments and try again."
            )
            await ctx.send(embed=embed)
            
async def setup(client):
  await client.add_cog(Error(client))