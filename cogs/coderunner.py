import json
import re
from dataclasses import dataclass
import discord
from discord.ext import commands, tasks
from discord.utils import escape_mentions
# from aiohttp import ContentTypeError
import aiohttp
from .utils.codeswap import add_boilerplate
from .utils.errors import CodeRunInvalidContentType, CodeRunInvalidStatus, CodeRunNoOutput
#pylint: disable=E1101


@dataclass
class RunIO:
    input: discord.Message
    output: discord.Message


class CodeRunner(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.run_IO_store = dict()  # Store the most recent /run message for each user.id
        self.languages = {'brainfuck': 'brainfuck', 'bf': 'brainfuck', 'cjam': 'cjam', 'clojure': 'clojure', 'clj': 'clojure', 'cobol': 'cobol', 'cob': 'cobol', 'coffeescript': 'coffeescript', 'coffee': 'coffeescript', 'cow': 'cow', 'crystal': 'crystal', 'cr': 'crystal', 'dart': 'dart', 'dash': 'dash', 'typescript': 'typescript', 'deno-ts': 'typescript', 'deno': 'typescript', 'javascript': 'javascript', 'deno-js': 'javascript', 'dotnet': 'dotnet', 'cs': 'mono', 'csharp': 'mono', 'dragon': 'dragon', 'elixir': 'elixir', 'exs': 'elixir', 'emacs': 'emacs', 'el': 'emacs', 'elisp': 'emacs', 'erlang': 'erlang', 'erl': 'erlang', 'escript': 'erlang', 'awk': 'awk', 'gawk': 'awk', 'c': 'c', 'gcc': 'c', 'c++': 'c++', 'cpp': 'c++', 'g++': 'c++', 'd': 'd', 'gdc': 'd', 'fortran': 'fortran', 'f90': 'fortran', 'go': 'go', 'golang': 'go', 'golfscript': 'golfscript', 'groovy': 'groovy', 'gvy': 'groovy', 'haskell': 'haskell', 'hs': 'haskell', 'java': 'java', 'jelly': 'jelly', 'julia': 'julia', 'jl': 'julia', 'kotlin': 'kotlin', 'kt': 'kotlin', 'lisp': 'lisp', 'cl': 'lisp', 'sbcl': 'lisp', 'commonlisp': 'lisp', 'lolcode': 'lolcode', 'lol': 'lolcode', 'lci': 'lolcode', 'lua': 'lua', 'mono': 'mono', 'nasm': 'nasm', 'asm': 'nasm', 'nasm32': 'nasm', 'nasm64': 'nasm64', 'asm64': 'nasm64', 'nim': 'nim', 'node-javascript': 'javascript', 'node-js': 'javascript', 'js': 'javascript', 'ocaml': 'ocaml', 'ml': 'ocaml', 'octave': 'octave', 'matlab': 'octave', 'm': 'octave', 'osabie': 'osabie', '05AB1E': 'osabie', 'usable': 'osabie', 'paradoc': 'paradoc', 'pascal': 'pascal', 'freepascal': 'pascal', 'pp': 'pascal', 'pas': 'pascal', 'perl': 'perl', 'pl': 'perl', 'php': 'php', 'php8': 'php', 'html': 'php', 'ponylang': 'ponylang', 'pony': 'ponylang', 'ponyc': 'ponylang', 'prolog': 'prolog', 'plg': 'prolog', 'pure': 'pure', 'pyth': 'pyth', 'python2': 'python2', 'py2': 'python2', 'python': 'python', 'py': 'python', 'py3': 'python', 'python3': 'python', 'raku': 'raku', 'rakudo': 'raku', 'perl6': 'raku', 'p6': 'raku', 'pl6': 'raku', 'rockstar': 'rockstar', 'rock': 'rockstar', 'rocky': 'rockstar', 'ruby': 'ruby', 'ruby3': 'ruby', 'rb': 'ruby', 'rust': 'rust', 'rs': 'rust', 'scala': 'scala', 'sc': 'scala', 'swift': 'swift', 'ts': 'typescript', 'node-ts': 'typescript', 'tsc': 'typescript', 'vlang': 'vlang', 'v': 'vlang', 'yeethon': 'yeethon', 'yeethon3': 'yeethon', 'zig': 'zig'} # Store the supported languages and aliases
        self.run_regex_code = re.compile(
            r'(?s)>(?:edit_last_)?runcode(?: +(?P<language>\S*)\s*|\s*)(?:\n'
            r'(?P<args>(?:[^\n\r\f\v]*\n)*?)\s*|\s*)'
            r'```(?:(?P<syntax>\S+)\n\s*|\s*)(?P<source>.*)```'
            r'(?:\n?(?P<stdin>(?:[^\n\r\f\v]\n?)+)+|)'
        )
        self.run_regex_file = re.compile(
            r'(?s)>runcode(?: *(?P<language>\S*)|\s*)?'
            r'(?:\n(?P<args>(?:[^\n\r\f\v]\n?)*))?'
            r'(?:\n+(?P<stdin>(?:[^\n\r\f\v]\n*)+)|)'
        )
    async def get_api_parameters_with_codeblock(self, ctx):
        if ctx.message.content.count('```') != 2:
            raise commands.BadArgument('''Invalid command format!\n\n**Sample Format**\n\n>runcode <language>\ncommand line parameters (optional) - 1 per line\n
\\`\\`\\`\nyour code\n\\`\\`\\`\nstandard input (optional)\n''')

        match = self.run_regex_code.search(ctx.message.content)


        if not match:
            raise commands.BadArgument('''Invalid command format!\n\n**Sample Format**\n\n>runcode <language>\ncommand line parameters (optional) - 1 per line\n
\\`\\`\\`\nyour code\n\\`\\`\\`\nstandard input (optional)\n''')

        language, args, syntax, source, stdin = match.groups()
        
        if not language:
            language = syntax

        if language:
            language = language.lower()

        if language not in self.languages:
            raise commands.BadArgument(
                f'Unsupported language: **{str(language)[:1000]}**\nType `>help coderunner` to get list of available languages!'
            )
        if 'from os import system' in str(source) or 'os.system' in str(source):
            raise commands.BadArgument("\n<a:infernocross:844577707727388742> You can't import system function from os module ")
        if 'import subprocess' in str(source) :
            raise commands.BadArgument("\n<a:infernocross:844577707727388742> You can't import subprocess module ")

        if '../../config.yaml' in str(source):
            raise commands.BadArgument("\n<a:infernocross:844577707727388742> You can't access config files")
        return language, source, args, stdin

    async def get_api_parameters_with_file(self, ctx):
        if len(ctx.message.attachments) != 1:
            raise commands.BadArgument('Invalid number of attachments')

        file = ctx.message.attachments[0]

        MAX_BYTES = 65535
        if file.size > MAX_BYTES:
            raise commands.BadArgument(f'Source file is too big ({file.size}>{MAX_BYTES})')

        filename_split = file.filename.split('.')

        if len(filename_split) < 2:
            raise commands.BadArgument('Please provide a source file with a file extension')

        match = self.run_regex_file.search(ctx.message.content)

        if not match:
            raise commands.BadArgument('Invalid command format File')

        language, args, stdin = match.groups()

        if not language:
            language = filename_split[-1]

        if language:
            language = language.lower()

        if language not in self.languages:
            raise commands.BadArgument(
                f'Unsupported language: **{language}**\n[Request a new language](https://discord.gg/tTr6DvyRCH)'
            )

        source = await file.read()
        try:
            source = source.decode('utf-8')
        except UnicodeDecodeError as e:
            raise commands.BadArgument(str(e))

        if 'from os import system' in str(source) or 'os.system' in str(source):
            raise commands.BadArgument("\n<a:infernocross:844577707727388742> You can't import system function from os module ")
        if 'import subprocess' in str(source) :
            raise commands.BadArgument("\n<a:infernocross:844577707727388742> You can't import subprocess module ")

        if '../../config.yaml' in str(source):
            raise commands.BadArgument("\n<a:infernocross:844577707727388742> You can't access config files")
        return language, source, args, stdin
        return language, source, args, stdin

    async def get_run_output(self, ctx):
        # Get parameters to call api depending on how the command was called (file <> codeblock)
        if ctx.message.attachments:
            alias, source, args, stdin = await self.get_api_parameters_with_file(ctx)
        else:
            alias, source, args, stdin = await self.get_api_parameters_with_codeblock(ctx)

        # Resolve aliases for language
        language = self.languages[alias]

        # Add boilerplate code to supported languages
        source = add_boilerplate(language, source)

        # Split args at newlines
        if args:
            args = [arg for arg in args.strip().split('\n') if arg]

        if not source:
            raise commands.BadArgument(f'No source code found')

        # Call piston API
        
        data = {
            'language': alias,
            'version': '*',
            'files': [{'content': source}],
            'args': args,
            'stdin': stdin or "",
            'log': 0
        }
        # headers = {'Authorization': self.client.config["emkc_key"]}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://emkc.org/api/v2/piston/execute',
                json=data
            ) as response:
                try:
                    r = await response.json()
                except aiohttp.ContentTypeError:
                    raise CodeRunInvalidContentType('Invalid Content Type')
        if not response.status == 200:
            raise CodeRunInvalidStatus(f'status {response.status}: {r.get("message", "")}')

        comp_stderr = r['compile']['stderr'] if 'compile' in r else ''
        run = r['run']

        if run['output'] is None:
            raise CodeRunNoOutput('no output')

        # Logging
        # await self.send_to_log(ctx, language, source)

        # Return early if no output was received
        if len(run['output'] + comp_stderr) == 0:
            return "nooutput","noutput"
            # return f'Your code ran without output {ctx.author.mention}'

        # Limit output to 30 lines maximum
        output = '\n'.join((comp_stderr + run['output']).split('\n')[:30])

        # Prevent mentions in the code output
        output = escape_mentions(output)

        # Prevent code block escaping by adding zero width spaces to backticks
        output = output.replace("`", "`\u200b")

        # Truncate output to be below 2000 char discord limit.
        if len(comp_stderr) > 0:
            # introduction = f'{ctx.author.mention} I received compile errors\n'
            introduction = "compile"
        elif len(run['stdout']) == 0 and len(run['stderr']) > 0:
            # introduction = f'{ctx.author.mention} I only received error output\n'
            introduction = "error"
        else:
            # introduction = f'Here is your output {ctx.author.mention}\n'
            introduction = "proper"
        truncate_indicator = '[...]'
        len_codeblock = 7  # 3 Backticks + newline + 3 Backticks
        available_chars = 2000-len(introduction)-len_codeblock
        if len(output) > available_chars:
            output = output[:available_chars-len(truncate_indicator)] + truncate_indicator

        return (introduction,(
            '```\n'
            + output
            + '```'
        ))

    # async def delete_last_output(self, user_id):
    #     try:
    #         msg_to_delete = self.run_IO_store[user_id].output
    #         del self.run_IO_store[user_id]
    #         await msg_to_delete.delete()
    #     except KeyError:
    #         # Message does not exist in store dicts
    #         return
    #     except discord.NotFound:
    #         # Message no longer exists in discord (deleted by server admin)
    #         return

    # @commands.command(aliases=['del'])
    # async def delete(self, ctx):
    #     """Delete the most recent output message you caused
    #     Type "/run" or "/help" for instructions"""
    #     await self.delete_last_output(ctx.author.id)

    @commands.command()
    async def runcode(self, ctx, *, source=None):
        """Executes your code and returns the Output!\ntype `>help coderunner` to know more!"""
        # if self.client.maintenance_mode:
        #     await ctx.send('Sorry - I am currently undergoing maintenance.')
        #     return
        await ctx.trigger_typing()
        if not source and not ctx.message.attachments:
            await self.send_howto(ctx)
            return
        try:
            first,runoutput = await self.get_run_output(ctx)
            if first =="nooutput":
                embed = discord.Embed(color=discord.Colour.purple(),description="Your Code ran without giving any output")
                msg = await ctx.send(f"{ctx.author.mention}",embed = embed)
                self.run_IO_store[ctx.author.id] = RunIO(input=ctx.message, output=msg)
                return

            regex = r"/piston/jobs/?[A-Za-z0-9.-]+/?[A-Za-z0-9.-]+"
            a = re.findall(regex,runoutput)
            for i in a:
                runoutput = runoutput.replace(i,'inferno/coderunner/output.code')

            if first == "proper":
                embed = discord.Embed(title = "<a:coderunner:871630156471623741> Code Runner Output",color = discord.Colour.purple(),description = f"{runoutput}")
                msg = await ctx.send(f"{ctx.author.mention}",embed = embed)
            elif first == "error":
                embed = discord.Embed(title = "<a:coderunner:871630156471623741> Code Runner Output",color = discord.Colour.purple(),description = f"Your Code Gave Some Error Output\n{runoutput}")
                msg = await ctx.send(f"{ctx.author.mention}",embed = embed)
            elif first == "compile":
                embed = discord.Embed(title = "<a:coderunner:871630156471623741> Code Runner Output",color = discord.Colour.purple(),description = f"There were some Compilation Errors in your Code\n{runoutput}")
                msg = await ctx.send(f"{ctx.author.mention}",embed = embed)

        except commands.BadArgument as error:
            error = str(error)
            if not error =="Invalid command format File":
                if '\n' in error:
                    x = error.find('\n')
                    title = error[:x]
                    description = error[x+1:]
                else:
                    title = ""
                    description=error
                embed = discord.Embed(
                title=title,
                description=str(description),
                color=discord.Colour.purple()
            )
            else:
                embed = discord.Embed(title = "Invalid Format",color = discord.Colour.purple(),description="The correct way to use this command is :-")
                embed.set_image(url = "https://cdn.discordapp.com/attachments/862939982837317672/871386389869109248/krt90o5t59a.png")

            msg = await ctx.send(ctx.author.mention, embed=embed)
        self.run_IO_store[ctx.author.id] = RunIO(input=ctx.message, output=msg)

    @commands.command(hidden=True)
    async def edit_last_runcode(self, ctx, *, content=None):
        """Run some edited code and edit previous message"""
        # if self.client.maintenance_mode:
        #     return
        if (not content) or ctx.message.attachments:
            return
        try:
            msg_to_edit = self.run_IO_store[ctx.author.id].output
            first,runoutput = await self.get_run_output(ctx)
            if first =="nooutput":
                embed = discord.Embed(color=discord.Colour.purple(),description="Your Code ran without giving any output")
                await msg_to_edit.edit(content=f"{ctx.author.mention}",embed = embed)

                

            regex = r"/piston/jobs/?[A-Za-z0-9.-]+/?[A-Za-z0-9.-]+"
            a = re.findall(regex,runoutput)
            for i in a:
                runoutput = runoutput.replace(i,'inferno/coderunner/output.code')

            if first == "proper":
                embed = discord.Embed(title = "<a:coderunner:871630156471623741> Code Runner Output",color = discord.Colour.purple(),description = f"{runoutput}")
                await msg_to_edit.edit(content=f"{ctx.author.mention}",embed = embed)
            elif first == "error":
                embed = discord.Embed(title = "<a:coderunner:871630156471623741> Code Runner Output",color = discord.Colour.purple(),description = f"Your Code Gave Some Error Output\n{runoutput}")
                await msg_to_edit.edit(content=f"{ctx.author.mention}",embed = embed)
            elif first == "compile":
                embed = discord.Embed(title = "<a:coderunner:871630156471623741> Code Runner Output",color = discord.Colour.purple(),description = f"There were some Compilation Errors in your Code\n{runoutput}")
                await msg_to_edit.edit(content=f"{ctx.author.mention}",embed = embed)
            
            
        except KeyError:
            # Message no longer exists in output store
            # (can only happen if smartass user calls this command directly instead of editing)
            return
        except discord.NotFound:
            # Message no longer exists in discord
            if ctx.author.id in self.run_IO_store:
                del self.run_IO_store[ctx.author.id]
            return
        except commands.BadArgument as error:
            # Edited message probably has bad formatting -> replace previous message with error
            embed = discord.Embed(
                title='Error',
                description=str(error),
                color=discord.Colour.purple()
            )
            try:
                await msg_to_edit.edit(content=ctx.author.mention, embed=embed)
            except discord.NotFound:
                # Message no longer exists in discord
                del self.run_IO_store[ctx.author.id]
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # if self.client.maintenance_mode:
        #     return
        if after.author.bot:
            return
        if before.author.id not in self.run_IO_store:
            return
        if before.id != self.run_IO_store[before.author.id].input.id:
            return
        prefixes = ['>']
        if isinstance(prefixes, str):
            prefixes = [prefixes, ]
        if any(after.content in (f'>delete', f'>del') for prefix in prefixes):
            # await self.delete_last_output(after.author.id)
            return
        for prefix in prefixes:
            if after.content.lower().startswith(f'{prefix}runcode'):
                aftercopy = after
                aftercopy.content = aftercopy.content.replace(f'{prefix}runcode', f'>edit_last_runcode', 1)
                await self.client.process_commands(aftercopy)
                break
        return

    # @commands.Cog.listener()
    # async def on_message_delete(self, message):
    #     # if self.client.maintenance_mode:
    #     #     return
    #     if message.author.bot:
    #         return
    #     if message.author.id not in self.run_IO_store:
    #         return
    #     if message.id != self.run_IO_store[message.author.id].input.id:
    #         return
    #     await self.delete_last_output(message.author.id)

    @commands.command()
    async def coderunnerinfo(self, ctx):
        languages = sorted(set(self.languages.values()))

        run_instructions = (
            '**Here are my supported languages:**\n'
            + ', '.join(languages) +
            '\n\n**You can run code like this:**\n'
            '>runcode <language>\ncommand line parameters (optional) - 1 per line\n'
            '\\`\\`\\`\nyour code\n\\`\\`\\`\nstandard input (optional)\n\nJoin [Support Server](https://discord.gg/tTr6DvyRCH) for more info\n'
        )
        e = discord.Embed(title = "Code Runner Command Help",description=run_instructions,colour=discord.Colour.purple())
        await ctx.send(embed=e)
    @commands.command()
    async def howtoruncodebyfile(self,ctx):
        embed = discord.Embed(title="How to run code by file?",description='''Here is an example usage of how to run code by file
Add `>runcode [langauge]` as a comment while uploading file''',color= discord.Colour.purple())
        embed.set_image(url = "https://cdn.discordapp.com/attachments/862939982837317672/871386389869109248/krt90o5t59a.png")
        return await ctx.send(embed=embed)
    @commands.command()
    async def examplecoderun(self,ctx):
        embed = discord.Embed(title="How to run code by using CodeBlocks?",description='''Here is an example usage of how to run code by using codeblocks!''',color= discord.Colour.purple())
        embed.set_image(url = "https://media.discordapp.net/attachments/862939982837317672/871634630581821461/kru8973hi9a.png")
        return await ctx.send(embed=embed)        

async def setup(client):
    await client.add_cog(CodeRunner(client))