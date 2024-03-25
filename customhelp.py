import discord 
from discord.ext import commands
import os 
import requests
import aiohttp
embed0=discord.Embed(title="Help",colour=discord.Colour.purple(),description='''
```asciidoc
Prefix :: >
Total Commands :: 123 commands
```''')
embed0.add_field(name="<:cti:860805450455056385>Code To Image",value="`>help cti`")
embed0.add_field(name="<a:coderunner:871630156471623741> Code Runner",value="`>help coderunner`")
embed0.add_field(name=":joy:Fun",value="`>help Fun`")
embed0.add_field(name="<:games:847836492449841152>Games",value="`>help Games`")
# embed0.add_field(name="<:stream:857114055478476810>Stream/\nDiscord Together",value="`>help stream`")
embed0.add_field(name="<:image:847839209732964363>Image",value="`>help Image`")
embed0.add_field(name="<:info:847837030636978226>Info",value="`>help Info`")
embed0.add_field(name="<:mod:847837349004967957>Mod",value="`>help Mod`")
embed0.add_field(name="<:manager:861890539989368883>Manager",value="`>help Manager`")
embed0.add_field(name="<:logs:861891714402353162>Logging",value="`>help Logging`")
embed0.add_field(name="<:utilities:847841200731717632>Utility",value="`>help Utility`")
embed0.add_field(name="<:rr:856744950041542678> Reaction Roles",value="`>help rr`")
embed0.add_field(name="<a:wavehand:849510257914282005> Welcome",value="`>help welcome`")
embed0.add_field(name="<:misc:847846836902428672>Misc",value="`>help Misc`")
embed0.add_field(name="\u202b",value="\u202b")
# embed0.set_footer(text='''Type >help command for more info on a command.
# You can also type >help category for more info on a category.''')
embed0.set_footer(text='''Type >help command for more info on a command.
You can also type >help category for more info on a category.''')

embed1=discord.Embed(title="<:cti:860805450455056385>Code To Image",colour=discord.Colour.purple())
embed1.set_image(url="https://cdn.discordapp.com/attachments/848425307333459989/848425321296298014/unknown.png")
embed1.set_footer(text = "Use >enable CTI or >disable CTI to toggle the event" )


embed2=discord.Embed(title=":joy:Fun",description='''Commands to make you enjoy!!
```
8ball | meme | avatar | say | snipe | editsnipe | bored | lenny | cat | dog | panda | fox | bird
```
**PREFIX**
```yaml
>
```
''',colour=discord.Colour.purple())
embed2.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')
embed3=discord.Embed(title="<:games:847836492449841152>Games",description='''Feeling Bored? Try some Game commands mentioned down below!!
```
hangman | tictactoe | guess | ticbuttons
```
**PREFIX**
```yaml
>
```
**NEW FEATURE**
```md
#Tic-Tac-Toe-Buttons - The experience of playing TicTacToe is now even better. You can now play the game by clicking on buttons just like you play on a real game app!!. Type >help ticbuttons to know more
```

''',colour=discord.Colour.purple())
embed3.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')
embed4 = discord.Embed(title="<:image:847839209732964363>Image",description='''Creates Image using your avatar
```
Thor | Captainamerica | DrStrange | Hulk | IronMan | SpiderMan | Thanos 
Slap | Triggered
```
**PREFIX**
```yaml
>
```
''',colour=discord.Colour.purple())
embed4.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')
embed5 = discord.Embed(title="<:info:847837030636978226>Info",description='''Commands related to Information
```
botinfo | invite | support | vote | ping | about | suggest | serverinfo | userinfo | members
```
**PREFIX**
```yaml
>
```
''',colour=discord.Colour.purple())
embed5.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')

embed6 = discord.Embed(title="<:mod:847837349004967957>Mod",description = '''Commands to help you manage your server(can be used by Mods and Admins only)
```yaml
clear | kick | ban | unban | softban | mute | unmute | tempmute | block | unblock | addrole | unrole | chnick | resetnick | lock | unlock | 
warn | warnings | modcase | clearwarns | delwarn | delmodcase | modhistory
```
**PREFIX**
```yaml
>
```
''',colour = discord.Colour.purple())
embed6.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')
embed7=discord.Embed(title = "<:utilities:847841200731717632>Utility",description = '''Commands to help you!!
```
hastebin | raw | qrcode | notepad
```
**PREFIX**
```yaml
>
```
**NEW FEATURE**
```md
#Notepad - Create, Edit, View or Remove Note(s) from your Notepad!. There are 4 sub-commands , [add,view,remove,edit]. Start creating a new note by typing >notes add <notename> <note> !! 
```

''',colour=discord.Colour.purple())
embed7.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')
embed8 = discord.Embed(title="<:misc:847846836902428672>Misc",description = '''Miscellaneous Commands
```
poll | calculator | remind | pypi | wiki | wikisearch | ipinfo
```
**PREFIX**
```yaml
>
```
**NEW FEATURE**
```md
#Calculator - Solve your Math problems with this newly added Interactive Calculator . Type >calc to use it.

#Reminder - Creates a reminder for you.
```
''',colour = discord.Colour.purple())
embed8.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')

