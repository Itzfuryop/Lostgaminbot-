from discord.ext import commands
import discord


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner.py is loaded")


    @commands.command(name='owner')
    @commands.is_owner()
    async def owner_test(self, ctx):
        owner_id = self.bot.owner_id
        await ctx.send(f'This command can only be used by the owner (ID: {owner_id})')



async def setup(bot):
  await bot.add_cog(Owner(bot))
