import aiohttp
import discord
from discord.ext import commands
from PIL import ImageFont, ImageDraw, Image
from io import BytesIO
import os
def make_RGBA(im):
    if im.mode == 'RGBA':
        return im
    im = im.convert('RGBA')
    im.putalpha(255)
    return im

def mask_circle(im):
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)
    return im


async def make_avatar(user):
    asset = user.display_avatar.with_static_format('png')
    data = BytesIO(await asset.read())
    im = Image.open(data)
    # avatar = im.copy()
    # avatar = make_RGBA(avatar)
    im = make_RGBA(im)
    return im


def resize_avatar(avatar, size, rot=0, make_circle=True):
    new_avatar = avatar.copy()
    new_avatar = new_avatar.rotate(rot)
    if size != new_avatar.size:
        new_avatar = new_avatar.resize(size)
    if make_circle:
        new_avatar = mask_circle(new_avatar)
    return new_avatar

class ownerlogs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener("on_guild_join")
    async def joing(self, guild):
        l=[]
        x=guild.members
        for i in x:
            if i.bot:
                l.append(i)
        embed = discord.Embed(title = "Joined Server",colour=discord.Colour.purple(),description=f'''
**Guild Name** - {guild.name}
**Guild Id** - {guild.id}
**Guild Owner** - {guild.owner.mention}

**Members** - {len(guild.members) - len(l)}
**Bots** - {len(l)}
**Total Members** - {len(guild.members)}
''')
        await self.client.get_channel(849628636809920512).send(embed=embed)
        return   
            
    @commands.Cog.listener("on_guild_remove")
    async def leftg(self, guild):
        l=[]
        x=guild.members
        for i in x:
            if i.bot:
                l.append(i)
        embed = discord.Embed(title = "Server Left",colour=discord.Colour.purple(),description=f'''
**Guild Name** - {guild.name}
**Guild Id** - {guild.id}
**Guild Owner** - {guild.owner.mention}

**Members** - {len(guild.members) - len(l)}
**Bots** - {len(l)}
**Total Members** - {len(guild.members)}
''')
        await self.client.get_channel(849628636809920512).send(embed=embed)   
        return    

    @commands.Cog.listener("on_member_join")
    async def omjic(self,member):
        '''
        the guild_ids are me or my friend's personal servers, for which I had changed some stuffs'''
        if member.guild.id not in [guild_id1,guild_id2,guild_id3]: 
            return
        if member.guild.id == guild_id4:
        
            role = member.guild.get_role(849495386548338688)
            await member.add_roles(role)
            #welcome image
            im = Image.open('/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/bgwelcomeinfernocom.png')
            im = im.convert('RGBA')
            im.putalpha(255)
            avatar = await make_avatar(member)
            sized_avatar = resize_avatar(avatar, (197,197), rot=0)
            im.alpha_composite(sized_avatar,dest=(56,49))
            im.save("/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/tempwelcome.png")
            fnt = ImageFont.truetype("/home/pranav/Inferno/Inferno/roboto.TTF", 46)
            img = Image.open("/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/tempwelcome.png")
            d = ImageDraw.Draw(img)
            d.multiline_text((300, 124), f"{member.name}#{member.discriminator}", font=fnt, fill=(0, 128, 128))
            img.save('/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/welcome.png')
            await self.client.get_channel(850009521560879106).send(f"Welcome {member.mention} to Inferno Community, the official support server of Inferno.\nHope you'll have a great experience here.",file=discord.File('/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/welcome.png'))
            os.remove('/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/welcome.png')
            return

        if member.guild.id == guild_id5:
            dict= {"0":"th","1":"st","2":"nd","3":"rd","4":"th","5":"th","6":"th","7":"th","8":"th","9":"th"}
            im = Image.open('/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/bgwelcomeinfernocom.png')
            im = im.convert('RGBA')
            im.putalpha(255)
            avatar = await make_avatar(member)
            sized_avatar = resize_avatar(avatar, (197,197), rot=0)
            im.alpha_composite(sized_avatar,dest=(56,49))
            im.save("/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/tempwelcomefurious.png")
            fnt = ImageFont.truetype("/home/pranav/Inferno/Inferno/roboto.TTF", 46)
            img = Image.open("/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/tempwelcomefurious.png")
            d = ImageDraw.Draw(img)
            d.multiline_text((300, 124), f"{member.name}#{member.discriminator}", font=fnt, fill=(0, 128, 128))
            img.save('/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/welcomefurious.png')
            x=member.guild.members
            l=[]
            for i in x:
                if i.bot:
                    l.append(i)
            memcount = len(member.guild.members) - len(l)
            if str(memcount)[-2:] in ["11","12","13"]:
                suffix = "th"
            else:
                suffix = dict[str(memcount)[-1]]
            await self.client.get_channel(859300058875953152).send(f"Welcome {member.mention} to **Furious Gaming**. You are the **{memcount}{suffix}** user!",file=discord.File('/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/welcomefurious.png'))
            os.remove('/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/welcomefurious.png')
            return
        

    @commands.Cog.listener("on_member_remove")
    async def omric(self,member):
        if member.guild.id not in [guild_id1,guild_id2]:
            return        
        if member.guild.id == guild_id3:
            await self.client.get_channel(850009945788645427).send(f"{member.mention} ({member.name}#{member.discriminator}) left the server :pensive:")   
            return   
        elif member.guild.id == guild_id4:
            await self.client.get_channel(775304570439991307).send(f"{member.mention} ({member.name}#{member.discriminator}) left the server :pensive:")   
            return    
   
async def setup(client):  # Cog setup command
    await client.add_cog(ownerlogs(client))