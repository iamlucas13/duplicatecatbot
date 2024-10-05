import discord
from discord.ext import commands
import env  # Importer le token depuis env.py
from category import duplicate_category, duplicate_category_only

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Gestionnaire d'erreurs global
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the necessary permissions to use this command.")
    else:
        # Vous pouvez gérer d'autres types d'erreurs ici
        await ctx.send(f"An error occurred: {error}")

# Ajouter les commandes
bot.add_command(duplicate_category)
bot.add_command(duplicate_category_only)

bot.run(env.DISCORD_TOKEN)
