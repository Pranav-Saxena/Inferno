import os
import discord
import aiohttp
import random
from discord.ext import commands
from PIL import ImageFont, ImageDraw, Image
from io import BytesIO
from functools import partial
import asyncio
import re
import motor.motor_asyncio
import nest_asyncio
nest_asyncio.apply()
cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb_client_auth")
welcomedb = cluster["welcome"]["welcome"]
leavedb = cluster["leave"]["leave"]

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
def resize_bg(image, size, rot=0):
    new_image = image.copy()
    new_image = new_image.rotate(rot)
    if size != new_image.size:
        new_image = new_image.resize(size)
    return new_image



class Welcome(commands.Cog):
    def __init__(self,client):
        self.client = client
    @staticmethod
    def make_infernocom_similar(avatar,member):
        folder = os.path.join('./', 'cogs', 'welcome')
        im = Image.open('/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/bgwelcomeinfernocom.png')
        im = im.convert('RGBA')
        im.putalpha(255)
        sized_avatar = resize_avatar(avatar, (197,197), rot=0)
        im.alpha_composite(sized_avatar,dest=(56,49))
        im.save("/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/tempwelcome.png")
        fnt = ImageFont.truetype("/home/pranav/Inferno/Inferno/roboto.TTF", 46)
        img = Image.open("/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/tempwelcome.png")
        d = ImageDraw.Draw(img)
        d.multiline_text((300, 124), f"{member.name}#{member.discriminator}", font=fnt, fill=(0, 128, 128))
        outfile = os.path.join(folder, 'welcome.png')
        img.save(outfile)
        return outfile
#-------------presets creation------------------------------------------
    @staticmethod
    def preset1(avatar,member,im,text,fontcolour):
        im  = resize_bg(im, (936,284), rot=0)
        mask = Image.open('/home/pranav/Inferno/Inferno/cogs/welcome/circlemask.png')
        mask = mask.convert("RGBA")
        im.paste(mask,(0,0),mask)
        folder = os.path.join('./', 'cogs', 'welcome')
        
        x=member.guild.members
        l=[]
        for i in x:
            if i.bot:
                l.append(i)
        humanscount = len(x) - len(l)
        memcount = len(x)
        botscount = len(l)
        dict= {"0":"th","1":"st","2":"nd","3":"rd","4":"th","5":"th","6":"th","7":"th","8":"th","9":"th"}
        if str(memcount)[-2:] in ["11","12","13"]:
            memordinal = "th"
        else:
            memordinal = dict[str(memcount)[-1]]
            
        if str(humanscount)[-2:] in ["11","12","13"]:
            humanordinal = "th"
        else:
            humanordinal = dict[str(humanscount)[-1]]
            
        if str(botscount)[-2:] in ["11","12","13"]:
            botordinal = "th"
        else:
            botordinal = dict[str(botscount)[-1]]
        text = text.replace("{server}",f"{member.guild.name}")
        text = text.replace("{username}",f"{member.name}#{member.discriminator}")
        text = text.replace("{membercount}",f"{memcount}")
        text = text.replace("{botcount}",f"{botscount}")
        text = text.replace("{humancount}",f"{humanscount}")
        text = text.replace("{membercount.ordinal}",f"{memordinal}")
        text = text.replace("{humancount.ordinal}",f"{humanordinal}")
        text = text.replace("{botcount.ordinal}",f"{botordinal}")
        newtext = ''
        numberoflines = 1
        if len(text)>23:
            newtext = text[:23]+"\n"+text[23:]
            numberoflines=2
            if len(text)>46:
                newtext = text[:23] +"\n" +text[23:46] +"\n"+text[46:]
                numberoflines=3
        else:
            newtext = text
        
        if numberoflines==1:
            textdest = (300,124)
        elif numberoflines==2:
            textdest =(300,114)
        else:
            textdest = (300,94)
        sized_avatar = resize_avatar(avatar, (197,197), rot=0)
        # im.alpha_composite(mask)
        im.putalpha(255)
        im.alpha_composite(sized_avatar,dest=(56,49))
        im.save(f"/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/tempwelcome{member.id}.png")
        fnt = ImageFont.truetype("/home/pranav/Inferno/Inferno/roboto.TTF", 46)
        img = Image.open(f"/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/tempwelcome{member.id}.png")
        d = ImageDraw.Draw(img)
        d.multiline_text(textdest, f"{newtext}", font=fnt, fill=tuple(fontcolour))
        outfile = os.path.join(folder, f'welcome{member.id}.png')
        img.save(outfile)
        return outfile
    @staticmethod
    def defaultpreset1(avatar,member,text,fontcolour):
        folder = os.path.join('./', 'cogs', 'welcome','temp')
        im = Image.open('/home/pranav/Inferno/Inferno/cogs/welcome/preset1.png')
        im = im.convert('RGBA')
        im.putalpha(255)
        sized_avatar = resize_avatar(avatar, (197,197), rot=0)
        im.alpha_composite(sized_avatar,dest=(56,49))
        im.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/temp/tempwelcome{member.id}.png")
        fnt = ImageFont.truetype("/home/pranav/Inferno/Inferno/roboto.TTF", 46)
        img = Image.open(f"/home/pranav/Inferno/Inferno/cogs/welcome/temp/tempwelcome{member.id}.png")
        d = ImageDraw.Draw(img)

        x=member.guild.members
        l=[]
        for i in x:
            if i.bot:
                l.append(i)
        humanscount = len(x) - len(l)
        memcount = len(x)
        botscount = len(l)
        dict= {"0":"th","1":"st","2":"nd","3":"rd","4":"th","5":"th","6":"th","7":"th","8":"th","9":"th"}
        if str(memcount)[-2:] in ["11","12","13"]:
            memordinal = "th"
        else:
            memordinal = dict[str(memcount)[-1]]
            
        if str(humanscount)[-2:] in ["11","12","13"]:
            humanordinal = "th"
        else:
            humanordinal = dict[str(humanscount)[-1]]
            
        if str(botscount)[-2:] in ["11","12","13"]:
            botordinal = "th"
        else:
            botordinal = dict[str(botscount)[-1]]
        text = text.replace("{server}",f"{member.guild.name}")
        text = text.replace("{username}",f"{member.name}#{member.discriminator}")
        text = text.replace("{membercount}",f"{memcount}")
        text = text.replace("{botcount}",f"{botscount}")
        text = text.replace("{humancount}",f"{humanscount}")
        text = text.replace("{membercount.ordinal}",f"{memordinal}")
        text = text.replace("{humancount.ordinal}",f"{humanordinal}")
        text = text.replace("{botcount.ordinal}",f"{botordinal}")
        newtext = ''

        numberoflines = 1
        if len(text)>23:
            newtext = text[:23]+"\n"+text[23:]
            numberoflines = 2
            if len(text)>46:
                newtext = text[:23] +"\n" +text[23:46] +"\n"+text[46:]
                numberoflines = 3
        else:
            newtext = text
        if numberoflines==1:
            textdest = (300,124)
        elif numberoflines==2:
            textdest =(300,114)
        else:
            textdest =(300,84)
        d.multiline_text(textdest, f"{newtext}", font=fnt, fill=tuple(fontcolour))
        outfile = os.path.join(folder, f'welcome{member.id}.png')
        img.save(outfile)
        return outfile

