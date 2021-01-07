import discord
import json
import random
import os
from discord.ext import commands
from importlib.machinery import SourceFileLoader

token = os.environ['DISCORD_TOKEN']

intents = discord.Intents.all()

c = commands.Bot(command_prefix = '.', intents=intents)
c.remove_command('help')

@c.event
async def on_ready():
    print(f"{c.user.name}")
    for guild in c.guilds:
        members = len(guild.members)
    await c.change_presence(activity=discord.Streaming(name=f'ציונים {members}', url='https://youtu.be/V9hav4QPSeU?t=6'))

@c.event
async def on_raw_reaction_add(payload):
    if payload.member.bot: return
    msgid = payload.message_id


@c.command(aliases=['helpme'])
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_author(name='Help')

    embed.add_field(name='.test', value='Test command', inline=False)

    await ctx.channel.send(embed=embed)

@c.command()
async def test(ctx):
    await ctx.message.channel.send("Message recieved")
  
@c.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Member")
    rand1 = random.randint(1,100)
    rand2 = random.randint(1,100)
    if rand1 == rand2:
        role2 = discord.utils.get(member.guild.roles, name="ציוני ראוי")
        await member.add_roles(role2)
    await member.add_roles(role)
    welcome_channel = discord.utils.get(ctx.guild.channels, name="『🤝』ברוכים-הבאים")
    await welcome_channel.send(f"ברוכים הבאים לשרת {member.mention}")

@c.command()
@commands.has_role('Owner')
async def addroletoeveryone(ctx, role : discord.Role):
    #role = discord.utils.get(ctx.guild.roles, name="Member")
    for m in ctx.guild.members:
        await ctx.channel.send(f"**Added role {role.name} to: {m.name} **")
        await m.add_roles(role)

@c.command()
@commands.has_permissions(Adminstrator = True)
async def purge(ctx, limit=10):
    member = ctx.message.author
    await ctx.message.delete()
    msg = []
    try:
        limit = int(limit)
    except:
        return await ctx.send(f"{ctx.message.author.mention} בבקשה להשתמש במספר")
    if not member:
        await ctx.channel.purge(limit=limit)
        return await ctx.send(f"**מחקתי {limit} הודעות**", delete_after=2)
    async for m in ctx.channel.history():
        if len(msg) == limit:
            break
        if m.author == member:
            msg.append(m)
    await ctx.channel.delete_messages(msg)
    await ctx.send(f"מחקתי {limit} הודעות", delete_after=2)

c.run(token)