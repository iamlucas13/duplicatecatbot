import discord
from discord.ext import commands
import env  # Importer le token depuis env.py
from category import duplicate_category, duplicate_category_only
from discord.app_commands import MissingPermissions  # Import de l'erreur

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    # Synchroniser les commandes slash
    try:
        bot.tree.copy_global_to(guild=discord.Object(id=env.DISCORD_ID))
        synced = await bot.tree.sync(guild=discord.Object(id=env.DISCORD_ID))
        print(f"Synced {len(synced)} commands to guild {env.DISCORD_ID}.")
    except discord.HTTPException as e:
        print(f"Failed to sync commands: {e}")

# Gestionnaire d'erreurs global pour les commandes slash
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, MissingPermissions):
        await interaction.response.send_message(
            "You do not have the necessary permissions to use this command. Only administrators can execute it.", 
            ephemeral=True
        )
    else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

# Ajouter les commandes traditionnelles
bot.add_command(duplicate_category)
bot.add_command(duplicate_category_only)

# Charger la commande slash duplicate_category_only du dossier commands
async def setup_hook():
    await bot.load_extension("commands.ping")
    await bot.load_extension("commands.duplicate_category_only_slash")
    await bot.load_extension("commands.duplicate_category_slash")

bot.setup_hook = setup_hook

bot.run(env.DISCORD_TOKEN)
