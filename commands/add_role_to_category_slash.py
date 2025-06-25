import discord
from discord import app_commands
from discord.ext import commands

class AddRoleToCategorySlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="add_role_to_category", description="Add a role to all channels in a category with all permissions denied")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_role_to_category(self, interaction: discord.Interaction, category_id: str, role_id: str):
        await interaction.response.send_message("Command received. The process is running, please wait...", ephemeral=True)

        # Conversion des IDs en entiers
        try:
            category_id = int(category_id)
            role_id = int(role_id)
        except ValueError:
            await interaction.followup.send("Invalid category ID or role ID. Please provide valid numbers.", ephemeral=True)
            return

        # Vérifier si la catégorie existe
        category = discord.utils.get(interaction.guild.categories, id=category_id)
        if not category:
            await interaction.followup.send(f"No category found with ID '{category_id}'.", ephemeral=True)
            return

        # Vérifier si le rôle existe
        role = discord.utils.get(interaction.guild.roles, id=role_id)
        if not role:
            await interaction.followup.send(f"No role found with ID '{role_id}'.", ephemeral=True)
            return

        # Créer les permissions avec tout en False par défaut
        denied_permissions = discord.PermissionOverwrite(
            # Permissions générales
            view_channel=False,
            manage_channels=False,
            manage_permissions=False,
            manage_webhooks=False,
            create_instant_invite=False,
            
            # Permissions de messages texte
            send_messages=False,
            send_messages_in_threads=False,
            create_public_threads=False,
            create_private_threads=False,
            embed_links=False,
            attach_files=False,
            add_reactions=False,
            use_external_emojis=False,
            use_external_stickers=False,
            mention_everyone=False,
            manage_messages=False,
            read_message_history=False,
            send_tts_messages=False,
            use_application_commands=False,
            
            # Permissions vocales
            connect=False,
            speak=False,
            mute_members=False,
            deafen_members=False,
            move_members=False,
            use_voice_activation=False,
            priority_speaker=False,
            stream=False,
            use_embedded_activities=False,
            use_soundboard=False,
            use_external_sounds=False,
            
            # Permissions de stage
            request_to_speak=False,
            manage_events=False,
            use_external_apps=False,
            send_polls=False,
            send_voice_messages=False,
            manage_threads=False,
        )

        channels_updated = 0
        errors = []

        # D'abord, ajouter le rôle à la catégorie elle-même
        try:
            await category.set_permissions(role, overwrite=denied_permissions)
        except discord.Forbidden:
            errors.append(f"Missing permissions for category '{category.name}'")
        except Exception as e:
            errors.append(f"Error in category '{category.name}': {str(e)}")

        # Ensuite, ajouter le rôle à tous les salons de la catégorie
        for channel in category.channels:
            try:
                await channel.set_permissions(role, overwrite=denied_permissions)
                channels_updated += 1
            except discord.Forbidden:
                errors.append(f"Missing permissions for '{channel.name}'")
                continue
            except Exception as e:
                errors.append(f"Error in '{channel.name}': {str(e)}")
                continue

        # Message de confirmation
        success_message = f"Role '{role.name}' added to category '{category.name}' and {channels_updated} channels with all permissions denied by default."
        
        if errors:
            error_message = f"\n\nErrors encountered:\n" + "\n".join(errors[:5])  # Limiter à 5 erreurs pour éviter les messages trop longs
            if len(errors) > 5:
                error_message += f"\n... and {len(errors) - 5} more errors."
            success_message += error_message

        await interaction.followup.send(success_message, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AddRoleToCategorySlash(bot))