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


@c.command(aliases=['cmd','commands','cmds'])
async def command(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_author(name='Help')

    embed.add_field(name='.test', value='Test command', inline=False)

    await ctx.channel.send(embed=embed)
  
@c.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Member")
    rand1 = random.randint(1,100)
    rand2 = random.randint(1,100)
    if rand1 == rand2:
        role2 = discord.utils.get(member.guild.roles, name="ציוני ראוי")
        await member.add_roles(role2)
        await member.send("קיבלת רול **ציוני ראוי** שמקבלים אחת ל2 בחזקת 100 מצטרפים לשרת!")
    await member.add_roles(role)
    welcome_channel = discord.utils.get(member.guild.channels, name="『🤝』ברוכים-הבאים")
    await welcome_channel.send(f"ברוכים הבאים לשרת {member.mention}")

@c.command()
@commands.has_role('Owner')
async def addroletoeveryone(ctx, role : discord.Role):
    #role = discord.utils.get(ctx.guild.roles, name="Member")
    for m in ctx.guild.members:
        await ctx.channel.send(f"**Added role {role.name} to: {m.name} **")
        await m.add_roles(role)

@c.command()
@commands.has_permissions(administrator = True)
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

@c.command(aliases=['h','helpme','עזרה'])
async def help(ctx):
    if ctx.channel.id != 796766184565243934:
        await ctx.message.delete()
        help_channel = discord.utils.get(ctx.guild.channels, name="『🙋』עזרה")
        await ctx.channel.send(f"ניתן לשלוח את הפקודה הזאת רק בחדר {help_channel.mention}",delete_after=5)

    staff = discord.utils.get(member.guild.roles, name="●▬▬▬▬staff▬▬▬▬●")
    await ctx.channel.send(f"צריך את עזרתכם {ctx.member.mention} ,{staff.mention}")

c.run(token)