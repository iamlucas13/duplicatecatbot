import discord
from discord.ext import commands
import env  # Importer le token depuis env.py

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Vérifier si l'utilisateur qui exécute la commande est un administrateur
def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
@is_admin()
async def duplicate_category(ctx, category_id: int):
    original_category = discord.utils.get(ctx.guild.categories, id=category_id)
    if not original_category:
        await ctx.send(f"No category with ID '{category_id}' found.")
        return

    new_category = await ctx.guild.create_category(name=f"{original_category.name} - copy", overwrites=original_category.overwrites)

    for channel in original_category.channels:
        overwrites = channel.overwrites
        if isinstance(channel, discord.TextChannel):
            await ctx.guild.create_text_channel(name=channel.name, category=new_category, overwrites=overwrites)
        elif isinstance(channel, discord.VoiceChannel):
            await ctx.guild.create_voice_channel(name=channel.name, category=new_category, overwrites=overwrites)

    for role, permissions in original_category.overwrites.items():
        await new_category.set_permissions(role, overwrite=permissions)

    await ctx.send(f"Category '{original_category.name}' duplicated successfully with permissions.")

@bot.command()
@is_admin()
async def duplicate_category_only(ctx, category_id: int):
    original_category = discord.utils.get(ctx.guild.categories, id=category_id)
    if not original_category:
        await ctx.send(f"No category with ID '{category_id}' found.")
        return

    new_category = await ctx.guild.create_category(name=f"{original_category.name} - copy", overwrites=original_category.overwrites)

    for role, permissions in original_category.overwrites.items():
        await new_category.set_permissions(role, overwrite=permissions)

    await ctx.send(f"Category '{original_category.name}' duplicated successfully without channels.")

bot.run(env.DISCORD_TOKEN)
