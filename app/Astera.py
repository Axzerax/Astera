# Created by Xz1il on github / Xzil_#3487 on discord
# This is still in development and features are still going to be added!


import discord
import time
import asyncio
import requests
import json
import smtplib
import pathlib
import logging
import os

from discord.ext.commands import bot, context
from discord.ext.commands.core import _CaseInsensitiveDict, command
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from discord import client
from discord import embeds
from discord import activity
from discord.ext import commands
from email import message
from discord.colour import Color
from os import name
from discord.gateway import DiscordClientWebSocketResponse
from discord.guild import BanEntry
from discord.enums import Status
from discord.message import Message
from discord.member import Member

Token = "YOURTOKEN" # Make an application inside the discord developer pannel, and make a bot, then put the bot's token here.

Role = "YOUROLE" # Change this to whatever role you want to allow the commands to be ran by.

Muted = "YOUROLE"

NormalRole = "YOUROLE"

bot = commands.Bot(command_prefix="!", case_insensitive=True)

game = discord.Game("Type !commands for more info | https://github.com/Xz1il/Astera")

DiscordWebHook = "YOURWEBHOOK" # Put the channel of your choice webhook here, for shutdown logs.

Mail_Content = '''Hello,
Someone has requested a full shutdown of the bot Astera, make sure to check if this was supposed to happen
and not a admin abuser!

Please do not reply to this email, as this is a no-reply email.
'''

# Change all of them from here to Reveiver address.

Sender_Address = "The sender address, the email it will send from!"
Sender_Pass = "The password of the sender address, I recomend making an app password!"
Receiver_Address = "The receiver address of your choice to receive the emails from the bot."

message = MIMEMultipart()
message["From"] = Sender_Address
message["To"] = Receiver_Address
message["Subject"] = "[Astera] - A full shutdown was requested!"

message.attach(MIMEText(Mail_Content, "plain"))

Session = smtplib.SMTP("smtp.gmail.com", 587)
Session.starttls()
Session.login(Sender_Address, Sender_Pass)
text = message.as_string()

Logger = logging.getLogger("discord")
Logger.setLevel(logging.DEBUG)
Handler = logging.FileHandler(filename="Debug_Logs.json", encoding="utf-8", mode="w")
Handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
Logger.addHandler(Handler)

CommandsVar = '''
**Help Menu**: `!commands`
**Shutdown Astera**: `!shutdown`
**Ban**: `!ban <Member>`
**Unban**: `!unban <Member>`
**Kick**: `!kick <Member>`
**SoftBan**: `!softban <Member>`
**UnsoftBan**: `!unsoftban <Member>`
**Warn**: `!warn <Member>`
**VcMute**: `!vcmute <Member>`
**UnVcMute**: `!unvcmute <Member>`
**VcBan**: `!vcban <Member>`
**UnVcBan**: `!unvcban <Member>`
**Clear**: `!clear <Amount>`
**Version**: `!version`
**Info**: `!info`
'''

@bot.event
async def on_ready():
    print("Starting")
    time.sleep(2)
    print("Logged on!")
    await bot.change_presence(status=discord.Status.online, activity=game)

@commands.guild_only()
@bot.command()
async def commands(ctx):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        EmbedVar = discord.Embed(title="Astera", color=0xA2C4C9)
        EmbedVar.add_field(name="Commands", value=CommandsVar, inline=True)
        await ctx.channel.send(embed=EmbedVar)
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

@bot.command()
async def shutdown(ctx):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        print("Starting Shutdown..")
        time.sleep(5)

        EmbedShutdown = discord.Embed(title="Astera", description="Shutting Down..", color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedShutdown)
        requests.post(DiscordWebHook, data={"content": "The user" + " " + ctx.author.mention + " " + "has request a full shutdown of Astera!"})
        Session.sendmail(Sender_Address, Receiver_Address, text)

        print("Sent Full Shutdown Report!")
        await bot.close()
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        await member.ban(reason=reason)

        EmbedBan = discord.Embed(title="Info", description="Successfuly Banned the user" + " " + member.mention + "!")
        await message.channel.send(embed=EmbedBan)
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

@bot.command()
async def unban(ctx, *, member):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                EmbedUnban = discord.Embed(title="Info", description="Successfuly Unbanned user" + " " + user.mention, color=0xA2C4C9)
                await ctx.channel.send(embed=EmbedUnban)
                return
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

@bot.command()
async def softban(ctx, member : discord.Member):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        MutedRole = discord.utils.get(ctx.guild.roles, name=Muted)
        MemberRole = discord.utils.get(ctx.guild.roles, name=NormalRole)

        await member.remove_roles(MemberRole)
        await member.add_roles(MutedRole)

        EmbedMuted = discord.Embed(title="Info", description="Successfuly Soft Banned the user" + " " + member.mention + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedMuted)
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

@bot.command()
async def unsoftban(ctx, member : discord.Member):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        MutedRole = discord.utils.get(ctx.guild.roles, name=Muted)
        MemberRole = discord.utils.get(ctx.guild.roles, name=NormalRole)

        await member.remove_roles(MutedRole)
        await member.add_roles(MemberRole)

        EmbedUnmute = discord.Embed(title="Info", description="Successfuly Un-Soft Banned the user" + " " + member.mention + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedUnmute)
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

@bot.command()
async def vcmute(ctx, member : discord.Member):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        await member.edit(mute = True)

        EmbedVcmute = discord.Embed(title="Info", description="Successfuly Vcmuted the user" + " " + member.mention + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedVcmute)
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

@bot.command()
async def unvcmute(ctx, member : discord.Member):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        await member.edit(mute = False)

        EmbedUnvcmute = discord.Embed(title="Info", description="Successfuly UnVcmuted the user" + " " + member.mention + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedUnvcmute)
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

@bot.command()
async def info(ctx):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        EmbedInfo = discord.Embed(title="Info", description="Astera was created by Xzil_#3487 and is written in python and is an open-source project." + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedInfo)
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

@bot.command()
async def version(ctx):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        EmbedVersion = discord.Embed(title="Info", description="Astera Beta" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedVersion)
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

@bot.command()
async def clear(ctx, amount = 4):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        await ctx.channel.purge(limit = amount)

        EmbedVersion = discord.Embed(title="Info", description="Successfuly Bulk deleted" + " " + str(amount) + " " + "messages" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedVersion)
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

@bot.command()
async def kick(ctx, member : discord.Member, *, reason = None):
    role = discord.utils.get(ctx.guild.roles, name=Role)
    if role in ctx.author.roles:
        await member.kick(reason=reason)

        EmbedKick = discord.Embed(title="Info", description="Successfuly Kicked" + " " + member.mention + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedKick)
    else:
        EmbedError = discord.Embed(title="Error", description="You're not authorized to use this command!" + " " + ctx.author.mention, color=0xA2C4C9)
        await ctx.channel.send(embed=EmbedError)

bot.run(Token)
