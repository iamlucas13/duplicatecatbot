import discord
import env
from discord.ext import commands

# Définir les intents que ton bot utilisera
intents = discord.Intents.default()
intents.message_content = True  # Si tu veux que le bot puisse lire les messages texte
intents.guilds = True  # Si tu veux que le bot puisse interagir avec les guildes

# Initialiser le bot avec les intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def duplicate_category(ctx, category_id: int):
    # Récupérer la catégorie à partir de son ID
    original_category = discord.utils.get(ctx.guild.categories, id=category_id)
    if not original_category:
        await ctx.send(f"No category with ID '{category_id}' found.")
        return

    # Créer la nouvelle catégorie en copiant les permissions de la catégorie originale
    new_category = await ctx.guild.create_category(name=f"{original_category.name} - copy", overwrites=original_category.overwrites)

    for channel in original_category.channels:
        # Copier les permissions spécifiques au salon
        overwrites = channel.overwrites
        if isinstance(channel, discord.TextChannel):
            await ctx.guild.create_text_channel(name=channel.name, category=new_category, overwrites=overwrites)
        elif isinstance(channel, discord.VoiceChannel):
            await ctx.guild.create_voice_channel(name=channel.name, category=new_category, overwrites=overwrites)

    # Appliquer les permissions de la catégorie originale à la nouvelle catégorie
    for role, permissions in original_category.overwrites.items():
        await new_category.set_permissions(role, overwrite=permissions)

    await ctx.send(f"Category '{original_category.name}' duplicated successfully with permissions.")

@bot.command()
async def duplicate_category_only(ctx, category_id: int):
    # Récupérer la catégorie à partir de son ID
    original_category = discord.utils.get(ctx.guild.categories, id=category_id)
    if not original_category:
        await ctx.send(f"No category with ID '{category_id}' found.")
        return

    # Créer la nouvelle catégorie en copiant les permissions de la catégorie originale
    new_category = await ctx.guild.create_category(name=f"{original_category.name} - copy", overwrites=original_category.overwrites)

    # Appliquer les permissions de la catégorie originale à la nouvelle catégorie
    for role, permissions in original_category.overwrites.items():
        await new_category.set_permissions(role, overwrite=permissions)

    await ctx.send(f"Category '{original_category.name}' duplicated successfully without channels.")



bot.run(env.DISCORD_TOKEN)