embed9 = discord.Embed(title="<:rr:856744950041542678> Reaction Roles",description = '''
```elm
rrcreate - starts the creation of reaction roles
rrupdate - delete or add reaction roles in a message. 
rrdelete - removes all reaction roles from the message 
rrinfo - gives info regarding reaction roles setup on a message   
rrlist - gives info of all the messages having reaction roles setup in the server   
```
**PREFIX**
```yaml
>
```
''',colour = discord.Colour.purple())
embed9.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')

embed10 = discord.Embed(title="<:stream:857114055478476810> Stream / Discord Together",description = '''
Watch Youtube Videos together in VC with a new UI. also you can play games (chess,fishington,)

Commands Usage :- `>[commandname] [mention a voice channel]`

To get help how to mention a voice channel, join my support server [Support Server](https://discord.gg/tTr6DvyRCH)

```elm
ytstream - Watch youtube with your friends in vc with an interactive ui
pokernight - play pokernight with your friends in vc with an interactive ui
betrayal -  play betrayal.io in vc with an interactive ui
chess - play chess in vc with an interactive ui    
fishington - play fishington.io in vc with an interactive ui
```
**PREFIX**
```yaml
>
```
''',colour = discord.Colour.purple())
embed10.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')
embed11 = discord.Embed(title="<:logs:861891714402353162> Logging",description = '''
Keep a track of the acitivities in your server with an advanced Logging System.
Type `>setlogs` to begin
You can type `>tellmeaboutlogs` to get info about what all types of logs you can setup.

```yaml
setlogs | showlogs | updatelogs | dellogs | 
updatemodlogschannel | updatemsglogschannel | updatememlogschannel | updatememjoinlogschannel | updateinvlogschannel 
```
**PREFIX**
```yaml
>
```
''',colour = discord.Colour.purple())
embed11.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')

embed12 = discord.Embed(title="<:manager:861890539989368883> Manager",description = '''
Commands to help you manage your server

```yaml
createrole | delrole | changerolecolour | addemoji | delemoji | disable_slowmode | enable_slowmode | delete_channel | clean_channel |
autorole | autoroleupdate | deleteautorole | botautorole | botautoroleupdate | deletebotautorole 
```
**PREFIX**
```yaml
>
```
''',colour = discord.Colour.purple())
embed12.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')

embed13 = discord.Embed(title="<a:coderunner:871630156471623741> Code Runner",description = '''
Executes your code and returns the Output!

**Commands**
```yaml
runcode | coderunnerinfo | howtoruncodebyfile | examplecoderun
```
**PREFIX**
```yaml
>
```
**Supported Languages**
```
awk, brainfuck, c, c++, cjam, clojure, cobol, coffeescript, cow, crystal, d, dart, dash, dotnet, dragon, elixir, emacs, erlang, fortran, go, golfscript, groovy, haskell, java, javascript, jelly, julia, kotlin, lisp, lolcode, lua, mono, nasm, nasm64, nim, ocaml, octave, osabie, paradoc, pascal, perl, php, ponylang, prolog, pure, pyth, python, python2, raku, rockstar, ruby, rust, scala, swift, typescript, vlang, yeethon, zig
```
**Syntax**
>runcode <language>
command line parameters (optional) - 1 per line
\`\`\`
your code
\`\`\`
standard input (optional) [each required input should be in different line]

```yaml
If you correct the code by editing your original message, bot will also edit its message and show the correct code

Also you can use a file to run code . type `>help howtoruncodebyfile` to know more
```

''',colour = discord.Colour.purple())
embed13.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')

embed14 = discord.Embed(title="<a:wavehand:849510257914282005> Welcome",description = '''
Setup / Disable a **Fully Customizable** welcome system in your server.

**Available Customizations**
```yaml
Custom Background Image
Custom Font Colour
Custom Text Inside Welcome Image(except in preset4)
```
**Commands**
```yaml
showwelcomepresets | setwelcometext | setwelcomeimage | setfarewelltext | delwelcome | delwelcometext | delwelcomeimage | delfarewelltext
```
**PREFIX**
```yaml
>
```
''',colour = discord.Colour.purple())
embed14.set_footer(text='''Type >help command for more info on a command.
Don't forget to use the prefix''')