#-------------preset 2 ---------------(26,100)
    @staticmethod
    def defaultpreset2(member,text,fontcolour):
        folder = os.path.join('./', 'cogs', 'welcome','temp')
        img = Image.open(f"/home/pranav/Inferno/Inferno/cogs/welcome/preset2.png")
        fnt = ImageFont.truetype("/home/pranav/Inferno/Inferno/roboto.TTF", 46)
        d = ImageDraw.Draw(img)
        x=member.guild.members
        l=[]
        for i in x:
            if i.bot:
                l.append(i)
        humanscount = len(x) - len(l)
        memcount = len(x)
        botscount = len(l)
        dict= {"0":"th","1":"st","2":"nd","3":"rd","4":"th","5":"th","6":"th","7":"th","8":"th","9":"th"}
        if str(memcount)[-2:] in ["11","12","13"]:
            memordinal = "th"
        else:
            memordinal = dict[str(memcount)[-1]]
            
        if str(humanscount)[-2:] in ["11","12","13"]:
            humanordinal = "th"
        else:
            humanordinal = dict[str(humanscount)[-1]]
            
        if str(botscount)[-2:] in ["11","12","13"]:
            botordinal = "th"
        else:
            botordinal = dict[str(botscount)[-1]]
        text = text.replace("{server}",f"{member.guild.name}")
        text = text.replace("{username}",f"{member.name}#{member.discriminator}")
        text = text.replace("{membercount}",f"{memcount}")
        text = text.replace("{botcount}",f"{botscount}")
        text = text.replace("{humancount}",f"{humanscount}")
        text = text.replace("{membercount.ordinal}",f"{memordinal}")
        text = text.replace("{humancount.ordinal}",f"{humanordinal}")
        text = text.replace("{botcount.ordinal}",f"{botordinal}")
        newtext = ''
        if len(text)>33:
            newtext = text[:33]+"\n"+text[33:]
            if len(text)>66:
                newtext = text[:33] +"\n" +text[33:66] +"\n"+text[66:]
                if len(text) >99:
                    newtext = text[:33] +"\n" +text[33:66] +"\n"+text[66:99] + '\n' +text[99:]
        else:
            newtext = text
        d.multiline_text((26, 100), f"{newtext}", font=fnt, fill=tuple(fontcolour))
        outfile = os.path.join(folder, f'welcome{member.id}.png')
        img.save(outfile)
        return outfile
    @staticmethod
    def preset2(member,im,text,fontcolour):
        folder = os.path.join('./', 'cogs', 'welcome','temp')
        im  = resize_bg(im, (936,284), rot=0)
        fnt = ImageFont.truetype("/home/pranav/Inferno/Inferno/roboto.TTF", 46)
        x=member.guild.members
        l=[]
        for i in x:
            if i.bot:
                l.append(i)
        humanscount = len(x) - len(l)
        memcount = len(x)
        botscount = len(l)
        dict= {"0":"th","1":"st","2":"nd","3":"rd","4":"th","5":"th","6":"th","7":"th","8":"th","9":"th"}
        if str(memcount)[-2:] in ["11","12","13"]:
            memordinal = "th"
        else:
            memordinal = dict[str(memcount)[-1]]
            
        if str(humanscount)[-2:] in ["11","12","13"]:
            humanordinal = "th"
        else:
            humanordinal = dict[str(humanscount)[-1]]
            
        if str(botscount)[-2:] in ["11","12","13"]:
            botordinal = "th"
        else:
            botordinal = dict[str(botscount)[-1]]
        text = text.replace("{server}",f"{member.guild.name}")
        text = text.replace("{username}",f"{member.name}#{member.discriminator}")
        text = text.replace("{membercount}",f"{memcount}")
        text = text.replace("{botcount}",f"{botscount}")
        text = text.replace("{humancount}",f"{humanscount}")
        text = text.replace("{membercount.ordinal}",f"{memordinal}")
        text = text.replace("{humancount.ordinal}",f"{humanordinal}")
        text = text.replace("{botcount.ordinal}",f"{botordinal}")
        newtext = ''
        if len(text)>33:
            newtext = text[:33]+"\n"+text[33:]
            if len(text)>66:
                newtext = text[:33] +"\n" +text[33:66] +"\n"+text[66:]
                if len(text) >99:
                    newtext = text[:33] +"\n" +text[33:66] +"\n"+text[66:99] + '\n' +text[99:]
        else:
            newtext = text
        
        d = ImageDraw.Draw(im)
        d.multiline_text((26, 100), f"{newtext}", font=fnt, fill=tuple(fontcolour))
        outfile = os.path.join(folder, f'welcome{member.id}.png')
        im.save(outfile)
        return outfile
#------------do in preset1 that if only 1 line then position is different -------------------
# preset 3--------
    @staticmethod
    def preset3(avatar,member,im,text,fontcolour):
        im  = resize_bg(im, (936,284), rot=0)
        folder = os.path.join('./', 'cogs', 'welcome')
        
        x=member.guild.members
        l=[]
        for i in x:
            if i.bot:
                l.append(i)
        humanscount = len(x) - len(l)
        memcount = len(x)
        botscount = len(l)
        dict= {"0":"th","1":"st","2":"nd","3":"rd","4":"th","5":"th","6":"th","7":"th","8":"th","9":"th"}
        if str(memcount)[-2:] in ["11","12","13"]:
            memordinal = "th"
        else:
            memordinal = dict[str(memcount)[-1]]
            
        if str(humanscount)[-2:] in ["11","12","13"]:
            humanordinal = "th"
        else:
            humanordinal = dict[str(humanscount)[-1]]
            
        if str(botscount)[-2:] in ["11","12","13"]:
            botordinal = "th"
        else:
            botordinal = dict[str(botscount)[-1]]
        text = text.replace("{server}",f"{member.guild.name}")
        text = text.replace("{username}",f"{member.name}#{member.discriminator}")
        text = text.replace("{membercount}",f"{memcount}")
        text = text.replace("{botcount}",f"{botscount}")
        text = text.replace("{humancount}",f"{humanscount}")
        text = text.replace("{membercount.ordinal}",f"{memordinal}")
        text = text.replace("{humancount.ordinal}",f"{humanordinal}")
        text = text.replace("{botcount.ordinal}",f"{botordinal}")
        newtext = ''
        numberoflines = 1
        if len(text)>23:
            newtext = text[:23]+"\n"+text[23:]
            numberoflines = 2
            if len(text)>46:
                newtext = text[:23] +"\n" +text[23:46] +"\n"+text[46:]
                numberoflines = 3
        else:
            newtext = text
        if numberoflines==1:
            textdest = (300,124)
        elif numberoflines==2:
            textdest =(300,114)
        else:
            textdest =(300,84)
        sized_avatar = resize_avatar(avatar, (197,197), rot=0)
        # im.alpha_composite(mask)
        im.putalpha(255)
        im.alpha_composite(sized_avatar,dest=(56,49))
        im.save(f"/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/tempwelcome{member.id}.png")
        fnt = ImageFont.truetype("/home/pranav/Inferno/Inferno/roboto.TTF", 46)
        img = Image.open(f"/home/pranav/Inferno/Inferno/cogs/Images/welcomeinfernocommunity/tempwelcome{member.id}.png")
        d = ImageDraw.Draw(img)
        d.multiline_text((300, 109), f"{newtext}", font=fnt, fill=tuple(fontcolour))
        outfile = os.path.join(folder, f'welcome{member.id}.png')
        img.save(outfile)
        return outfile
    @staticmethod
    def defaultpreset3(avatar,member,text,fontcolour):
        folder = os.path.join('./', 'cogs', 'welcome','temp')
        im = Image.open('/home/pranav/Inferno/Inferno/cogs/welcome/preset3.png')
        im = im.convert('RGBA')
        im.putalpha(255)
        sized_avatar = resize_avatar(avatar, (197,197), rot=0)
        im.alpha_composite(sized_avatar,dest=(56,49))
        im.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/temp/tempwelcome{member.id}.png")
        fnt = ImageFont.truetype("/home/pranav/Inferno/Inferno/roboto.TTF", 46)
        img = Image.open(f"/home/pranav/Inferno/Inferno/cogs/welcome/temp/tempwelcome{member.id}.png")
        d = ImageDraw.Draw(img)

        x=member.guild.members
        l=[]
        for i in x:
            if i.bot:
                l.append(i)
        humanscount = len(x) - len(l)
        memcount = len(x)
        botscount = len(l)
        dict= {"0":"th","1":"st","2":"nd","3":"rd","4":"th","5":"th","6":"th","7":"th","8":"th","9":"th"}
        if str(memcount)[-2:] in ["11","12","13"]:
            memordinal = "th"
        else:
            memordinal = dict[str(memcount)[-1]]
            
        if str(humanscount)[-2:] in ["11","12","13"]:
            humanordinal = "th"
        else:
            humanordinal = dict[str(humanscount)[-1]]
            
        if str(botscount)[-2:] in ["11","12","13"]:
            botordinal = "th"
        else:
            botordinal = dict[str(botscount)[-1]]
        text = text.replace("{server}",f"{member.guild.name}")
        text = text.replace("{username}",f"{member.name}#{member.discriminator}")
        text = text.replace("{membercount}",f"{memcount}")
        text = text.replace("{botcount}",f"{botscount}")
        text = text.replace("{humancount}",f"{humanscount}")
        text = text.replace("{membercount.ordinal}",f"{memordinal}")
        text = text.replace("{humancount.ordinal}",f"{humanordinal}")
        text = text.replace("{botcount.ordinal}",f"{botordinal}")
        newtext = ''
        numberoflines = 1
        if len(text)>23:
            newtext = text[:23]+"\n"+text[23:]
            numberoflines = 2
            if len(text)>46:
                newtext = text[:23] +"\n" +text[23:46] +"\n"+text[46:]
                numberoflines = 3
        else:
            newtext = text
        
        if numberoflines==1:
            textdest = (300,124)
        elif numberoflines==2:
            textdest =(300,114)
        else:
            textdest =(300,84)
        d.multiline_text((300, 109), f"{newtext}", font=fnt, fill=tuple(fontcolour))
        outfile = os.path.join(folder, f'welcome{member.id}.png')
        img.save(outfile)
        return outfile
