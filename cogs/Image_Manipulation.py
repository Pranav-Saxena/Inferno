from PIL import Image, ImageFilter,ImageDraw
from io import BytesIO
import discord
from discord.ext import commands
import requests
import os
from os import getenv

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

class Image_Manipulation(commands.Cog, name="Image"):
  def __init__(self,client):
    self.client=client
  @commands.command(aliases=["IronMan","Ironman","IRONMAN"],description = "Creates an Iron Man image using the user's avatar")
  async def ironman(self,ctx,user : discord.Member=None):
    if not user:
      user=ctx.author
    im = Image.open('/home/pranav/Inferno/Inferno/cogs/Images/Iron Man/iron man.jpg')
    im = im.convert('RGBA')
    im.putalpha(255)

    avatar = await make_avatar(user)

    sized_avatar = resize_avatar(avatar, (335,345), rot=0)

    im.alpha_composite(sized_avatar,dest=(620,263))

    im.save('/home/pranav/Inferno/Inferno/cogs/Images/Iron Man/ironmanout.png')
    await ctx.send(file=discord.File('/home/pranav/Inferno/Inferno/cogs/Images/Iron Man/ironmanout.png'))
    os.remove('/home/pranav/Inferno/Inferno/cogs/Images/Iron Man/ironmanout.png')
    return


  @commands.command(aliases=["thor","THOR"],description = "Creates a Thor image using the user's avatar")
  async def Thor(self,ctx,user : discord.Member=None):
    if not user:
      user=ctx.author

    im = Image.open('/home/pranav/Inferno/Inferno/cogs/Images/Thor/thor 3.jpg')
    im = im.convert('RGBA')
    im.putalpha(255)

  
    avatar = await make_avatar(user)
    sized_avatar = resize_avatar(avatar, (114,114), rot=0)
    im.alpha_composite(sized_avatar,dest=(343,41))

    im.save('/home/pranav/Inferno/Inferno/cogs/Images/Thor/thorout.png')
    await ctx.send(file=discord.File('/home/pranav/Inferno/Inferno/cogs/Images/Thor/thorout.png'))
    os.remove('/home/pranav/Inferno/Inferno/cogs/Images/Thor/thorout.png')
    return
  @commands.command(aliases=["Thanos","THANOS"],description = "Creates a Thanos image using the user's avatar")
  async def thanos(self,ctx,user : discord.Member=None):
    if not user:
      user=ctx.author
    im = Image.open('/home/pranav/Inferno/Inferno/cogs/Images/Thanos/thanos.jpg')
    im = im.convert('RGBA')
    im.putalpha(255)
    avatar = await make_avatar(user)
    sized_avatar = resize_avatar(avatar, (132,127), rot=0)
    im.alpha_composite(sized_avatar,dest=(221,55))
    im.save('/home/pranav/Inferno/Inferno/cogs/Images/Thanos/thanosout.png')
    await ctx.send(file=discord.File('/home/pranav/Inferno/Inferno/cogs/Images/Thanos/thanosout.png'))
    os.remove('/home/pranav/Inferno/Inferno/cogs/Images/Thanos/thanosout.png')
    return
  @commands.command(aliases=["DrStrange","Drstrange","DRSTRANGE","doctorstrange"],description = "Creates a Dr. Strange image using the user's avatar")
  async def drstrange(self,ctx,user : discord.Member=None):
    if not user:
      user=ctx.author
    im = Image.open('/home/pranav/Inferno/Inferno/cogs/Images/DrStrange/drstrange.jpg')
    im = im.convert('RGBA')
    im.putalpha(255)

    avatar = await make_avatar(user)

    sized_avatar = resize_avatar(avatar, (69,76), rot=0)

    im.alpha_composite(sized_avatar,dest=(225,66))

    im.save('/home/pranav/Inferno/Inferno/cogs/Images/DrStrange/drstrangeout.png')
    await ctx.send(file=discord.File('/home/pranav/Inferno/Inferno/cogs/Images/DrStrange/drstrangeout.png'))
    os.remove('/home/pranav/Inferno/Inferno/cogs/Images/DrStrange/drstrangeout.png')
    return
  @commands.command(aliases=["Spiderman","SPIDERMAN","SpiderMan"],description = "Creates a SpiderMan image using the user's avatar")
  async def spiderman(self,ctx,user : discord.Member=None):
    if not user:
      user=ctx.author
    im = Image.open('/home/pranav/Inferno/Inferno/cogs/Images/Spiderman/spiderman.jpg')
    im = im.convert('RGBA')
    im.putalpha(255)

    avatar = await make_avatar(user)

    sized_avatar = resize_avatar(avatar, (137,154), rot=0)

    im.alpha_composite(sized_avatar,dest=(349,40))

    im.save('/home/pranav/Inferno/Inferno/cogs/Images/Spiderman/spidermanout.png')
    await ctx.send(file=discord.File('/home/pranav/Inferno/Inferno/cogs/Images/Spiderman/spidermanout.png'))
    os.remove('/home/pranav/Inferno/Inferno/cogs/Images/Spiderman/spidermanout.png')
    return
  @commands.command(aliases=["Captainamerica","CaptainAmerica","CAPTAINAMERICA","CAPAMERICA","CapAmerica","capamerica"],description = "Creates a Captain America image using the user's avatar")
  async def captainamerica(self,ctx,user : discord.Member=None):
    if not user:
      user=ctx.author
    im = Image.open('/home/pranav/Inferno/Inferno/cogs/Images/Captain/captainamerica.jpg')
    im = im.convert('RGBA')
    im.putalpha(255)

    avatar = await make_avatar(user)

    sized_avatar = resize_avatar(avatar, (172,193), rot=0)

    im.alpha_composite(sized_avatar,dest=(368,83))

    im.save('/home/pranav/Inferno/Inferno/cogs/Images/Captain/captainamericaout.png')
    await ctx.send(file=discord.File('/home/pranav/Inferno/Inferno/cogs/Images/Captain/captainamericaout.png'))
    os.remove('/home/pranav/Inferno/Inferno/cogs/Images/Captain/captainamericaout.png')
    return
  @commands.command(aliases=["Hulk","HULK"],description = "Creates a Hulk image using the user's avatar")
  async def hulk(self,ctx,user : discord.Member=None):
    if not user:
      user=ctx.author
    im = Image.open('/home/pranav/Inferno/Inferno/cogs/Images/Hulk/hulk.jpg')
    im = im.convert('RGBA')
    im.putalpha(255)

    avatar = await make_avatar(user)

    sized_avatar = resize_avatar(avatar, (97,100), rot=13)

    im.alpha_composite(sized_avatar,dest=(127,47))

    im.save('/home/pranav/Inferno/Inferno/cogs/Images/Hulk/hulkoutput.png')
    await ctx.send(file=discord.File('/home/pranav/Inferno/Inferno/cogs/Images/Hulk/hulkoutput.png'))
    os.remove('/home/pranav/Inferno/Inferno/cogs/Images/Hulk/hulkoutput.png')
    return
  @commands.command(aliases = ["Slap","SLAP"],description = "Slaps the user")
  async def slap(self,ctx, user : discord.Member):
    
    user = ctx.author if not user else user
    im = Image.open('/home/pranav/Inferno/Inferno/cogs/Images/Slap/slap.png')
    im = im.convert('RGBA')
    im.putalpha(255)
    pfp1 = await make_avatar(ctx.author)
    pfp1 = resize_avatar(pfp1, (300,300), rot=0)
    pfp2 = await make_avatar(user)
    pfp2 = resize_avatar(pfp2, (300,300), rot=0)
    im.alpha_composite(pfp1,dest=(500,60))
    im.alpha_composite(pfp2,dest=(808,350))
    im.save('/home/pranav/Inferno/Inferno/cogs/Images/Slap/slapout.png')
    await ctx.send(file=discord.File('/home/pranav/Inferno/Inferno/cogs/Images/Slap/slapout.png'))
    os.remove('/home/pranav/Inferno/Inferno/cogs/Images/Slap/slapout.png')
    return

async def setup(client):
  await client.add_cog(Image_Manipulation(client))


    
   