class MyHelp(commands.HelpCommand):
   # !help
    async def send_bot_help(self, mapping):
      url = f"https://discord.com/api/channels/{self.context.channel.id}/messages"
    # embed = discord.Embed(title = "Title")
      button1 = discord.ui.Button(label="INVITE ME",style = discord.ButtonStyle.link,url = "https://discord.com/api/oauth2/authorize?client_id=808690602358079508&permissions=261926419703&scope=bot%20applications.commands",emoji = "<:invite:848985576731312128>")
      button2 = discord.ui.Button(label="SUPPORT SERVER",style = discord.ButtonStyle.link,url = "https://discord.gg/tTr6DvyRCH",emoji = "<:support:849646432138559488>")     
 
      view = discord.ui.View()
      view.add_item(button1)
      view.add_item(button2)
      await self.context.send(embed=embed0, view=view)
      return
      
        
   # !help <command>
    async def send_command_help(self, command):
        # await self.context.send("This is help command")
        cgs = {"fun":"Fun","games":"Games","image":"Image","info":"Info","mod":"Mod","utility":"Utility","misc":"Misc","cti":"Events","rr":"rr","logging":"Logging","manager":"Manager","coderunner":"CodeRunner","welcome":"Welcome"}
        
        if command.name.lower() in cgs:
          await self.send_cog_help(self.context.bot.get_cog(cgs[command.name.lower()]))
          return
        if command.name == "poll":
          embed = discord.Embed(title=command.name,description=command.description,colour=discord.Colour.purple())
          if len(command.aliases)==0:
            embed.add_field(name="Aliases",value="None")
          else:
            embed.add_field(name="Aliases",value=f"`{', '.join(command.aliases)}`")
          embed.add_field(name="Usage",value = f"`>{command.name.lower()} \"title\" \"option1\" ....`",inline=False)
          await self.context.send(embed=embed) 
          return
        embed = discord.Embed(title=command.name,description=command.description,colour=discord.Colour.purple())
       
        if len(command.aliases)==0:
          embed.add_field(name="Aliases",value="None")
        else:
          embed.add_field(name="Aliases",value=f"`{', '.join(command.aliases)}`")
        embed.add_field(name="Usage",value = f"`>{command.name.lower()} {command.signature}`",inline=False)
        embed.set_footer(text="< > means required and [ ] means optional (You don't need to use the brackets with the cmd)")
        await self.context.send(embed=embed) 
      
   # !help <group>
    async def send_group_help(self, group):
        embed = discord.Embed(title=group.qualified_name.title(),colour=discord.Colour.purple())
        embed.add_field(name="Description",value = group.description)
        embed.add_field(name="Aliases",value= f"{', '.join(group.aliases)}")
        subcmds = ""
        for i in group.commands:
          subcmds = subcmds + str(i.name)+", "
        subcmds = subcmds[:-2]
          
        embed.add_field(name = "Sub-Commands",value = subcmds)
        embed.add_field(name = "Cooldown",value  =group.extras['cooldown'])
        embed.add_field(name = "Usage",value = f"`>{group.qualified_name} [{subcmds}]`")
        embed.set_footer(text = f"You can type >help {group.qualified_name} [{subcmds}] to get more info on a sub-command.\nAlso you can type >{group.qualified_name} to get to know about Sample Usage of this command!")
        await self.context.send(embed = embed)
    
   # !help <cog>
    async def send_cog_help(self, cog):
        
        if str(cog.qualified_name) == "Fun":
          await self.context.send(embed = embed2)
        elif str(cog.qualified_name) == "Games":
          await self.context.send(embed = embed3)
        elif str(cog.qualified_name) == "Image":
          await self.context.send(embed = embed4)
        elif str(cog.qualified_name) == "Info":
          await self.context.send(embed = embed5)
        elif str(cog.qualified_name) == "Mod":
          await self.context.send(embed=embed6)
        elif str(cog.qualified_name) == "Utility":
          await self.context.send(embed = embed7)
        elif str(cog.qualified_name) == "Misc":
          await self.context.send(embed=embed8)
        elif str(cog.qualified_name) == "Events":
          await self.context.send(embed=embed1)
        elif str(cog.qualified_name)=="rr":
          await self.context.send(embed = embed9)
        # elif str(cog.qualified_name)=="discordtogether":
        #   await self.context.send(embed = embed10)
        elif str(cog.qualified_name)=="Logging":
          await self.context.send(embed = embed11)
        elif str(cog.qualified_name)=="Manager":
          await self.context.send(embed = embed12)
        elif str(cog.qualified_name)=="CodeRunner":
          await self.context.send(embed = embed13)
        elif str(cog.qualified_name)=="Welcome":
          await self.context.send(embed = embed14)
        else:
          await self.context.send(f"No command called \"{cog.qualified_name}\" found.")
        return
