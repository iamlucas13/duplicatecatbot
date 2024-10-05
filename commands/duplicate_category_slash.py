import discord
from discord import app_commands
from discord.ext import commands

class DuplicateCategorySlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commande slash /duplicate_category
    @app_commands.command(name="duplicate_category", description="Duplicate a category with channels")
    @app_commands.checks.has_permissions(administrator=True)  # Vérifie si l'utilisateur est administrateur
    async def duplicate_category(self, interaction: discord.Interaction, category_id: str):
        # Envoyer une réponse initiale pour informer l'utilisateur que la commande est en cours d'exécution
        await interaction.response.send_message("Command received. The process is running, please wait...", ephemeral=True)

        try:
            category_id = int(category_id)  # Conversion de l'ID en entier
        except ValueError:
            # Utiliser followup.send pour envoyer des messages supplémentaires
            await interaction.followup.send(f"Invalid category ID '{category_id}'.", ephemeral=True)
            return

        original_category = discord.utils.get(interaction.guild.categories, id=category_id)
        if not original_category:
            await interaction.followup.send(f"No category found with ID '{category_id}'.", ephemeral=True)
            return

        # Créer une nouvelle catégorie en dupliquant uniquement les permissions
        new_category = await interaction.guild.create_category(
            name=f"{original_category.name} - copy", 
            overwrites=original_category.overwrites
        )

        # Dupliquer les salons
        for channel in original_category.channels:
            overwrites = channel.overwrites
            if isinstance(channel, discord.TextChannel):
                await interaction.guild.create_text_channel(
                    name=channel.name, 
                    category=new_category, 
                    overwrites=overwrites, 
                    topic=channel.topic, 
                    slowmode_delay=channel.slowmode_delay, 
                    nsfw=channel.nsfw, 
                    position=channel.position
                )
            elif isinstance(channel, discord.VoiceChannel):
                await interaction.guild.create_voice_channel(
                    name=channel.name, 
                    category=new_category, 
                    overwrites=overwrites, 
                    bitrate=channel.bitrate, 
                    user_limit=channel.user_limit, 
                    position=channel.position
                )

        # Envoyer un message de confirmation en utilisant followup.send
        await interaction.followup.send(
            f"Category '{original_category.name}' and its channels duplicated successfully.", ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(DuplicateCategorySlash(bot))