#---------preset4------(0,310), (1000,370)  ; (0,370), (1000,418)
    @staticmethod
    def defaultpreset4(avatar,member):
        folder = os.path.join('./', 'cogs', 'welcome','temp')
        im = Image.open('/home/pranav/Inferno/Inferno/cogs/welcome/preset4.png')
        fnt1 = ImageFont.truetype("/home/pranav/Inferno/Inferno/Roboto-Bold.ttf", 36)
        fnt2 = ImageFont.truetype("/home/pranav/Inferno/Inferno/Roboto-Regular.ttf", 30)
        draw = ImageDraw.Draw(im)
        bounding_box1 = [0,310,1000,370]
        bounding_box2 = [0,370,1000,418]
        x1a, y1a, x2a, y2a = bounding_box1 
        x1b, y1b, x2b, y2b = bounding_box2 # For easy reading
        # Calculate the width and height of the text to be drawn, given font size
        s = f"{member.name}#{member.discriminator}"
        if len(s)>46:
            s = s[:41]+"#"+s[-4:]

        x=member.guild.members
        l=[]
        for i in x:
            if i.bot:
                l.append(i)
        humancount = len(x) - len(l)
        w1, h1 = draw.textsize(s, font=fnt1)
        w2, h2 = draw.textsize(f"Member#{humancount}", font=fnt2)

        # Calculate the mid points and offset by the upper left corner of the bounding box
        xa = (x2a - x1a - w1)/2 + x1a
        ya = (y2a - y1a - h1)/2 + y1a
        xb = (x2b - x1b - w2)/2 + x1b
        yb = (y2b - y1b - h2)/2 + y1b

        # Write the text to the image, where (x,y) is the top left corner of the text
        draw.text((xa, ya), s, align='center', font=fnt1)
        draw.text((xb, yb), f"Member#{humancount}", align='center', font=fnt2)

        im = im.convert('RGBA')
        im.putalpha(255)
        sized_avatar = resize_avatar(avatar, (199,198), rot=0)
        im.alpha_composite(sized_avatar,dest=(403,73))
        outfile = os.path.join(folder, f'welcome{member.id}.png')
        im.save(outfile)
        return outfile
    @staticmethod
    def preset4(avatar,member,im):
        im  = resize_bg(im, (1000,450), rot=0)
        folder = os.path.join('./', 'cogs', 'welcome')
        fnt1 = ImageFont.truetype("/home/pranav/Inferno/Inferno/Roboto-Bold.ttf", 36)
        fnt2 = ImageFont.truetype("/home/pranav/Inferno/Inferno/Roboto-Regular.ttf", 30)
        draw = ImageDraw.Draw(im)
        bounding_box1 = [0,310,1000,370]
        bounding_box2 = [0,370,1000,418]
        x1a, y1a, x2a, y2a = bounding_box1 
        x1b, y1b, x2b, y2b = bounding_box2 # For easy reading
        # Calculate the width and height of the text to be drawn, given font size
        s = f"{member.name}#{member.discriminator}"
        x=member.guild.members
        l=[]
        for i in x:
            if i.bot:
                l.append(i)
        humancount = len(x) - len(l)
        
        if len(s)>46:
            s = s[:41]+"#"+s[-4:]
        w1, h1 = draw.textsize(s, font=fnt1)
        w2, h2 = draw.textsize(f"Member#{humancount}", font=fnt2)

        # Calculate the mid points and offset by the upper left corner of the bounding box
        xa = (x2a - x1a - w1)/2 + x1a
        ya = (y2a - y1a - h1)/2 + y1a
        xb = (x2b - x1b - w2)/2 + x1b
        yb = (y2b - y1b - h2)/2 + y1b

        # Write the text to the image, where (x,y) is the top left corner of the text
        draw.text((xa, ya), s, align='center', font=fnt1)
        draw.text((xb, yb), f"Member#{humancount}", align='center', font=fnt2)
        sized_avatar = resize_avatar(avatar, (199,198), rot=0)
        # im.alpha_composite(mask)
        im = im.convert('RGBA')
        mask = Image.open('/home/pranav/Inferno/Inferno/cogs/welcome/preset4mask.png')
        mask = mask.convert("RGBA")
        im.paste(mask,(0,0),mask)

        im.putalpha(255)
        im.alpha_composite(sized_avatar,dest=(403,73))
        outfile = os.path.join(folder, f'welcome{member.id}.png')
        im.save(outfile)
        return outfile
#--------main--------
#------------leave----------------------------
    @commands.Cog.listener("on_member_remove")
    async def leave(self,member):
        count = await leavedb.count_documents({"guildid":str(member.guild.id)})
        if count ==0:
            return
        data = await leavedb.find_one({"guildid":str(member.guild.id)})
        if 1==1:#i am lazy to change indents
            x=member.guild.members
            l=[]
            for i in x:
                if i.bot:
                    l.append(i)
            humanscount = len(x) - len(l)
            memcount = len(x)
            botscount = len(l)
            dict= {"0":"th","1":"st","2":"nd","3":"rd","4":"th","5":"th","6":"th","7":"th","8":"th","9":"th"}
            if str(memcount)[-2:] in ["11","12","13"]:
                memordinal = "th"
            else:
                memordinal = dict[str(memcount)[-1]]
            
            if str(humanscount)[-2:] in ["11","12","13"]:
                humanordinal = "th"
            else:
                humanordinal = dict[str(humanscount)[-1]]
            
            if str(botscount)[-2:] in ["11","12","13"]:
                botordinal = "th"
            else:
                botordinal = dict[str(botscount)[-1]]

            text  = data ['textoutput']
            text  = text.replace("{user}",f"<@{member.id}>")
            text = text.replace("{username}",f"{member.name}#{member.discriminator}")
            text = text.replace("{server}",f"{member.guild.name}")
            text = text.replace("{membercount}",f"{memcount}")
            text = text.replace("{botcount}",f"{botscount}")
            text = text.replace("{humancount}",f"{humanscount}")
            text = text.replace("{membercount.ordinal}",f"{memordinal}")
            text = text.replace("{humancount.ordinal}",f"{humanordinal}")
            text = text.replace("{botcount.ordinal}",f"{botordinal}")
            channelid = int(data['channelid'])
            await self.client.get_channel(channelid).send(text)
        return
