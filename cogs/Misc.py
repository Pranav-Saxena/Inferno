import discord
from discord.ext import commands,tasks
from discord.ext.commands.cooldowns import BucketType
import asyncio
import re
import motor.motor_asyncio
import nest_asyncio
import datetime
import os
import aiohttp
import wikipedia
nest_asyncio.apply()
cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb_cluster_auth")
reminder = cluster["reminder"]["reminder"]

#------math parser------------
grammar = """
?start: exponent
      | func
?func: NAME "(" [exponent|func] ")"	-> func
?exponent: sum
    | exponent "^" sum			-> exp
?sum: product
    | sum "+" product  			-> add
    | sum "-" product  			-> sub
    | sum "^" sum				-> exp

?product: atom
        | product "*" atom 		-> mul
        | product "/" atom 		-> div
        | product "^" atom		-> exp
?atom: NUMBER					-> number
     | "-" atom					-> neg
     | "(" sum ")"
NAME: "a".."z"+
DIGIT: "0".."9"
INT: DIGIT+
SIGNED_INT: ["+"|"-"] INT
DECIMAL: INT "." INT? | "." INT
_EXP: ("e"|"E") SIGNED_INT
FLOAT: INT _EXP | DECIMAL _EXP?
SIGNED_FLOAT: ["+"|"-"] FLOAT
NUMBER: FLOAT | INT
%import common.WS_INLINE
%ignore WS_INLINE
"""
from lark import Lark, Transformer, v_args
from functools import wraps


def size_limit(amount=((2 ** 32) - 1) / 2):
    def outer(func):
        @wraps(func)
        def inner(self, l, r=0):
            if l > amount or l < - amount:
                # print("Infinty")
                return "Infinity"

            if r > amount or r < - amount:
                # print("infinity")
                return "Infinity"

            return func(self, l, r)

        return inner

    return outer


import math as _math


@v_args(inline=True)
class CalculateTree(Transformer):
    _FUNCS = {
        x: getattr(_math, x)
        for x in dir(_math)
        if not x.startswith('_')
           and callable(getattr(_math, x))
    }
    number = float

    @size_limit()
    def add(self, l, r):
        return l + r

    @size_limit()
    def sub(self, l, r):
        return l - r

    @size_limit()
    def mul(self, l, r):
        return l * r

    @size_limit()
    def div(self, l, r):
        return l / r

    def neg(self, l, r=0):
        return -l

    @size_limit()
    def exp(self, l, r):
        return l ** r

    def func(self, name, arg):
        return self._FUNCS[name](arg)


#-------row 0 ------------------
class Brac1(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "(",row=0)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression=="Syntax Error":
            view.expression = '''('''
            view.actual = '''('''
        else:
            view.expression = view.expression + "("
            view.actual = view.actual + "("
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class Brac2(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = ")",row=0)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression=="Syntax Error":
            view.expression = ''')'''
            view.actual = ''')'''
        else:
            view.expression = view.expression + ")"
            view.actual = view.actual + ")"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class Perc(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "%",row=0)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression=="Syntax Error":
            view.expression = '''%'''
            view.actual = '''*0.01'''
        else:
            view.expression = view.expression + '''%'''
            view.actual = view.actual + '''*0.01'''
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class Backspace(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.blurple,label = "⌫",row=0)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression=="Syntax Error":
            view.expression = ''''''
            view.actual = ''''''
        else:
            view.expression = view.expression[:-1]
            view.actual = view.actual[:-1]
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)

class AC(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.danger,label = "AC",row=0)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        view.expression = ''''''
        view.actual = ''''''
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
#-----row 1-------------
class seven(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "7",row=1)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "7"
            view.actual = "7"
        else:
            view.expression = view.expression + "7"
            view.actual = view.actual + "7"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class eight(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "8",row=1)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression=="Syntax Error":
            view.expression = "8"
            view.actual = "8"
        else:
            view.expression = view.expression + "8"
            view.actual = view.actual + "8"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class nine(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "9",row=1)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "9"
            view.actual = "9"
        else:
            view.expression = view.expression + "9"
            view.actual = view.actual + "9"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class divide(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "÷",row=1)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "÷"
            view.actual = "/"
        else:
            view.expression = view.expression + "÷"
            view.actual = view.actual + "/"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class Power(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "xʸ",row=1)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "^"
            view.actual = "^"
        else:
            view.expression = view.expression + "^"
            view.actual = view.actual + "^"

        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)

