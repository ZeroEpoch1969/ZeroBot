import discord
import os
import re
import checks
import asyncio
import time
import datetime
import subprocess

from discord.ext import commands
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix="z!", description="Some moderation bot", pm_help=False)

xl = "```xl\n{}```"

py = "```py\n{}```"

admin_role_ids = checks.admin_role_ids

mod_role_id = checks.mod_role_id

nsfw_role_id = 321747603677118465

update_role_id = 321747640918474763

ruby_rose_id = 209470164633124864

auto_reboot_ruby = True

bot_log_channel_id = 321769461051031562

last_reboot = None

poll_role_id = 402693375179882497

@bot.event
async def on_ready():
    print("Connected! Logged in as {}/{}".format(bot.user, bot.user.id))
    await bot.change_presence(game=discord.Game(name="with my Mercenary"), status=discord.Status.dnd)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, checks.dev_only):
        await ctx.send("Only the bot developers may use this command")
        return
    if isinstance(error, checks.admin_only):
        await ctx.send("Only the server admins may use this command")
        return
    if isinstance(error, checks.mod_only):
        await ctx.send("Only server mods may use this command")
        return
    try:
        await ctx.send(error)
    except:
        pass
    print("An error occured while executing the command named {}: {}".format(ctx.command.qualified_name, error))

@bot.event
async def on_message(message):
    if not isinstance(message.author, discord.Member) or message.author.bot or message.author is bot.user:
        return
    no_filter_role_ids = [mod_role_id, 321747548823879680, 321747755519442955, 321808415120687104]
    for id in admin_role_ids:
        no_filter_role_ids.append(id)
    bypass = False
    for role in message.author.roles:
        if role.id in no_filter_role_ids:
            bypass = True
            break
    if not bypass:
        if re.search("/discord\.gg\/[a-zA-z0-9\-]{1,16}", message.content) or re.search("/discordapp\.com\/invite\/[a-z0-9]+/ig", message.content):
            await message.delete()
            await message.channel.send("{} do not post invite links to other discord servers.".format(message.author.mention))
    await bot.process_commands(message)

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if after.id == ruby_rose_id and before.status != discord.Status.offline and after.status == discord.Status.offline and auto_reboot_ruby:
        global last_reboot
        now = datetime.now()
        last = last_reboot
        if last_reboot != None:
            time_remaining = (last - now).seconds
            if (last - now).total_seconds() > 0:
                return
        last_reboot = now + timedelta(minutes=1)
        os.popen("restartbot.sh")
        await bot.get_channel(bot_log_channel_id).send(":stopwatch: `{}` {}".format(time.strftime("%H:%M:%S"), "Ruby Rose was automatically rebooted"))

@bot.command(hidden=True)
@checks.is_dev()
async def debug(ctx, *, shit:str):
    """This is the part where I make 20,000 typos before I get it right"""
    # "what the fuck is with your variable naming" - EJH2
    # seth seriously what the fuck - Robin
    import os
    import random
    import re
    from datetime import datetime, timedelta
    try:
        rebug = eval(shit)
        if asyncio.iscoroutine(rebug):
            rebug = await rebug
        await ctx.send(py.format(rebug))
    except Exception as damnit:
        await ctx.send(py.format("{}: {}".format(type(damnit).__name__, damnit)))

@bot.command(hidden=True)
@checks.is_dev()
async def terminal(ctx, *, command:str):
    """Runs terminal commands and shows the output via a message. Oooh spoopy!"""
    try:
        await ctx.channel.trigger_typing()
        await ctx.send(xl.format(subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("ascii")))
    except:
        await ctx.send("Error, couldn't send command")

@bot.command()
async def updates(ctx):
    """Subscribes you to bot update notifications"""
    role = discord.utils.get(ctx.guild.roles, id=update_role_id)
    if role is None:
        await ctx.send("Uh oh! The Updates role wasn't found!")
    await ctx.author.add_roles(role)
    await ctx.send("Okay you are now subscribed to update notifications")

@bot.command()
async def noupdates(ctx):
    """Un-subscribes you from bot update notifications"""
    role = discord.utils.get(ctx.message.guild.roles, id=update_role_id)
    if role is None:
        await ctx.send("Uh oh! The Updates role wasn't found!")
    await ctx.author.remove_roles(role)
    await ctx.send("Okay you are now un-subscribed from update notifications")

@checks.is_admin()
@bot.command(hidden=True)
async def toggleautoreboot(ctx):
    """Toggles auto reboot on Ruby Rose"""
    global auto_reboot_ruby
    auto_reboot_ruby = not auto_reboot_ruby
    if auto_reboot_ruby:
        await ctx.send("Ruby Rose will now auto reboot on crash")
    else:
        await ctx.send("Ruby Rose will no longer auto reboot on crash")
        
@bot.command()
async def polls(ctx):
    """Subscribes you to bot poll notifications"""
    role = discord.utils.get(ctx.guild.roles, id=poll_role_id)
    if role is None:
        await ctx.send("Uh oh! The Polls role wasn't found!")
    await ctx.author.add_roles(role)
    await ctx.send("Okay you are now subscribed to poll notifications")

@bot.command()
async def nopolls(ctx):
    """Un-subscribes you from poll notificatios"""
    role = discord.utils.get(ctx.message.guild.roles, id=poll_role_id)
    if role is None:
        await ctx.send("Uh oh! The Polls role wasn't found!")
    await ctx.author.remove_roles(role)
    await ctx.send("Okay you are now un-subscribed from poll notifications")

print("Connecting...")
bot.run("put ur token here")