#---welcome------

    @commands.Cog.listener("on_member_join")
    async def welcome(self,member):
        count = await welcomedb.count_documents({"guildid":str(member.guild.id)})
        if count ==0:
            return
        data = await welcomedb.find_one({"guildid":str(member.guild.id)})
        if data['text'] == 0 and data['image'] ==1:
            presetnumber = data['preset']
            custom = data['custom']
            if custom == "no":
                if presetnumber == 1:
                    text = data['imagetext']
                    fontcolour = data['fontcolour']
                    
                    avatar = await make_avatar(member)
                    fn = partial(self.defaultpreset1, avatar,member,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        try:
                            await self.client.get_channel(int(channel)).send(embed=embed,file=file)
                        except:
                            pass
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return
                elif presetnumber ==2:
                    text= data['imagetext']
                    embedcheck = data["embedimage"]
                    channel = data['channelid']
                    fontcolour = data['fontcolour']
                    fn = partial(self.defaultpreset2,member,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(file=discord.File(outfile))
                        os.remove(outfile)
                        return
                elif presetnumber ==3:
                    text = data['imagetext']
                    avatar = await make_avatar(member)
                    fontcolour = data['fontcolour']
                    fn = partial(self.defaultpreset3, avatar,member,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return
                else:
                    avatar = await make_avatar(member)
                    fn = partial(self.defaultpreset4, avatar,member)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return
            if custom == "yes":
                if presetnumber == 1:
                    text = data['imagetext']
                    im = Image.open(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{member.guild.id}.png")
                    im = make_RGBA(im)
                    fontcolour = data['fontcolour']
                    avatar = await make_avatar(member)
                    fn = partial(self.preset1, avatar,member,im,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return
                elif presetnumber ==2:
                    text= data['imagetext']
                    im = Image.open(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{member.guild.id}.png")
                    im = make_RGBA(im)
                    fontcolour = data['fontcolour']
                    fn = partial(self.preset2,member,im,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    embedcheck = data["embedimage"]
                    channel = data['channelid']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(file=discord.File(outfile))
                        os.remove(outfile)
                        return
                elif presetnumber ==3:
                    text = data['imagetext']
                    avatar = await make_avatar(member)
                    im = Image.open(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{member.guild.id}.png")
                    im = make_RGBA(im)
                    fontcolour = data['fontcolour']
                    fn = partial(self.preset3, avatar,member,im,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return
                else:
                    im = Image.open(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{member.guild.id}.png")
                    avatar = await make_avatar(member)
                    fn = partial(self.preset4, avatar,member,im)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return



            # avatar = await make_avatar(member)
            # fn = partial(self.make_infernocom_similar, avatar,member)
            # outfile = await self.client.loop.run_in_executor(None, fn)
            # await self.client.get_channel(840914226062426132).send(file=discord.File(outfile))
            # os.remove(outfile)
            # return
        elif data['text']==1 and data['image']==1:
            presetnumber = data['preset']
            custom = data['custom']
            
            x=member.guild.members
            l=[]
            for i in x:
                if i.bot:
                    l.append(i)
            humanscount = len(x) - len(l)
            memcount = len(x)
            botscount = len(l)
            dict= {"0":"th","1":"st","2":"nd","3":"rd","4":"th","5":"th","6":"th","7":"th","8":"th","9":"th"}
            if str(memcount)[-2:] in ["11","12","13"]:
                memordinal = "th"
            else:
                memordinal = dict[str(memcount)[-1]]
            
            if str(humanscount)[-2:] in ["11","12","13"]:
                humanordinal = "th"
            else:
                humanordinal = dict[str(humanscount)[-1]]
            
            if str(botscount)[-2:] in ["11","12","13"]:
                botordinal = "th"
            else:
                botordinal = dict[str(botscount)[-1]]

            textnormal  = data ['textoutput']
            textnormal  = textnormal.replace("{user}",f"<@{member.id}>")
            textnormal = textnormal.replace("{username}",f"{member.name}#{member.discriminator}")
            textnormal = textnormal.replace("{server}",f"{member.guild.name}")
            textnormal = textnormal.replace("{membercount}",f"{memcount}")
            textnormal = textnormal.replace("{botcount}",f"{botscount}")
            textnormal = textnormal.replace("{humancount}",f"{humanscount}")
            textnormal = textnormal.replace("{membercount.ordinal}",f"{memordinal}")
            textnormal = textnormal.replace("{humancount.ordinal}",f"{humanordinal}")
            textnormal = textnormal.replace("{botcount.ordinal}",f"{botordinal}")

            if custom == "no":
                if presetnumber == 1:
                    text = data['imagetext']
                    avatar = await make_avatar(member)
                    fontcolour = data['fontcolour']
                    fn = partial(self.defaultpreset1, avatar,member,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return
                elif presetnumber ==2:
                    text= data['imagetext']
                    embedcheck = data["embedimage"]
                    channel = data['channelid']
                    fontcolour = data['fontcolour']
                    fn = partial(self.defaultpreset2,member,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",file=discord.File(outfile))
                        os.remove(outfile)
                        return
                elif presetnumber ==3:
                    text = data['imagetext']
                    avatar = await make_avatar(member)
                    fontcolour = data['fontcolour']
                    fn = partial(self.defaultpreset3, avatar,member,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return
                else:
                    avatar = await make_avatar(member)
                    fn = partial(self.defaultpreset4, avatar,member)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return
            if custom == "yes":
                if presetnumber == 1:
                    text = data['imagetext']
                    im = Image.open(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{member.guild.id}.png")
                    im = make_RGBA(im)
                    avatar = await make_avatar(member)
                    fontcolour = data['fontcolour']
                    fn = partial(self.preset1, avatar,member,im,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return
                elif presetnumber ==2:
                    text= data['imagetext']
                    im = Image.open(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{member.guild.id}.png")
                    im = make_RGBA(im)
                    fontcolour = data['fontcolour']
                    fn = partial(self.preset2,member,im,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    embedcheck = data["embedimage"]
                    channel = data['channelid']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",file=discord.File(outfile))
                        os.remove(outfile)
                        return
                elif presetnumber ==3:
                    text = data['imagetext']
                    avatar = await make_avatar(member)
                    im = Image.open(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{member.guild.id}.png")
                    im = make_RGBA(im)
                    fontcolour = data['fontcolour']
                    fn = partial(self.preset3, avatar,member,im,text,fontcolour)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return
                else:
                    im = Image.open(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{member.guild.id}.png")
                    avatar = await make_avatar(member)
                    fn = partial(self.preset4, avatar,member,im)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    channel = data['channelid']
                    embedcheck = data['embedimage']
                    if embedcheck == "yes":
                        embed = discord.Embed(colour=discord.Colour.purple())
                        file = discord.File(str(outfile), filename="welcome.png")
                        embed.set_image(url="attachment://welcome.png")
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",embed=embed,file=file)
                        os.remove(outfile)
                        return
                    else:
                        await self.client.get_channel(int(channel)).send(f"{textnormal}",file=discord.File(outfile))
                        os.remove(outfile)
                        return
                    return

        elif data['text']==1 and data['image']==0:
            x=member.guild.members
            l=[]
            for i in x:
                if i.bot:
                    l.append(i)
            humanscount = len(x) - len(l)
            memcount = len(x)
            botscount = len(l)
            dict= {"0":"th","1":"st","2":"nd","3":"rd","4":"th","5":"th","6":"th","7":"th","8":"th","9":"th"}
            if str(memcount)[-2:] in ["11","12","13"]:
                memordinal = "th"
            else:
                memordinal = dict[str(memcount)[-1]]
            
            if str(humanscount)[-2:] in ["11","12","13"]:
                humanordinal = "th"
            else:
                humanordinal = dict[str(humanscount)[-1]]
            
            if str(botscount)[-2:] in ["11","12","13"]:
                botordinal = "th"
            else:
                botordinal = dict[str(botscount)[-1]]

            text  = data ['textoutput']
            text  = text.replace("{user}",f"<@{member.id}>")
            text = text.replace("{username}",f"{member.name}#{member.discriminator}")
            text = text.replace("{server}",f"{member.guild.name}")
            text = text.replace("{membercount}",f"{memcount}")
            text = text.replace("{botcount}",f"{botscount}")
            text = text.replace("{humancount}",f"{humanscount}")
            text = text.replace("{membercount.ordinal}",f"{memordinal}")
            text = text.replace("{humancount.ordinal}",f"{humanordinal}")
            text = text.replace("{botcount.ordinal}",f"{botordinal}")
            channelid = int(data['channelid'])
            await self.client.get_channel(channelid).send(text)
            return
        return

    @commands.command(aliases = ['swt'],description="Sets Welcome Text in the Server")
    @commands.has_permissions(manage_guild=True)
    async def setwelcometext(self,ctx):
        count = await welcomedb.count_documents({"guildid":str(ctx.guild.id),"text":1})
        if count ==1:
            embed = discord.Embed(color=discord.Colour.purple(),description="Welcome text is already setup in your server.\nUse `>delwelcometext` to disable it and use this cmd again if you want to change the welcome text")
            return await ctx.send(embed=embed)
        
        #------text-replacer---------------
        count2 = await welcomedb.count_documents({"guildid":str(ctx.guild.id)})
        if count2 ==0:
            embed = discord.Embed(title="Step 1",color=discord.Colour.purple(),description="Enter channel where you want to setup welcome text")
            msg = await ctx.send(embed=embed)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                channelinput = await self.client.wait_for("message", timeout=120, check=check)
            except:
                embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                await msg.edit(embed=embed)
                return
            try:
                channel = await commands.TextChannelConverter().convert(ctx, channelinput.content)
            except:
                embed = discord.Embed(color=discord.Colour.purple(),description="Invalid channel entered.\nPlease restart the process from beginning")
                return await ctx.send(embed=embed)
            embed = discord.Embed(title="Step 2",color=discord.Colour.purple(),description='''Enter the welcome text which will be sent when a member joins the server.\n\n```q
Available Tags:- 

"{user}" - mentions the user.

"{username}" - display users username with his discriminator

"{server}" - displays server name.

"{membercount}" - shows the member count of the server(including bots). `Example: {user} joined ! We are now {membercount} in the server.`

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
            msg = await ctx.send(embed=embed)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                textinput = await self.client.wait_for("message", timeout=120, check=check)
            except:
                embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                await msg.edit(embed=embed)
                return
            text = textinput.content

            info ={
                "guildid":str(ctx.guild.id),
                "text" : 1,
                "textoutput":text,
                "image" :0,
                "channelid" : str(channel.id)
            }
            await welcomedb.insert_one(info)
            embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome text has been setup successfully in {channel.mention}")
            await ctx.send(embed=embed)
            return
#--------make if channel already exists ie. welcome img is setup----
        else:
            embed = discord.Embed(title="Step 1",color=discord.Colour.purple(),description='''Enter the welcome text which will be sent when a member joins the server.\n\n```q
Available Tags:- 

"{user}" - mentions the user.

"{username}" - display users username with his discriminator

"{server}" - displays server name.

"{membercount}" - shows the member count of the server(including bots). `Example: {user} joined ! We are now {membercount} in the server.`

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
            msg = await ctx.send(embed=embed)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                textinput = await self.client.wait_for("message", timeout=120, check=check)
            except:
                embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                await msg.edit(embed=embed)
                return
            text = textinput.content
            data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
            data['text'] = 1
            data['textoutput']= text
            await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
            embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome text has been setup successfully in {self.client.get_channel(int(data['channelid'])).mention}")
            await ctx.send(embed=embed)
            return
#------------embedtext------------
    @commands.command(aliases = ['swi'],description="Sets Welcome Image in the Server")
    @commands.has_permissions(manage_guild=True)
    async def setwelcomeimage(self,ctx):
        count = await welcomedb.count_documents({"guildid":str(ctx.guild.id),"image":1})
        if count ==1:
            embed = discord.Embed(color=discord.Colour.purple(),description="Welcome Image is already setup in your server.\nUse `>delwelcomeimage` to disable it and then use this cmd if you want a different welcome image!")
            return await ctx.send(embed=embed)
        
        #------text-replacer---------------
        count2 = await welcomedb.count_documents({"guildid":str(ctx.guild.id)})
        if count2 ==0:
            embed = discord.Embed(title="Step 1",color=discord.Colour.purple(),description="Enter channel where you want to setup welcome Image")
            msg = await ctx.send(embed=embed)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                channelinput = await self.client.wait_for("message", timeout=120, check=check)
            except:
                embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                await msg.edit(embed=embed)
                return
            try:
                channel = await commands.TextChannelConverter().convert(ctx, channelinput.content)
            except:
                embed = discord.Embed(color=discord.Colour.purple(),description="Invalid channel entered.\nPlease restart the process from beginning")
                return await ctx.send(embed=embed)
            embed = discord.Embed(title="Step 2",color=discord.Colour.purple(),description="Enter Preset Number.\n\nTo See the available presets type `>showwelcomepresets`")
            msg = await ctx.send(embed=embed)
            try:
                presetinput = await self.client.wait_for("message", timeout=120, check=check)
            except:
                embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                await msg.edit(embed=embed)
                return
            if presetinput.content not in ["1","2","3","4"]:
                embed = discord.Embed(colour = discord.Colour.purple(),description="<a:infernocross:844577707727388742> Invalid Preset Number entered.\nAcceptable Entries are 1, 2, 3 or 4")
                return await ctx.send(embed=embed)
            presetnumber = int(presetinput.content)
#--------------preset1-------------------------------------------------
            if presetnumber ==1:
                #-------image/png contenttype----------
                embed = discord.Embed(title="Step 3",colour=discord.Colour.purple(),description = "Would you like to go with the default background in this preset?\n\nType y/yes to use default background and n/no to use a custom background")
                file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset1.png", filename="preset1.png")
                embed.set_image(url="attachment://preset1.png")
                msg = await ctx.send(embed=embed,file=file)
                try:
                    bgtype = await self.client.wait_for("message", timeout=120, check=check)
                except:
                    embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                    await msg.edit(embed=embed)
                    return
                if bgtype.content.lower() in ['y','yes']:
#--------------------------------default bg--------------------------------------                    
                    embed = discord.Embed(title="Step 4",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 46 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>46:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 46")
                        return await ctx.send(embed=embed)
                    text= originaltext
                    #----fontcolour-----
                    embed = discord.Embed(title="Step 5",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.defaultpreset1, avatar,ctx.author,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#-------------------------embed------------
                    embed = discord.Embed(title="Step 6",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "no",
                            "imagetext": text,
                            "embedimage":"yes",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        #dbstuff
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "no",
                            "imagetext": text,
                            "embedimage":"no",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                        

                    return
#-----------------store in db--------------------                    
#------------------------add for custom fill colour--------------------
                elif bgtype.content.lower() in ['n',"no"]:
                    embed = discord.Embed(title = "Step 4",color=discord.Colour.purple(),description="Send the image which you want to set as background.")
                    embed.set_footer(text = "Recommended Size is 936x284 px")
                    msg = await ctx.send(embed=embed)
                    try:
                        message = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    #----check if attachment there or not and raise invalid input                
                    if len(message.attachments)==0:
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    if str(message.attachments[0].content_type)[:5] != "image":
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    data = BytesIO(await message.attachments[0].read())
                    im = Image.open(data)
                    image = im.copy()
                    im = make_RGBA(im)
                    embed = discord.Embed(title="Step 5",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 46 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>46:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 46")
                        return await ctx.send(embed=embed)
                    text= originaltext
                    #----fontcolour-----
                    embed = discord.Embed(title="Step 6",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.preset1, avatar,ctx.author,im,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#-------------------------------embed-------------------------
                    embed = discord.Embed(title="Step 7",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "yes",
                            "imagetext": text,
                            "embedimage":"yes",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        #dbstuff
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "yes",
                            "imagetext": text,
                            "embedimage":"no",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    return
#---------------preset2-------------
            if presetnumber ==2:
                #-------image/png contenttype----------
                embed = discord.Embed(title="Step 3",colour=discord.Colour.purple(),description = "Would you like to go with the default background in this preset?\n\nType y/yes to use default background and n/no to use a custom background")
                file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset2.png", filename="preset2.png")
                embed.set_image(url="attachment://preset2.png")
                msg = await ctx.send(embed=embed,file=file)
                try:
                    bgtype = await self.client.wait_for("message", timeout=120, check=check)
                except:
                    embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                    await msg.edit(embed=embed)
                    return
                if bgtype.content.lower() in ['y','yes']:
#--------------------------------default bg--------------------------------------                    
                    embed = discord.Embed(title="Step 4",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 99 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>99:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 99")
                        return await ctx.send(embed=embed)

                    #----fontcolour-----
                    embed = discord.Embed(title="Step 5",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    text= originaltext
                    fn = partial(self.defaultpreset2,ctx.author,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#--------------------------embed---------------------------
                    embed = discord.Embed(title="Step 6",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "no",
                            "imagetext": text,
                            "embedimage":"yes",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        #dbstuff
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "no",
                            "imagetext": text,
                            "embedimage":"no",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    return
#-----------------store in db--------------------                    
#------------------------add for custom fill colour--------------------
                elif bgtype.content.lower() in ['n',"no"]:
                    embed = discord.Embed(title = "Step 4",color=discord.Colour.purple(),description="Send the image which you want to set as background.")
                    embed.set_footer(text="Recommended Size is 936x284 px")
                    msg = await ctx.send(embed=embed)
                    try:
                        message = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    #----check if attachment there or not and raise invalid input                
                    if len(message.attachments)==0:
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    if str(message.attachments[0].content_type)[:5] != "image":
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    data = BytesIO(await message.attachments[0].read())
                    im = Image.open(data)
                    image = im.copy()
                    im = make_RGBA(im)
                    embed = discord.Embed(title="Step 5",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 99 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>99:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 99")
                        return await ctx.send(embed=embed)
                    text= originaltext
                    #----fontcolour-----
                    embed = discord.Embed(title="Step 6",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    fn = partial(self.preset2,ctx.author,im,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#------------------------------------embed------------------------
                    embed = discord.Embed(title="Step 7",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        #dbstuff
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "yes",
                            "imagetext": text,
                            "embedimage":"yes",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "yes",
                            "imagetext": text,
                            "embedimage":"no",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    return
#---------------preset3-----------
            if presetnumber ==3:
                #-------image/png contenttype----------
                embed = discord.Embed(title="Step 3",colour=discord.Colour.purple(),description = "Would you like to go with the default background in this preset?\n\nType y/yes to use default background and n/no to use a custom background")
                file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset3.png", filename="preset3.png")
                embed.set_image(url="attachment://preset3.png")
                msg = await ctx.send(embed=embed,file=file)
                try:
                    bgtype = await self.client.wait_for("message", timeout=120, check=check)
                except:
                    embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                    await msg.edit(embed=embed)
                    return
                if bgtype.content.lower() in ['y','yes']:
#--------------------------------default bg--------------------------------------                    
                    embed = discord.Embed(title="Step 4",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 46 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>46:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 46")
                        return await ctx.send(embed=embed)
                    text= originaltext
                    #----fontcolour-----
                    embed = discord.Embed(title="Step 5",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.defaultpreset3, avatar,ctx.author,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#-----------------------------embed-------------------------------------------------
                    embed = discord.Embed(title="Step 6",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "no",
                            "imagetext": text,
                            "embedimage":"yes",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "no",
                            "imagetext": text,
                            "embedimage":"no",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    return
#-----------------store in db--------------------                    
#------------------------add for custom fill colour--------------------
                elif bgtype.content.lower() in ['n',"no"]:
                    embed = discord.Embed(title = "Step 4",color=discord.Colour.purple(),description="Send the image which you want to set as background.")
                    embed.set_footer(text="Recommended Size is 936x284 px")
                    msg = await ctx.send(embed=embed)
                    try:
                        message = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    #----check if attachment there or not and raise invalid input                
                    if len(message.attachments)==0:
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    if str(message.attachments[0].content_type)[:5] != "image":
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    data = BytesIO(await message.attachments[0].read())
                    im = Image.open(data)
                    image=im.copy()
                    im = make_RGBA(im)
                    embed = discord.Embed(title="Step 5",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 46 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>46:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 46")
                        return await ctx.send(embed=embed)
                    text= originaltext
                    #----fontcolour-----
                    embed = discord.Embed(title="Step 6",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.preset3, avatar,ctx.author,im,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#---embed----------------------------------
                    embed = discord.Embed(title="Step 7",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        #dbstuff
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "yes",
                            "imagetext": text,
                            "embedimage":"yes",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "yes",
                            "imagetext": text,
                            "embedimage":"no",
                            "text":0,
                            "fontcolour":fontcolour.to_rgb(),
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return

                    return            

#----------preset4---(0,310), (1000,370)  ; (0,370), (1000,418)

            if presetnumber ==4:
                #-------image/png contenttype----------
                embed = discord.Embed(title="Step 3",colour=discord.Colour.purple(),description = "Would you like to go with the default background in this preset?\n\nType y/yes to use default background and n/no to use a custom background")
                file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset4alt.png", filename="preset4.png")
                embed.set_image(url="attachment://preset4.png")
                msg = await ctx.send(embed=embed,file=file)
                try:
                    bgtype = await self.client.wait_for("message", timeout=120, check=check)
                except:
                    embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                    await msg.edit(embed=embed)
                    return
                
                if bgtype.content.lower() in ['y','yes']:
                    
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.defaultpreset4, avatar,ctx.author)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#---------do embed part----------         
                    embed = discord.Embed(title="Step 4",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "no",
                            "embedimage":"yes",
                            "text":0,
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                        
                    elif embedcheck.content.lower() in ['n','no']:
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "no",
                            "embedimage":"no",
                            "text":0,
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return


                    return


                elif bgtype.content.lower() in ['n','no']:
                    embed = discord.Embed(title = "Step 4",color=discord.Colour.purple(),description="Send the image which you want to set as background.")
                    embed.set_footer(text="Recommended Size is 1000x450 px")
                    msg = await ctx.send(embed=embed)
                    try:
                        message = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    #----check if attachment there or not and raise invalid input                
                    if len(message.attachments)==0:
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    if str(message.attachments[0].content_type)[:5] != "image":
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    data = BytesIO(await message.attachments[0].read())
                    im = Image.open(data)
                    image = im.copy()
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.preset4, avatar,ctx.author,im)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
                    
                    embed = discord.Embed(title="Step 5",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "yes",
                            "embedimage":"yes",
                            "text":0,

                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        info ={
                            "guildid":str(ctx.guild.id),
                            "image" : 1,
                            "preset":presetnumber,
                            "custom" : "yes",
                            "embedimage":"no",
                            "text":0,
                            "channelid" : str(channel.id)
                        }
                        await welcomedb.insert_one(info)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in {channel.mention}")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return

                    return            

#-------------------------------------------------------------------------------------------
#--------------------------count2!=0-----------------------------------------------
#-------------------------------------------------------------------------------------------
        else:
            embed = discord.Embed(title="Step 1",color=discord.Colour.purple(),description="Enter Preset Number.\n\nTo See the available presets type `>showwelcomepresets`")
            msg = await ctx.send(embed=embed)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                presetinput = await self.client.wait_for("message", timeout=120, check=check)
            except:
                embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                await msg.edit(embed=embed)
                return
            if presetinput.content not in ["1","2","3","4"]:
                embed = discord.Embed(colour = discord.Colour.purple(),description="<a:infernocross:844577707727388742> Invalid Preset Number entered.\nAcceptable Entries are 1, 2, 3 or 4")
                return await ctx.send(embed=embed)
            presetnumber = int(presetinput.content)
#--------------preset1-------------------------------------------------
            if presetnumber ==1:
                #-------image/png contenttype----------
                embed = discord.Embed(title="Step 2",colour=discord.Colour.purple(),description = "Would you like to go with the default background in this preset?\n\nType y/yes to use default background and n/no to use a custom background")
                file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset1.png", filename="preset1.png")
                embed.set_image(url="attachment://preset1.png")
                msg = await ctx.send(embed=embed,file=file)
                try:
                    bgtype = await self.client.wait_for("message", timeout=120, check=check)
                except:
                    embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                    await msg.edit(embed=embed)
                    return
                if bgtype.content.lower() in ['y','yes']:
#--------------------------------default bg--------------------------------------                    
                    embed = discord.Embed(title="Step 3",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 46 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>46:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 46")
                        return await ctx.send(embed=embed)
                    text= originaltext
                    #----fontcolour-----
                    embed = discord.Embed(title="Step 4",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.defaultpreset1, avatar,ctx.author,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#-------------------------embed------------
                    embed = discord.Embed(title="Step 5",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "no"
                        data['imagetext'] = text
                        data['embedimage']= "yes"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return

                    elif embedcheck.content.lower() in ['n','no']:
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "no"
                        data['imagetext'] = text
                        data['embedimage']= "no"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    return
#-----------------store in db--------------------                    
#------------------------add for custom fill colour--------------------
                elif bgtype.content.lower() in ['n',"no"]:
                    embed = discord.Embed(title = "Step 3",color=discord.Colour.purple(),description="Send the image which you want to set as background.")
                    embed.set_footer(text = "Recommended Size is 936x284 px")
                    msg = await ctx.send(embed=embed)
                    try:
                        message = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    #----check if attachment there or not and raise invalid input                
                    if len(message.attachments)==0:
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    if str(message.attachments[0].content_type)[:5] != "image":
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    data = BytesIO(await message.attachments[0].read())
                    im = Image.open(data)
                    image = im.copy()
                    im = make_RGBA(im)
                    embed = discord.Embed(title="Step 4",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 46 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>46:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 46")
                        return await ctx.send(embed=embed)
                    text= originaltext
                    #----fontcolour-----
                    embed = discord.Embed(title="Step 5",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.preset1, avatar,ctx.author,im,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#-------------------------------embed-------------------------
                    embed = discord.Embed(title="Step 6",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "yes"
                        data['imagetext'] = text
                        data['embedimage']= "yes"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "yes"
                        data['imagetext'] = text
                        data['embedimage']= "no"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    return
#---------------preset2-------------
            if presetnumber ==2:
                #-------image/png contenttype----------
                embed = discord.Embed(title="Step 2",colour=discord.Colour.purple(),description = "Would you like to go with the default background in this preset?\n\nType y/yes to use default background and n/no to use a custom background")
                file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset2.png", filename="preset2.png")
                embed.set_image(url="attachment://preset2.png")
                msg = await ctx.send(embed=embed,file=file)
                try:
                    bgtype = await self.client.wait_for("message", timeout=120, check=check)
                except:
                    embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                    await msg.edit(embed=embed)
                    return
                if bgtype.content.lower() in ['y','yes']:
#--------------------------------default bg--------------------------------------                    
                    embed = discord.Embed(title="Step 3",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 99 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>99:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 99")
                        return await ctx.send(embed=embed)
                    text= originaltext
                    #----fontcolour-----
                    embed = discord.Embed(title="Step 4",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    fn = partial(self.defaultpreset2,ctx.author,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#--------------------------embed---------------------------
                    embed = discord.Embed(title="Step 5",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "no"
                        data['imagetext'] = text
                        data['embedimage']= "yes"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "no"
                        data['imagetext'] = text
                        data['embedimage']= "no"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    return
#-----------------store in db--------------------                    
#------------------------add for custom fill colour--------------------
                elif bgtype.content.lower() in ['n',"no"]:
                    embed = discord.Embed(title = "Step 3",color=discord.Colour.purple(),description="Send the image which you want to set as background.")
                    embed.set_footer(text="Recommended Size is 936x284 px")
                    msg = await ctx.send(embed=embed)
                    try:
                        message = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    #----check if attachment there or not and raise invalid input                
                    if len(message.attachments)==0:
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    if str(message.attachments[0].content_type)[:5] != "image":
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    data = BytesIO(await message.attachments[0].read())
                    im = Image.open(data)
                    image = im.copy()
                    im = make_RGBA(im)
                    embed = discord.Embed(title="Step 4",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 99 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>99:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 99")
                        return await ctx.send(embed=embed)
                    text= originaltext
                    #----fontcolour-----
                    embed = discord.Embed(title="Step 5",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    fn = partial(self.preset2,ctx.author,im,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#------------------------------------embed------------------------
                    embed = discord.Embed(title="Step 6",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "yes"
                        data['imagetext'] = text
                        data['embedimage']= "yes"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "yes"
                        data['imagetext'] = text
                        data['embedimage']= "no"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    return
#---------------preset3-----------
            if presetnumber ==3:
                #-------image/png contenttype----------
                embed = discord.Embed(title="Step 2",colour=discord.Colour.purple(),description = "Would you like to go with the default background in this preset?\n\nType y/yes to use default background and n/no to use a custom background")
                file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset3.png", filename="preset3.png")
                embed.set_image(url="attachment://preset3.png")
                msg = await ctx.send(embed=embed,file=file)
                try:
                    bgtype = await self.client.wait_for("message", timeout=120, check=check)
                except:
                    embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                    await msg.edit(embed=embed)
                    return
                if bgtype.content.lower() in ['y','yes']:
#--------------------------------default bg--------------------------------------                    
                    embed = discord.Embed(title="Step 3",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 46 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>46:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 46")
                        return await ctx.send(embed=embed)
                    text= originaltext
                    #----fontcolour-----
                    embed = discord.Embed(title="Step 4",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.defaultpreset3, avatar,ctx.author,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#-----------------------------embed-------------------------------------------------
                    embed = discord.Embed(title="Step 5",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                    
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "no"
                        data['imagetext'] = text
                        data['embedimage']= "yes"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "no"
                        data['imagetext'] = text
                        data['embedimage']= "no"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    return
#-----------------store in db--------------------                    
#------------------------add for custom fill colour--------------------
                elif bgtype.content.lower() in ['n',"no"]:
                    embed = discord.Embed(title = "Step 3",color=discord.Colour.purple(),description="Send the image which you want to set as background.")
                    embed.set_footer(text="Recommended Size is 936x284 px")
                    msg = await ctx.send(embed=embed)
                    try:
                        message = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    #----check if attachment there or not and raise invalid input                
                    if len(message.attachments)==0:
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    if str(message.attachments[0].content_type)[:5] != "image":
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    data = BytesIO(await message.attachments[0].read())
                    im = Image.open(data)
                    image = im.copy()
                    im = make_RGBA(im)
                    embed = discord.Embed(title="Step 4",colour=discord.Colour.purple(),description = '''Enter the text which you want to add to the image (it should be of max 46 letters)\n
```q
Available Tags:- 
"{username}" - display users username with his discriminator

"{server}" - displays server name. `The number of characters for this tag will be counted as in the server name`

"{membercount}" - shows the member count of the server(including bots). `Example: Welcome {username}. You are the {membercount}{membercount.ordinal} user!` here {membercount.ordinal} tag will be considered as 2 chars and {membercount} as 3 chars, same with other similar 5 tags

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
                    msg = await ctx.send(embed=embed)
                    try:
                        textinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    text = textinput.content
                    originaltext = text
                    text = text.replace('{server}',f"{ctx.guild.name}")
                    text = text.replace("{membercount}",f"123")
                    text = text.replace("{botcount}",f"123")
                    text = text.replace("{humancount}",f"123")
                    text = text.replace("{membercount.ordinal}",f"12")
                    text = text.replace("{humancount.ordinal}",f"12")
                    text = text.replace("{botcount.ordinal}",f"12")
                    if len(text)>46:
                        embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Number of characters in the text should be max 46")
                        return await ctx.send(embed=embed)
                    text= originaltext
                    #----fontcolour-----
                    embed = discord.Embed(title="Step 5",color=discord.Colour.purple(),description='''**Enter Font Colour**

The following formats are accepted:
`0x<hex>`

`#<hex>`

`0x#<hex>`

`rgb(<number>, <number>, <number>)`''')
                    msg = await ctx.send(embed=embed)
                    try:
                        fontcolourinput = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    try:
                        fontcolour = await commands.ColourConverter().convert(ctx, fontcolourinput.content)
                    except:
                        embed = discord.Embed(color=discord.Colour.purple(),description="Invalid Font Colour entered.\nPlease restart the process from beginning")
                        return await ctx.send(embed=embed)
                    #----fn calling
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.preset3, avatar,ctx.author,im,text,fontcolour.to_rgb())
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#---embed----------------------------------
                    embed = discord.Embed(title="Step 6",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "yes"
                        data['imagetext'] = text
                        data['embedimage']= "yes"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "yes"
                        data['imagetext'] = text
                        data['embedimage']= "no"
                        data["fontcolour"]=fontcolour.to_rgb()
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return


                    return            

#----------preset4---(0,310), (1000,370)  ; (0,370), (1000,418)

            if presetnumber ==4:
                #-------image/png contenttype----------
                embed = discord.Embed(title="Step 2",colour=discord.Colour.purple(),description = "Would you like to go with the default background in this preset?\n\nType y/yes to use default background and n/no to use a custom background")
                file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset4alt.png", filename="preset4.png")
                embed.set_image(url="attachment://preset4.png")
                msg = await ctx.send(embed=embed,file=file)
                try:
                    bgtype = await self.client.wait_for("message", timeout=120, check=check)
                except:
                    embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                    await msg.edit(embed=embed)
                    return
                
                if bgtype.content.lower() in ['y','yes']:
                    
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.defaultpreset4, avatar,ctx.author)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
#---------do embed part----------         
                    embed = discord.Embed(title="Step 3",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "no"
                        data['embedimage']= "yes"
                        
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                        
                    elif embedcheck.content.lower() in ['n','no']:
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "no"
                        data['embedimage']= "no"
                        
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return


                    return


                elif bgtype.content.lower() in ['n','no']:
                    embed = discord.Embed(title = "Step 3",color=discord.Colour.purple(),description="Send the image which you want to set as background.")
                    embed.set_footer(text="Recommended Size is 1000x450 px")
                    msg = await ctx.send(embed=embed)
                    try:
                        message = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    #----check if attachment there or not and raise invalid input                
                    if len(message.attachments)==0:
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    if str(message.attachments[0].content_type)[:5] != "image":
                        embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You should have sent an image")
                        return await ctx.send(embed=embed)
                    data = BytesIO(await message.attachments[0].read())
                    im = Image.open(data)
                    image = im.copy()   
                    avatar = await make_avatar(ctx.author)
                    fn = partial(self.preset4, avatar,ctx.author,im)
                    outfile = await self.client.loop.run_in_executor(None, fn)
                    await ctx.send("Here is a preview of how the welcome image will look",file=discord.File(outfile))
                    os.remove(outfile)
                    
                    embed = discord.Embed(title="Step 4",colour=discord.Colour.purple(),description = "Do you want to send the image inside an embed?\nReply with y/yes or n/no")
                    msg = await ctx.send(embed=embed)
                    try:
                        embedcheck = await self.client.wait_for("message", timeout=120, check=check)
                    except:
                        embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
                        await msg.edit(embed=embed)
                        return
                    
                    if embedcheck.content.lower() in ['y','yes']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "yes"
                        data['embedimage']= "yes"
                        
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return
                    elif embedcheck.content.lower() in ['n','no']:
                        image.save(f"/home/pranav/Inferno/Inferno/cogs/welcome/guildimages/{ctx.guild.id}.png")
                        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
                        data['image'] = 1
                        data['preset']= presetnumber
                        data['custom']= "yes"
                        data['embedimage']= "no"
                        
                        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
                        embed = discord.Embed(color = discord.Colour.purple(),description=f"Welcome image has been setup successfully in <#{data['channelid']}>")
                        await ctx.send(embed=embed)
                        #dbstuff
                        return

                    return            

            return        

#-----------make sample preview and also recommended size in footer
    @commands.command()
    async def showwelcomepresets(self,ctx,presetnumber:int = 1):
        pagenumber = presetnumber
        if pagenumber <1 or pagenumber>4:
            embed = discord.Embed(colour= discord.Colour.purple(),description = "<a:infernocross:844577707727388742> Preset number should be between 1 and 4")
            return await ctx.send(embed=embed)
        if pagenumber==1:
            file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset1preview.png", filename="preset1.png")
            embed = discord.Embed(title = "Preset 1",colour=discord.Colour.purple())
            embed.set_image(url="attachment://preset1.png")
            embed.set_footer(text = "Preset 1/4 . Use >showwelcomepresets [presetnumber] to view all the available presets!!")
            return await ctx.send(embed=embed,file=file)
        elif pagenumber ==2 :
            file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset2preview.png", filename="preset2.png")
            embed = discord.Embed(title = "Preset 2",colour=discord.Colour.purple())
            embed.set_image(url="attachment://preset2.png")
            embed.set_footer(text = "Preset 2/4 . Use >showwelcomepresets [presetnumber] to view all the available presets!!")
            return await ctx.send(embed=embed,file=file)
        elif presetnumber==3:
            file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset3preview.png", filename="preset3.png")
            embed = discord.Embed(title = "Preset 3",colour=discord.Colour.purple())
            embed.set_image(url="attachment://preset3.png")
            embed.set_footer(text = "Preset 3/4 . Use >showwelcomepresets [presetnumber] to view all the available presets!!")
            return await ctx.send(embed=embed,file=file)
        else:
            file = discord.File("/home/pranav/Inferno/Inferno/cogs/welcome/preset4preview.png", filename="preset4.png")
            embed = discord.Embed(title = "Preset 4",colour=discord.Colour.purple())
            embed.set_image(url="attachment://preset4.png")
            embed.set_footer(text = "Preset 4/4 . Use >showwelcomepresets [presetnumber] to view all the available presets!!")
            return await ctx.send(embed=embed,file=file)


    @commands.command(description="Removes Welcome System from the Server")
    @commands.has_permissions(manage_guild = True)
    async def delwelcome(self,ctx):
        count = await welcomedb.count_documents({"guildid":str(ctx.guild.id)})
        if count ==0:
            embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You don't have welcome system setup in your server")
            return await ctx.send(embed=embed)
        await welcomedb.delete_many({"guildid":str(ctx.guild.id)})
        embed = discord.Embed(description="Removed Welcome System from your server <a:tick:844553824991313961>",color = discord.Colour.purple())
        return await ctx.send(embed = embed)


    @commands.command(description="Removes Welcome Text from the Server")
    @commands.has_permissions(manage_guild = True)
    async def delwelcometext(self,ctx):
               
        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
        if data is None:
            embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You don't have welcome system setup in your server")
            return await ctx.send(embed=embed)
        if data['text'] ==0:
            embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You need to set welcome text before trying to delete it")
            return await ctx.send(embed=embed)
        if data['image']==0:
            await welcomedb.delete_many({"guildid":str(ctx.guild.id)})
            embed = discord.Embed(description="Removed Welcome Text from your server <a:tick:844553824991313961>",color = discord.Colour.purple())
            return await ctx.send(embed = embed)
        try:
            data.pop(textoutput)
        except:
            pass
        data['text'] = 0 
        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
        embed = discord.Embed(description="Removed Welcome Text from your server <a:tick:844553824991313961>",color = discord.Colour.purple())
        return await ctx.send(embed = embed)


    @commands.command(description="Removes Welcome Image from the Server")
    @commands.has_permissions(manage_guild = True)
    async def delwelcomeimage(self,ctx):
               
        data = await welcomedb.find_one({"guildid":str(ctx.guild.id)})
        if data is None:
            embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You don't have welcome system setup in your server")
            return await ctx.send(embed=embed)
        if data['image'] ==0:
            embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You need to set welcome image before trying to delete it")
            return await ctx.send(embed=embed)
        if data['text']==0:
            await welcomedb.delete_many({"guildid":str(ctx.guild.id)})
            embed = discord.Embed(description="Removed Welcome Image from your server <a:tick:844553824991313961>",color = discord.Colour.purple())
            return await ctx.send(embed = embed)
        try:
            data.pop(preset)
        except:
            pass
        try:
            data.pop(custom)
        except:
            pass
        try:
            data.pop(imagetext)
        except:
            pass
        try:
            data.pop(embedimage)
        except:
            pass
        try:
            data.pop(fontcolour)
        except:
            pass
        data['image'] = 0 
        await welcomedb.replace_one({"guildid":str(ctx.guild.id)},data)
        embed = discord.Embed(description="Removed Welcome Image from your server <a:tick:844553824991313961>",color = discord.Colour.purple())
        return await ctx.send(embed = embed)

#-----------------leave----------------------------------------------------------------------------------------
    @commands.command(aliases = ['slt',"setleavetext","setfarewell"],description="Sets Farewell Text in the Server. (Text which is sent when a user leaves the server)")
    @commands.has_permissions(manage_guild=True)
    async def setfarewelltext(self,ctx):
        count = await leavedb.count_documents({"guildid":str(ctx.guild.id)})
        if count !=0:
            embed = discord.Embed(color=discord.Colour.purple(),description="Farewell/Leave text is already setup in your server.\nUse `>delfarewell` to disable it and use this cmd again if you want to change the farewell text")
            return await ctx.send(embed=embed)
        
        #------text-replacer---------------
        embed = discord.Embed(title="Step 1",color=discord.Colour.purple(),description="Enter channel where you want to setup Farewell Text")
        msg = await ctx.send(embed=embed)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            channelinput = await self.client.wait_for("message", timeout=120, check=check)
        except:
            embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
            await msg.edit(embed=embed)
            return
        try:
            channel = await commands.TextChannelConverter().convert(ctx, channelinput.content)
        except:
            embed = discord.Embed(color=discord.Colour.purple(),description="Invalid channel entered.\nPlease restart the process from beginning")
            return await ctx.send(embed=embed)
        embed = discord.Embed(title="Step 2",color=discord.Colour.purple(),description='''Enter the Farewell text which will be sent when a member leaves the server.\n\n```q
Available Tags:- 

"{user}" - mentions the user.

"{username}" - display users username with his discriminator

"{server}" - displays server name.

"{membercount}" - shows the member count of the server(including bots). `Example: {user} left :( ! We now have {membercount} users left in the server.`

"{humancount}" - shows the member count of the server(only humans).

"{botcount}" - shows the number of bots in the server.

"{membercount.ordinal}" - ordinal number (st, nd, rd, th) for member count.

"{humancount.ordinal}" - ordinal number (st, nd, rd, th) for humans count.

"{botcount.ordinal}" - ordinal number (st, nd, rd, th) for bots count.```''')
        msg = await ctx.send(embed=embed)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            textinput = await self.client.wait_for("message", timeout=120, check=check)
        except:
            embed = discord.Embed(colour=discord.Colour.purple(), description="Request Timed Out")
            await msg.edit(embed=embed)
            return
        text = textinput.content

        info ={
                "guildid":str(ctx.guild.id),
                "textoutput":text,
                "channelid" : str(channel.id)
            }
        await leavedb.insert_one(info)
        embed = discord.Embed(color = discord.Colour.purple(),description=f"Farewell text has been setup successfully in {channel.mention}")
        await ctx.send(embed=embed)
        return

    @commands.command(description="Removes Farewell Text System from the Server",aliases= ['delleave','delfarewelltext'])
    @commands.has_permissions(manage_guild = True)
    async def delfarewell(self,ctx):
        count = await leavedb.count_documents({"guildid":str(ctx.guild.id)})
        if count ==0:
            embed = discord.Embed(color=discord.Colour.purple(),description="<a:infernocross:844577707727388742> You don't have Farewell Text setup in your server")
            return await ctx.send(embed=embed)
        await leavedb.delete_many({"guildid":str(ctx.guild.id)})
        embed = discord.Embed(description="Removed Farewell Text System from your server <a:tick:844553824991313961>",color = discord.Colour.purple())
        return await ctx.send(embed = embed)



async def setup(client):
  await client.add_cog(Welcome(client))