#------------------------------row2-----------------------------------------------

class four(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "4",row=2)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "4"
            view.actual = "4"
        else:
            view.expression = view.expression + "4"
            view.actual = view.actual + "4"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class five(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "5",row=2)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "5"
            view.actual = "5"
        else:
            view.expression = view.expression + "5"
            view.actual = view.actual + "5"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class six(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "6",row=2)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "6"
            view.actual = "6"
        else:
            view.expression = view.expression + "6"
            view.actual = view.actual + "6"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class multiply(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "x",row=2)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "*"
            view.actual = "*"
        else:
            view.expression = view.expression + "*"
            view.actual = view.actual + "*"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class pi(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "π",row=2)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression=="Syntax Error":
            view.expression = "π"
            view.actual = "3.141592653589793"
        else:
            view.expression = view.expression + "π"
            view.actual = view.actual + "3.141592653589793"

        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)

#------------------------row 3----------------------------

class one(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "1",row=3)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "1"
            view.actual = "1"
        else:
            view.expression = view.expression + "1"
            view.actual = view.actual + "1"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class two(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "2",row=3)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "2"
            view.actual = "2"
        else:
            view.expression = view.expression + "2"
            view.actual = view.actual + "2"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class three(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "3",row=3)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "3"
            view.actual = "3"
        else:
            view.expression = view.expression + "3"
            view.actual = view.actual + "3"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class sub(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "-",row=3)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "-"
            view.actual = "-"
        else:
            view.expression = view.expression + "-"
            view.actual = view.actual + "-"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class e(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "e",row=3)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression=="Syntax Error":
            view.expression = "e"
            view.actual = "2.718281828459045"
        else:
            view.expression = view.expression + "e"
            view.actual = view.actual + "2.718281828459045"

        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
#-------------------row4-----------------
class zero(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "0",row=4)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "0"
            view.actual = "0"
        else:
            view.expression = view.expression + "0"
            view.actual = view.actual + "0"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class deci(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = ".",row=4)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "."
            view.actual = "."
        else:
            view.expression = view.expression + "."
            view.actual = view.actual + "."
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)
class equal(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.success,label = "=",row=4)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        try:
            calc_parser =  Lark(grammar, parser='lalr', transformer=CalculateTree())
            calc = calc_parser.parse
            evalvalue = calc(view.actual)
            view.expression = str(evalvalue)
            view.actual=str(evalvalue)
        except:
            view.expression= "Syntax Error"
            view.actual=""
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)

class add(discord.ui.Button['Calculator']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.secondary,label = "+",row=4)
        self.ctx = ctx
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Calculator = self.view
        if interaction.user != self.ctx.author:
            return
        if view.expression == "Syntax Error":
            view.expression = "+"
            view.actual = "+"
        else:
            view.expression = view.expression + "+"
            view.actual = view.actual + "+"
        embed = discord.Embed(colour=discord.Colour.purple(),title= "Calculator",description=f'''```
{view.expression}{(40-len(view.expression))*" "}
```''')
        await interaction.response.edit_message(embed = embed, view=view)

class CalcExit(discord.ui.Button['TicTacToe']):
    def __init__(self,ctx):
        super().__init__(style = discord.ButtonStyle.danger,label = "Exit",row=4)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        if interaction.user != self.ctx.author:
            return
        view.stop()
