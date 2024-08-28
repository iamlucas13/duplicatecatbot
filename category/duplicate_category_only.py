import discord
from discord.ext import commands

def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

@commands.command()
@is_admin()
async def duplicate_category_only(ctx, category_id: int):
    await ctx.send("Command received. The process is running, please wait...")

    original_category = discord.utils.get(ctx.guild.categories, id=category_id)
    if not original_category:
        await ctx.send(f"No category with ID '{category_id}' found.")
        return

    new_category = await ctx.guild.create_category(name=f"{original_category.name} - copy", overwrites=original_category.overwrites)

    for role, permissions in original_category.overwrites.items():
        await new_category.set_permissions(role, overwrite=permissions)

    await ctx.send(f"Category '{original_category.name}' duplicated successfully without channels.")
