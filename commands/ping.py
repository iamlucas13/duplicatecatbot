import discord
from discord.ext import commands  

class PingCommand(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="A simple ping command")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PingCommand(bot))