class Calculator(discord.ui.View):
    def __init__(self,ctx):
        super().__init__()
        self.ctx = ctx
        self.expression = ''''''
        self.actual = ''''''
        self.add_item(Brac1(self.ctx))
        self.add_item(Brac2(self.ctx))
        self.add_item(Perc(self.ctx))
        self.add_item(Backspace(self.ctx))
        self.add_item(AC(self.ctx))
        self.add_item(seven(self.ctx))
        self.add_item(eight(self.ctx))
        self.add_item(nine(self.ctx))
        self.add_item(divide(self.ctx))
        self.add_item(Power(self.ctx))
        self.add_item(four(self.ctx))
        self.add_item(five(self.ctx))
        self.add_item(six(self.ctx))
        self.add_item(multiply(self.ctx))
        self.add_item(pi(self.ctx))
        self.add_item(one(self.ctx))
        self.add_item(two(self.ctx))
        self.add_item(three(self.ctx))
        self.add_item(sub(self.ctx))
        self.add_item(e(self.ctx))
        self.add_item(zero(self.ctx))
        self.add_item(deci(self.ctx))
        self.add_item(equal(self.ctx))
        self.add_item(add(self.ctx))
        self.add_item(CalcExit(self.ctx))

class Misc(commands.Cog):
    def __init__(self,client):
        self.client=client
        self.checker.start()

    @commands.command(aliases=["quickpoll"],description="Creates a poll (Max 10 options allowed)",brief = ">poll \"Yes/No\" \"Yes\" \"No\"")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def poll(self,ctx,*,text=None):

        if text is not None:
            m= re.findall(r"\"([^\"]+)\"", text)
      
        d = {1:"\u0031\ufe0f\u20e3",2:"\u0032\ufe0f\u20e3",3:"\u0033\ufe0f\u20e3",4:"\u0034\ufe0f\u20e3",5:"\u0035\ufe0f\u20e3",6:"\u0036\ufe0f\u20e3",7:"\u0037\ufe0f\u20e3",8:"\u0038\ufe0f\u20e3",9:"\u0039\ufe0f\u20e3"}

        if text is None:
        
            desc = '''\n\u0031\ufe0f\u20e3 Yes\n\u0032\ufe0f\u20e3 No'''
      
            embed = discord.Embed(title = "Yes/No",colour=discord.Colour.purple(),description = desc)
            msg = await ctx.send(embed=embed)
            
            await msg.add_reaction('\u0031\ufe0f\u20e3')
            await msg.add_reaction('\u0032\ufe0f\u20e3')
            return
        elif len(m)==1:

            embed = discord.Embed(colour = discord.Colour.purple(),description = "<a:infernocross:844577707727388742> You need to enter at least one option")
            await ctx.send(embed=embed)
            return
        elif len(m)>11:
            embed = discord.Embed(colour=discord.Colour.purple(),description="<a:infernocross:844577707727388742> Limit the no. of options/choices to 10")
            await ctx.send(embed=embed)
            return
        elif len(m)>1 and len(m)<=11:
            title = m[0]
      
            if len(m)==11:
                options = m[:-1]
                option10 = m[10]
                desc =""
                for i in range(9):
                    desc = desc + d[i+1] + f" {options[i]}\n"
                desc = desc + f"\U0001f51f {options10}"

                embed = discord.Embed(title = title,colour=discord.Colour.purple(),description = desc)
                
                msg = await ctx.send(embed=embed)
        
                for i in range(9):
                    await msg.add_reaction(d[i+1])
                await msg.add_reaction("\U0001f51f")
                return
            else:
                options = m[1:]
                desc = ""

                for i in range(len(m[1:])):
                    desc = desc + d[i+1] + f" {options[i]}\n"
          
                embed = discord.Embed(title = title,colour=discord.Colour.purple(),description = desc)
                msg = await ctx.send(embed=embed)
                        
                for i in range(len(m[1:])):
                    await msg.add_reaction(d[i+1])
                return
    @commands.command(aliases=["calci","calculator","Calculator","Calc","Calci"],description="A Simple Interactive Calculator")
    async def calc(self,ctx: commands.Context):
        embed = discord.Embed(title = "Calculator",colour=discord.Colour.purple(),description=f'''```
{40*" "}
```''')
        await ctx.send(embed=embed,view = Calculator(ctx))

