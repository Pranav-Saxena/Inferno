'''
Reaction Roles
'''
import discord
from discord.ext import commands
import json
import asyncio
import re
import motor.motor_asyncio
import nest_asyncio
import datetime
import os
import time
import emojis
nest_asyncio.apply()
cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb_cluster_auth")
reactionroles = cluster["rr"]["rr"]

class rr(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="starts the creation of reaction roles")
    @commands.has_permissions(manage_roles=True)
    async def rrcreate(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel.id == ctx.channel.id
        embed1 = discord.Embed(title="Step 1",colour=discord.Colour.purple(),description=f"Alright! Let's set up your reactionroles! Let's find your message on which you want to create reaction role\nYou can type `exit` at any time to cancel creation.\n\n`Enter the message link on which you want reaction roles to be set up (The Message should be in this server only)`")
        # await ctx.send("Alright! Let's set up your reactionroles! Let's find your message on which you want to create reaction role\nYou can type `exit` at any time to cancel creation.\n\n`Enter the message link on which you want reaction roles to be set up (The Message should be in this server only)`")
        await ctx.send(embed=embed1)
        try:
            messagelink = await self.client.wait_for("message",check=check,timeout=120)
        except:
            embedtimeout = discord.Embed(title = "Reaction Roles Creation Timed Out",colour=discord.Colour.purple(),description=f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles creation is cancelled`")
            return await ctx.send(embed = embedtimeout)
            # return await ctx.send(f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n `Reaction roles creation is cancelled`")

        if messagelink.content.lower()=="exit":
            embedexit = discord.Embed(colour=discord.Colour.purple())
            embedexit.set_author(name ="Alright! Seems we are not setting up reaction roles anymore.")
            return await ctx.send(embed = embedexit)
        # print(response)
#         if response.content == "yes":
#             await ctx.send("Sweet! Let's move to the next step! Let's find your message on which you want to create reaction role\n\n`Enter the message link on which you want reaction roles to be set up (The Message should be in this server only)`")
# #await commands.MessageConverter().convert(ctx, messagelink)

        # messagelink = await self.client.wait_for('message', check=check,timeout=60)
#--------create timeout error-----------
        #--- create for exit response
        try:
            message = await commands.MessageConverter().convert(ctx, messagelink.content)
        except Exception as e:
            embednotfound = discord.Embed(colour=discord.Colour.purple())
            embednotfound.set_author(name ="Uh ho! Message not found . Pls restart the process and provide a correct link next time")
            await ctx.send(embed = embednotfound)
            return
        try:
            all = reactionroles.find({})
        except:
            pass
        async for x in all:
            if x["messageid"] == str(message.id):
                embedexisting = discord.Embed(colour=discord.Colour.purple(),description="Uh ho! The message already has reaction roles set up on it.\nYou can use `>rrdelete` command to remove reaction roles from that message or `>rrupdate` to update the existing reaction roles on the message")
                return await ctx.send(embed = embedexisting)
        embed2 = discord.Embed(title="Step 2",colour=discord.Colour.purple(),description='Sweet! Now tell me the number of reaction roles u want \n`The no. should be less than 20`\n`Alternatively, If you want more reaction roles you can start this process again with another message`')
        await ctx.send(embed = embed2)
        try:
            num = await self.client.wait_for('message', check=check,timeout =120)
        except:
            embedtimeout = discord.Embed(title = "Reaction Roles Creation Timed Out",colour=discord.Colour.purple(),description=f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles creation is cancelled`")
            return await ctx.send(embed = embedtimeout)
            # return await ctx.send(f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles creation is cancelled`")
        if num.content.lower()=="exit":
            embedexit = discord.Embed(colour=discord.Colour.purple())
            embedexit.set_author(name="Alright! Seems we are not setting up reaction roles anymore.")
            return await ctx.send(embed = embedexit)
            # return await ctx.send("Alright! Seems we are not setting up reaction roles anymore.")
        if not num.content.isdigit():
            embednotdig = discord.Embed(colour=discord.Colour.purple())
            embednotdig.set_author(name = 'Uh ho! You should have entered a number \nPlease restart the process from the beginning')
            return await ctx.send(embed = embednotdig)
        elif int(num.content)<1 or int(num.content)>20:
            embednotrange = discord.Embed(colour=discord.Colour.purple())
            embednotrange.set_author(name = "The no. should had been between 1 and 20")
            return await ctx.send(embed = embednotrange)
        else:
            data = {}
            count = 1
            excep = 0
            dict = {"0": "th", "1": "st", "2": "nd", "3": "rd", "4": "th", "5": "th", "6": "th", "7": "th",
                        "8": "th", "9": "th"}
            for j in range(int(num.content)):
                embed3A = discord.Embed(title="Step 3A",colour=discord.Colour.purple(),description=f'Send an emoji for the {count}{dict[str(count)[-1]]} reaction role')
                await ctx.send(embed = embed3A)
                try:
                    emojiinput = await self.client.wait_for('message', check=check,timeout=120)
                except:
                    embedtimeout = discord.Embed(title="Reaction Roles Creation Timed Out",
                                                 colour=discord.Colour.purple(),
                                                 description=f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles creation is cancelled`")
                    return await ctx.send(embed=embedtimeout)
                    # return await ctx.send(f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles creation is cancelled`")
                if emojiinput.content.lower() == "exit":
                    embedexit = discord.Embed(colour=discord.Colour.purple())
                    embedexit.set_author(name="Alright! Seems we are not setting up reaction roles anymore.")
                    return await ctx.send(embed = embedexit)
                    # return await ctx.send("Alright! Seems we are not setting up reaction roles anymore.")
                try:
                    emoji = await commands.EmojiConverter().convert(ctx,emojiinput.content)
                except:
                    try:
                        checkunicode = emojis.get(emojiinput.content[0])
                        if len(checkunicode) !=0:
                            emoji = emojiinput.content[0]
                        else:
                            raise commands.CommandError
                    except:

                        embedinvalidemoji = discord.Embed(colour=discord.Colour.purple())
                        embedinvalidemoji.set_author(name ="Invalid emoji. Ignoring Input" )
                        await ctx.send(embed = embedinvalidemoji)
                        count +=1
                        excep +=1
                        continue
                # try:
                #     await message.add_reaction(str(emoji))
                # except:
                #     return await ctx.send('An emoji should have been sent...')
                if str(emoji) in data:
                    embedrrexists = discord.Embed(colour=discord.Colour.purple())
                    embedrrexists.set_author(name = "Reaction role for that emoji already created. Ignoring this input!")
                    count +=1
                    excep+=1
                    await ctx.send(embed = embedrrexists)
                    continue

                embed3B = discord.Embed(title = "Step 3B",colour=discord.Colour.purple(),description='Send the Role id or mention the role which will be assigned by reacting with {}'.format(emoji))
                await ctx.send(embed = embed3B)
                try:
                    role_id = await self.client.wait_for('message', check=check,timeout=120)
                except:
                    embedtimeout = discord.Embed(title="Reaction Roles Creation Timed Out",
                                                 colour=discord.Colour.purple(),
                                                 description=f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles creation is cancelled`")
                    return await ctx.send(embed=embedtimeout)
                    # return await ctx.send(f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n `Reaction roles creation is cancelled`")
                if role_id.content.lower() == "exit":
                    embedexit = discord.Embed(colour=discord.Colour.purple())
                    embedexit.set_author(name="Alright! Seems we are not setting up reaction roles anymore.")
                    return await ctx.send(embed = embedexit)
                    # return await ctx.send("Alright! Seems we are not setting up reaction roles anymore.")
                role_id=role_id.content
                role_id = role_id.replace("<","")
                role_id = role_id.replace(">", "")
                role_id = role_id.replace("@", "")
                role_id = role_id.replace("&", "")
                role_id = role_id.replace("!", "")
                if not role_id.isdigit():
                    embedroleinvalid = discord.Embed(colour=discord.Colour.purple())
                    embedroleinvalid.set_author(name = 'Invalid Role . Ignore this input!')
                    await ctx.send(embed = embedroleinvalid)
                    count+=1
                    excep +=1
                    continue
                try:
                    role = ctx.guild.get_role(int(role_id))
                    if role.position > ctx.author.top_role.position and not ctx.author == ctx.guild.owner:
                        embedrolepos = discord.Embed(colour=discord.Colour.purple())
                        embedrolepos.set_author(name = 'The role is higher than your current role. Ignoring this input')
                        await ctx.send(embed = embedrolepos)
                        count+=1
                        excep +=1
                        continue
                    if role.position >= ctx.guild.me.top_role.position:
                        embedbotrolepos = discord.Embed(colour=discord.Colour.purple())
                        embedbotrolepos.set_author(name = 'The role higher than my top role. Ignoring this input')
                        await ctx.send(embed = embedbotrolepos)
                        count +=1
                        excep +=1
                        continue
                except:
                    embedroleinv = discord.Embed(colour=discord.Colour.purple())
                    embedroleinv.set_author(name = 'Invalid Role. Ignoring this input')
                    await ctx.send(embed = embedroleinv)
                    count +=1
                    excep +=1
                    continue

                data[str(emoji)] = role.id

                count += 1
            finaldata = {}
            bool = 1
            boolcounter = 0
            if (count-1) == excep:
                embedallinc = discord.Embed(colour=discord.Colour.purple())
                embedallinc.set_author(name = "Reaction roles haven't been setup on the message because all the inputs were incorrect.")
                return await ctx.send(embed = embedallinc)
            else:
                for q in data.keys():
                    try:
                        await message.add_reaction(q)
                        finaldata[str(q)] = data[q]
                        boolcounter+=1
                    except:
                        embedissue = discord.Embed(colour=discord.Colour.purple())
                        embedissue.set_author(name = f"Issue Occured while reacting to the message since the emoji {q}.\nThis issue might have occured because there were already 20 reactions on that message or i don't have permissions to add reaction. \n\nIf you feel this error wouldn't have occured, join my support server and ask it there\nhttps://discord.com/invite/tTr6DvyRCH.")
                        await ctx.send(embed = embedissue)
                        bool = 0
                        breakemoji = q
                        break

                if bool ==0 and boolcounter!=0:
                    embednotreact = discord.Embed(colour=discord.Colour.purple())
                    embednotreact.set_author(name = "Reaction roles haven't been setup on the message because i wasn't able to react with even 1 emoji because of the issue occured")
                    return await ctx.send(embed = embednotreact)
                elif bool == 0 and boolcounter!=0:
                    embedpartialsetup = discord.Embed(colour=discord.Colour.purple(),title = "Reaction Roles - Setup Done",description=f"Done! Reaction roles have been setup till {breakemoji} emoji (not included) because of the error occured while reacting.\nYou can use `>rrupdate` to add more reactions if you want after fixing the cause of the error")
                    await ctx.send(embed = embedpartialsetup)
                else:
                    if excep !=0:
                        embedsend1 = discord.Embed(title = "Reaction Roles - Setup Done",colour=discord.Colour.purple(),description=f"Perfect! The reaction roles have been setup and {excep} invalid inputs were ignored.  Go check it out {messagelink.content}")
                        await ctx.send(embed = embedsend1)
                    else:
                        embedsend2 = discord.Embed(title = "Reaction Roles - Setup Done",colour=discord.Colour.purple(),description=f"Perfect! The reaction roles have been setup. Go check it out {messagelink.content}")
                        await ctx.send(embed = embedsend2)
                # print(data)

                rinfo = {
                        "guildid" : str(ctx.guild.id),
                        "messageid":str(message.id),
                        "data":finaldata,
                        "messagelink":str(messagelink.content)
                    }
                await reactionroles.insert_one(rinfo)
                return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            all = reactionroles.find({})

            async for x in all:

                if x["messageid"]==str(payload.message_id):

                    data = x["data"]

                    for i in data.keys():
                        if str(payload.emoji) == str(i):
                            guild = self.client.get_guild(payload.guild_id)
                            role = guild.get_role(int(data[i]))
                            await payload.member.add_roles(role)
                            embed = discord.Embed(title= "Role Added",colour=discord.Colour.purple(),description=f"You have got the `{role.name}` role by reacting in {guild.name}")
                            embed.set_footer(text = "Made by PRANAV SAXENA#9327 • dsc.gg/infernocommunity")
                            await payload.member.send(embed=embed)
                            break
                        else:
                            continue
        except:
            pass
        return
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        all = reactionroles.find({})
        async for x in all:
            if x["messageid"] == str(payload.message_id):
                data = x["data"]
                for i in data.keys():
                    try:
                        if str(i)[1] =="a":
                            tempi = "<"+ str(i)[2:]
                        else:
                            tempi = i
                    except:
                        tempi = i
                    if str(payload.emoji) == str(tempi):
                        guild = self.client.get_guild(payload.guild_id)
                        role = guild.get_role(int(data[i]))
                        # print(payload.member)
                        member = guild.get_member(payload.user_id)
                        await member.remove_roles(role)
                        embed = discord.Embed(title="Role Removed", colour=discord.Colour.purple(),
                                                  description=f"You have got the `{role.name}` role removed by unreacting in {guild.name}")
                        embed.set_footer(text="Made by PRANAV SAXENA#9327 • dsc.gg/infernocommunity")
                        await member.send(embed=embed)
                        break
                    else:
                        continue

        return

    @commands.command(description= "removes all reaction roles from the message")
    @commands.has_permissions(manage_roles=True)
    async def rrdelete(self, ctx, messagelink=None):
        if messagelink is None:
            embed = discord.Embed(colour=discord.Colour.purple(),description='Pls try again by entering the message link')
            return await ctx.send(embed = embed)
        try:
            message = await commands.MessageConverter().convert(ctx, messagelink)
        except Exception as e:
            embed = discord.Embed(colour=discord.Colour.purple(),description="Uh ho! Message not found . Pls try again and provide a correct link next time")
            await ctx.send(embed = embed)
            return
        all = reactionroles.find({})
        checker = 0
        async for i in all:
            if i["messageid"] == str(message.id):
                checker =1
                await reactionroles.delete_one(i)
                embed = discord.Embed(colour=discord.Colour.purple(),description="Reaction roles removed successfully from the message")
                await ctx.send(embed = embed)
                return
        if checker !=0:
            embed = discord.Embed(colour=discord.Colour.purple(),description="The message doesn't have reaction roles setup on it. Use `>rrcreate` command to setup reaction roles on that message first")
            return await ctx.send(embed = embed)
    @commands.command(description= "delete or add reaction roles in a message. ")
    @commands.has_permissions(manage_roles = True)
    async def rrupdate(self,ctx, messagelink = None):
        def check(m):
            return m.author == ctx.author and m.channel.id == ctx.channel.id
        if messagelink is None:
            embedwrongarg = discord.Embed(colour=discord.Colour.purple(),description='Pls try again by entering the message link')
            return await ctx.send(embed = embedwrongarg)
        try:
            message = await commands.MessageConverter().convert(ctx,messagelink)
        except Exception as e:
            embedmsgnotfound = discord.Embed(colour=discord.Colour.purple(),description="Uh ho! Message not found . Pls try again and provide a correct link next time")
            await ctx.send(embed = embedmsgnotfound)
            return
        all = reactionroles.find({})
        checker= 0
        async for x in all:
            if x["messageid"] == str(message.id):
                print("here")
                checker = 1
                embed1 = discord.Embed(title="Step 1",colour=discord.Colour.purple(),description="Alright message found! Now tell me do you want to add a reaction role or delete a reaction role.\nReply with `add` or `delete`")
                await ctx.send(embed = embed1)
                try:
                    response = await self.client.wait_for('message', check=check,timeout=120)
                except:
                    embedtimeout = discord.Embed(title="Reaction Roles Updation Timed Out",
                                                 colour=discord.Colour.purple(),
                                                 description=f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles updation is cancelled`")
                    return await ctx.send(embed=embedtimeout)
                    # return await ctx.send(f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles creation is cancelled`")
                if response.content.lower() == "exit":
                    embedexit = discord.Embed(colour=discord.Colour.purple())
                    embedexit.set_author(name="Alright! Seems we are not updating reaction roles anymore.")
                    return await ctx.send(embed = embedexit)
                    # return await ctx.send("Alright! Seems we are not updating reaction roles anymore.")

                if response.content.lower() == "add":
                    embed2 = discord.Embed(title="Step 2",colour=discord.Colour.purple(),description="Sweet! Now tell me how many reaction roles you want to add")
                    await ctx.send(embed = embed2)
                    try:
                        num = await self.client.wait_for('message', check=check,timeout=120)
                    except:
                        embedtimeout = discord.Embed(title="Reaction Roles Updation Timed Out",
                                                     colour=discord.Colour.purple(),
                                                     description=f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles updation is cancelled`")
                        return await ctx.send(embed=embedtimeout)
                        # return await ctx.send(f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles creation is cancelled`")
                    if num.content.lower() == "exit":
                        embedexit = discord.Embed(colour=discord.Colour.purple())
                        embedexit.set_author(name="Alright! Seems we are not updating reaction roles anymore.")
                        return await ctx.send(embed = embedexit)
                    if not num.content.isdigit():
                        embednumnotdigit = discord.Embed(colour=discord.Colour.purple(),description='Uh ho! You should have entered a number \nPlease restart the process from the beginning')
                        return await ctx.send(embed = embednumnotdigit)
                    else:
                        data = x["data"]
                        count = 1
                        excep = 0
                        dict = {"0": "th", "1": "st", "2": "nd", "3": "rd", "4": "th", "5": "th", "6": "th", "7": "th",
                                "8": "th", "9": "th"}
                        new=  {}
                        for j in range(int(num.content)):
                            embed3A = discord.Embed(title = "Step 3A",colour=discord.Colour.purple(),description=f'Send an emoji for the {count}{dict[str(count)[-1]]} reaction role')
                            await ctx.send(embed = embed3A)
                            try:
                                emojiinput = await self.client.wait_for('message', check=check,timeout=120)
                            except:
                                embedtimeout = discord.Embed(title="Reaction Roles Updation Timed Out",
                                                             colour=discord.Colour.purple(),
                                                             description=f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles updation is cancelled`")
                                return await ctx.send(embed=embedtimeout)
                            if emojiinput.content.lower() == "exit":
                                embedexit = discord.Embed(colour=discord.Colour.purple())
                                embedexit.set_author(name="Alright! Seems we are not updating reaction roles anymore.")
                                return await ctx.send(embed = embedexit)
                            try:
                                emoji = await commands.EmojiConverter().convert(ctx, emojiinput.content)
                            except:
                                try:
                                    checkunicode = emojis.get(emojiinput.content[0])
                                    if len(checkunicode) !=0:
                                        emoji = emojiinput.content[0]
                                    else:
                                        raise commands.CommandError
                                except:
                                    embedwronginput = discord.Embed(colour=discord.Colour.purple(),description="Invalid Emoji. Ignoring this input")
                                    await ctx.send(embed = embedwronginput)
                                    count +=1
                                    excep +=1
                                    continue
                            if str(emoji) in data or str(emoji) in new:
                                embedwrongiput = discord.Embed(colour=discord.Colour.purple(),description="The emoji already has a reaction role associated with it. Ignoring this input")
                                await ctx.send(embed = embedwrongiput)
                                count +=1
                                excep +=1
                                continue
                            # try:
                            #     await message.add_reaction(str(emoji))
                            # except:
                            #     return await ctx.send('An emoji should have been sent...')
                            embed3B = discord.Embed(colour=discord.Colour.purple(),title = "Step 3B",description='Send the Role id or mention the role which will be assigned by reacting with {}'.format(
                                    emoji))
                            await ctx.send(embed = embed3B)
                            try:
                                role_id = await self.client.wait_for('message', check=check,timeout=120)
                            except:
                                embedtimeout = discord.Embed(title="Reaction Roles Updation Timed Out",
                                                             colour=discord.Colour.purple(),
                                                             description=f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles updation is cancelled`")
                                return await ctx.send(embed=embedtimeout)
                            if role_id.content.lower() == "exit":
                                embedexit = discord.Embed(colour=discord.Colour.purple())
                                embedexit.set_author(
                                    name="Alright! Seems we are not setting up reaction roles anymore.")
                                return await ctx.send(embed = embedexit)
                            role_id = role_id.content
                            role_id = role_id.replace("<", "")
                            role_id = role_id.replace(">", "")
                            role_id = role_id.replace("@", "")
                            role_id = role_id.replace("&", "")
                            role_id = role_id.replace("!", "")
                            if not role_id.isdigit():
                                embedwrongroleinput = discord.Embed(colour=discord.Colour.purple(),description='Invalid Role . Ignoring this input')
                                await ctx.send(embed = embedwrongroleinput)
                                count +=1
                                excep +=1
                                continue
                            try:
                                role = ctx.guild.get_role(int(role_id))
                                if role.position > ctx.author.top_role.position and not ctx.author == ctx.guild.owner:
                                    embedrolepos = discord.Embed(colour=discord.Colour.purple(),description='The role is higher than your current role. Ignoring this input')
                                    await ctx.send(embed = embedrolepos)
                                    count +=1
                                    excep+=1
                                    continue
                                if role.position >= ctx.guild.me.top_role.position:
                                    embedbotrolepos = discord.Embed(colour=discord.Colour.purple(),description='The role higher than or equal to my top role. Ignoring this input')
                                    await ctx.send(embed = embedbotrolepos)
                                    count +=1
                                    excep +=1
                                    continue
                            except:
                                embedinvrole = discord.Embed(colour=discord.Colour.purple(),description='Invalid Role. Ignoring this input')
                                await ctx.send(embed = embedinvrole)
                                count +=1
                                excep +=1
                                continue
                            data[str(emoji)] = role.id
                            new[str(emoji)] = role.id
                            count += 1
                        finaldata = data
                        bool =1
                        boolcounter = 0
                        if (count - 1) == excep:
                            embednotsetup = discord.Embed(colour=discord.Colour.purple(),description="Reaction roles haven't been updated on the message because all the inputs were incorrect.")
                            return await ctx.send(embed = embednotsetup)
                        for q in new.keys():
                            try:
                                await message.add_reaction(q)
                                finaldata[str(q)] = new[q]
                                boolcounter+=1
                            except:
                                embedissue = discord.Embed(colour=discord.Colour.purple(),description=f"Issue Occured while reacting to the message since the emoji {q}.\nThis issue might have occured because there were already 20 reactions on that message or i don't have permissions to add reaction. \n\nIf you feel this error wouldn't have occured, join my support server and ask it there\nhttps://discord.com/invite/tTr6DvyRCH.")
                                await ctx.send(embed = embedissue)
                                bool = 0
                                breakemoji = q
                                break
                        if bool ==0 and boolcounter==0:
                            embednotupdated = discord.Embed(colour=discord.Colour.purple(),description="Reaction roles haven't been updated on the message because i wasn't able to react with even 1 emoji because of the issue occured")
                            return await ctx.send(embed = embednotupdated)
                        elif bool == 0 and boolcounter!=0:
                            embedpartialupdated = discord.Embed(title = "Reaction Roles - Updation Done",colour=discord.Colour.purple(),description=f"Done! Reaction roles have been updated till {breakemoji} emoji (not included) because of the error occured while reacting.")
                            await ctx.send(embed = embedpartialupdated)
                        else:
                            if excep !=0:
                                embedsend1 = discord.Embed(title="Reaction Roles- Updation Done",colour=discord.Colour.purple(),description=f"Perfect! The reaction roles have been updated successfully and {excep} inputs were ignored due to invalid inputs.. Go check it out {messagelink}")
                                await ctx.send(embed = embedsend1)
                            else:
                                embedsend2 = discord.Embed(title="Reaction Roles- Updation Done",
                                                           colour=discord.Colour.purple(),
                                                           description=f"Perfect! The reaction roles have been updated successfully. Go check it out {messagelink}")
                                await ctx.send(embed = embedsend2)
                        # print(data)
                        rinfo = {
                            "guildid" : str(ctx.guild.id),
                            "messageid": str(message.id),
                            "data": finaldata,
                            "messagelink":messagelink
                        }
                        await reactionroles.replace_one({'messageid': str(message.id)},rinfo)
                        return
                elif response.content.lower()=="delete":
                    embed1 = discord.Embed(title="Step 1",colour=discord.Colour.purple(),description="Sweet! Now tell me how many reaction roles you want to delete")
                    await ctx.send(embed = embed1)
                    try:
                        num = await self.client.wait_for('message', check=check,timeout=120)
                    except:
                        embedtimeout = discord.Embed(title="Reaction Roles Updation Timed Out",
                                                     colour=discord.Colour.purple(),
                                                     description=f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles updation is cancelled`")
                        return await ctx.send(embed=embedtimeout)
                    if num.content.lower() == "exit":
                        embedexit = discord.Embed(colour=discord.Colour.purple())
                        embedexit.set_author(name="Alright! Seems we are not updating reaction roles anymore.")
                        return await ctx.send(embed = embedexit)
                    if not num.content.isdigit():
                        embednotnumdig = discord.Embed(colour=discord.Colour.purple(),description='Uh ho! You should have entered a number \nPlease restart the process from the beginning')
                        return await ctx.send(embed = embednotnumdig)
                    elif int(num.content) <1 or int(num.content)>20:
                        embednotrange = discord.Embed(colour=discord.Colour.purple(),description="No. should be between 1 and 20")
                        return await ctx.send(embed = embednotrange)
                    else:
                        data = x["data"]
                        count = 1
                        dict = {"0": "th", "1": "st", "2": "nd", "3": "rd", "4": "th", "5": "th", "6": "th", "7": "th",
                                "8": "th", "9": "th"}
                        excep = 0
                        for j in range(int(num.content)):
                            embed2 = discord.Embed(title= "Step2",colour=discord.Colour.purple(),description=f'Send the emoji for the {count}{dict[str(count)[-1]]} reaction role which you want to remove')
                            await ctx.send(embed = embed2)
                            try:
                                emojiinput = await self.client.wait_for('message', check=check,timeout=120)
                            except:
                                embedtimeout = discord.Embed(title="Reaction Roles Updation Timed Out",
                                                             colour=discord.Colour.purple(),
                                                             description=f"Uh ho! you took more than 2 minutes to respond {ctx.author.mention}!. \n\n`Reaction roles updation is cancelled`")
                                return await ctx.send(embed=embedtimeout)
                            if emojiinput.content.lower() == "exit":
                                embedexit = discord.Embed(colour=discord.Colour.purple())
                                embedexit.set_author(name="Alright! Seems we are not updating reaction roles anymore.")
                                return await ctx.send(embed = embedexit)
                            try:
                                emoji = await commands.EmojiConverter().convert(ctx, emojiinput.content)
                            except:
                                try:
                                    checkunicode = emojis.get(emojiinput.content[0])
                                    if len(checkunicode) !=0:
                                        emoji = emojiinput.content[0]
                                    else:
                                        raise commands.CommandError
                                except:
                                    embedinvemoji = discord.Embed(colour=discord.Colour.purple(),description='Invalid emoji. Ignoring this input')
                                    await ctx.send(embed = embedinvemoji)
                                    count +=1
                                    excep +=1
                                    continue

                            if str(emoji) in data:
                                data.pop(str(emoji))
                            else:
                                embednorr = discord.Embed(colour=discord.Colour.purple(),description="There isn't any reaction role setup with that emoji on that message")
                                await ctx.send(embed = embednorr)
                                count +=1
                                excep +=1
                                continue
                            count += 1
                        if (count-1) ==excep:
                            embednotup = discord.Embed(colour=discord.Colour.purple(),description="Reaction roles have not been updated as values entered were incorrect")
                            return await ctx.send(embed = embednotup)
                        else:
                            if excep != 0:
                                embedsend1 = discord.Embed(title="Reaction Roles - Updation Done",colour=discord.Colour.purple(),description=f"Perfect! The reaction roles have been updated successfully and {excep} incorrect inputs were ignored.\n[Message Link]({messagelink}\n\n**Note -** `My reaction will remain there on the message with the emoji(s) whose reaction roles you removed right now , but the reaction roles will not work for those emojis`")
                                await ctx.send(embed = embedsend1)
                            else:
                                embedsend2 = discord.Embed(title="Reaction Roles - Updation Done",colour=discord.Colour.purple(),description=f"Perfect! The reaction roles have been updated successfully.\n[Message Link]({messagelink})\n\n**Note -** `My reaction will remain there on the message with the emoji(s) whose reaction roles you removed right now , but the reaction roles will not work for those emojis`")
                                await ctx.send(embed = embedsend2)
                        # print(data)
                            rinfo = {
                                "guildid" : str(ctx.guild.id),
                                "messageid": str(message.id),
                                "data": data,
                                "messagelink":messagelink
                            }
                            await reactionroles.replace_one({'messageid': str(message.id)}, rinfo)
                        return
                else:
                    embedinvresponse = discord.Embed(colour=discord.Colour.purple(),description="Invalid response")
                    return await ctx.send(embed = embedinvresponse)
        if checker !=0:
            embednorrexist = discord.Embed(colour=discord.Colour.purple(),description="The message doesn't have reaction roles setup on it. use `>rrcreate` command to set the reaction roles first")
            return await ctx.send(embed = embednorrexist)
        return

    @commands.command(description="gives info regarding reaction roles setup on a message")
    @commands.has_permissions(manage_roles = True)
    async def rrinfo(self,ctx,messagelink = None):
        if messagelink is None:
            embednomsglink = discord.Embed(colour=discord.Colour.purple(),description="Pls try again by entering the message link")
            return await ctx.send(embed = embednomsglink)
        try:
            message = await commands.MessageConverter().convert(ctx, messagelink)
        except Exception as e:
            embedmsgnotfound = discord.Embed(colour=discord.Colour.purple(),description="Uh ho! Message not found . Pls try again and provide a correct link next time")
            await ctx.send(embed = embedmsgnotfound)
            return
        all = reactionroles.find({})
        checker =0
        async for x in all:
            if x["messageid"]==str(message.id):
                checker =1
                rrlist = x["data"]
                s =""
                for i in rrlist:
                    s += str(i) + f" **-** <@&{x['data'][str(i)]}>" + "\t**;**\t"
                embed = discord.Embed(title= "Reaction Roles Information",colour=discord.Colour.purple(),description=f'''
Message Id - {message.id}
Message Link - {messagelink}

No. of Reaction roles on the message - {len(rrlist)}

Emojis and Roles - {s}''')
                await ctx.send(embed =embed)
                return
        if checker==0:
            embednorrexist = discord.Embed(colour=discord.Colour.purple(),description="The message doesn't have reaction roles setup on it")
            return await ctx.send(embed = embednorrexist)
        return

    @commands.command(description="gives info of all the messages having reaction roles setup in the server")
    @commands.has_permissions(manage_roles = True)
    async def rrlist(self,ctx):
        # a = reactionroles.find({"guildid":"dkjadjk"}).count()
        # print("here")
        count = await reactionroles.count_documents({'guildid': f"{ctx.guild.id}"})
        if count ==0:
            embed = discord.Embed(colour=discord.Colour.purple())
            embed.set_author(name="There are no reaction roles set up in this server")
            await ctx.send(embed=embed)
            return
        # async for x in a:
        #     print(x)
        #
        # # return
        all = reactionroles.find({"guildid":f"{ctx.guild.id}"})
        desc = ''''''
        c=1

        async for x in all:
            desc = desc + f"Message {c} - {x['messagelink']}"+"\n"
            c+=1
        embed = discord.Embed(title = "List of Messages which have Reaction Roles setup",colour=discord.Colour.purple(),description=desc)
        embed.set_footer(text="To get information about a particular message use `>rrinfo [messaglink]`")
        await ctx.send(embed=embed)
        return
        

async def setup(client):
    await client.add_cog(rr(client))