#----------------------------reminder--------------------\
    @commands.command(cooldown_after_parsing=True, aliases=["notify", "reminder","Reminder","Remind"],description= "Creates a reminder")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def remind(self, ctx: commands.Context, time, *, description: str):
        desc = description
        ttime = time
        try:

            if len(desc) < 101:
                typ = ttime[-1]
                dur = ttime
                choices = ["s", "m", "h", "d"]
                if typ not in choices:
                    embed=discord.Embed(description="Duration should be only in **s(seconds), m(minutes),h(hours),d(days)**\n Sample Usage - `>remind 10s test`",colour=discord.Colour.purple())
                    await ctx.send(embed=embed)
                else:
                    ttime = int(ttime[0:-1])
                    if typ == "s":
                        conv = ttime
                    elif typ == "m":
                        conv = ttime * 60
                    elif typ == "h":
                        conv = ttime * 3600
                    elif typ == "d":
                        conv = ttime * 86400

                    if conv > 604800:
                        embed = discord.Embed(colour=discord.Colour.purple(),description="<a:infernocross:844577707727388742> Reminder duration should not be more than 7 days")
                        await ctx.send(embed= embed)
                    else:
                        embed = discord.Embed(title = "Reminder Set",colour=discord.Colour.purple(),description =f'''
I'll remind you in 
```css
{dur}
```
For
```yaml
{desc}
```
''' )
                        await ctx.send(embed=embed)
                        tstamp = datetime.datetime.utcnow()
                        a = datetime.datetime.now()
                        a = a + datetime.timedelta(seconds=conv)
                        newuser = {
                            "id": ctx.author.mention,
                            "Time": a,
                            "Desc": desc,
                            "Channel": ctx.channel.id,
                            "tstamp" : tstamp
                        }
                        await reminder.insert_one(newuser)

            else:
                embed= discord.Embed(colour=discord.Colour.purple(),description="<a:infernocross:844577707727388742> Limit the Reminder description to 100 characters")
                # embed.set_author(name = "<a:infernocross:844577707727388742> Limit the Reminder description to 100 characters")
                await ctx.send(embed=embed)
        except ValueError:
            pass
        return
    @tasks.loop(seconds=10)
    async def checker(self):
        try:
            all = reminder.find({})
            current = datetime.datetime.now()
            async for x in all:
                if current >= x["Time"]:
                    channel_only = self.client.get_channel(x["Channel"])
                    
                    desc = x["Desc"]
                    person = x["id"]
                    tmestamp = x["tstamp"]
                    embed = discord.Embed(colour=discord.Colour.purple(),description=f'''
**Reminder **
```yaml
{desc}
```
''',timestamp=tmestamp)
                    embed.set_footer(text = "Reminder Created on")
                    try:
                        await channel_only.send(f"Here's your reminder {person}",embed=embed)
                    except Exception:
                        pass
                    await reminder.delete_one(x)
                else:
                    pass
        except Exception as e:
            
            pass
    @commands.command(aliases=["pip"],description = "Searches for Package on pypi.org")
    async def pypi(self, ctx, package_name=None):
        if package_name is None:
            await ctx.send("**Missing package name**")
        else:
            if len(package_name) >= 40:
                await ctx.send("**❌ Big package name **")
            else:
                url = f"https://pypi.org/pypi/{package_name}/json"
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(url) as res:
                        if res.status == 404:
                            await ctx.send("**No such package found**")
                        else:
                            r = await res.json()
                            author = r["info"]["author"]
                            desc = r["info"]["description"]
                            if len(desc) > 500:
                                d = desc[:500]
                                desc = f"{d}..."
                            else:
                                pass
                            home = r["info"]["home_page"]
                            name = r["info"]["name"]
                            summary = r["info"]["summary"]
                            if len(summary) > 100:
                                sum = summary[:100]
                                summary = f"{sum}..."
                            else:
                                pass
                            
                            desc = desc.replace("#", " ")
                            if desc == "":
                                desc = "None"
                            project = r["info"]["project_url"]
                            v = r["info"]["version"]

                            embed = discord.Embed(color=0xFF0000)
                            try:
                                embed.add_field(name="Name", value=f"{name}", inline=True)
                            except:
                                pass

                            try:
                                embed.add_field(name="Version", value=f"{v}", inline=True)
                            except:
                                pass

                            try:
                                embed.add_field(name="Author", value=f"{author}", inline=True)
                            except:
                                pass

                            try:
                                embed.add_field(
                                name="Summary", value=f"{summary}", inline=False
                            )
                            except:
                                pass
                                
                            try:
                                embed.add_field(
                                name="\n**Description**", value=f"{desc}", inline=False
                            )
                            except :
                                pass
                            try:
                                embed.add_field(
                                name="**Links**",
                                value=f"[Home Page]({home}) \n [Page]({project})",
                                inline=False,
                            )
                            except:
                                pass
                            embed.set_thumbnail(
                                url="https://miro.medium.com/max/1080/1*ciPCmwyO6C79SLVU5Rj50w.jpeg"
                            )

                            await ctx.send(embed=embed)
        return
    @commands.command(
        cooldown_after_parsing=True, description="Shows wikipedia summary"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def wiki(self, ctx, *, msg):
        try:
            content = wikipedia.summary(msg, auto_suggest=True, redirect=True)

            embed = discord.Embed(title="Wikipedia", color=discord.Colour.purple())
            chunks = [content[i : i + 1024] for i in range(0, len(content), 2000)]
            for chunk in chunks:
                embed.add_field(name="\u200b", value=chunk, inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send("**Failed to get information**")
        return

    @commands.command(
        cooldown_after_parsing=True,
        description="Searches the wikipedia for the message entered",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wikisearch(self, ctx, *, msg):
        try:

            content = wikipedia.search(msg, results=5, suggestion=True)
            content = content[0]
            embed = discord.Embed(title="Search Results", color=discord.Colour.purple())
            z = 1
            for i in content:
                embed.add_field(name="\u200b", value=f"{z}-{i}", inline=False)
                z += 1

            await ctx.send(embed=embed)
        except:
            await ctx.send("**Failed to get information**")
        return

    @commands.command(
        aliases=["ip"], description="Shows the info about the given ip/webiste"
    )
    async def ipinfo(self, ctx, ip_address):
        if ip_address == None:
            await ctx.send("You forgot to mention the ip address")
        else:
            # ip_address = int(ip_address)
            URL = f"http://ip-api.com/json/{ip_address}?fields=17000447"

            async def check_valid_status_code(request):
                if request.status == 200:
                    return await request.json()

                return False

            async def get_info():
                async with aiohttp.ClientSession() as session:
                    async with session.get(URL) as resp:
            
                        data = await check_valid_status_code(resp)

                        return data

            infoip = await get_info()
            check = infoip["status"]
            if not infoip or check == "fail":
                await ctx.channel.send("Couldn't get the IP info at the moment. Try again later.")

            else:
                embed = discord.Embed(
                    timestamp=ctx.message.created_at,
                    title="IP Information",
                    color=discord.Colour.purple()
                )
                embed.add_field(name="Status", value=infoip["status"])
                embed.add_field(name="IP ADDRESS", value=infoip["query"])
                embed.add_field(name="Country Code", value=infoip["countryCode"])
                embed.add_field(name="Country Name", value=infoip["country"])
                embed.add_field(name="Region Code", value=infoip["region"])
                embed.add_field(name="Region Name", value=infoip["regionName"])
                embed.add_field(name="City", value=infoip["city"])
                embed.add_field(name="Zip Code", value=infoip["zip"])
                embed.add_field(name="Time Zone", value=infoip["timezone"])
                embed.add_field(name="Latitude", value=infoip["lat"])
                embed.add_field(name="Longitude", value=infoip["lon"])
                embed.add_field(name="ISP", value=infoip["isp"])
                embed.add_field(name="ORG", value=infoip["org"])
                embed.add_field(name="Mobile", value=infoip["mobile"])
                embed.add_field(name="Hosting", value=infoip["hosting"])
                embed.add_field(name="Proxy", value=infoip["proxy"])
                embed.set_footer(
                    text=f"Requested By: {ctx.author.name}",
                    icon_url=f"{ctx.author.avatar.url}",
                )
                await ctx.send(embed=embed)
        return

async def setup(client):
  await client.add_cog(Misc(client))