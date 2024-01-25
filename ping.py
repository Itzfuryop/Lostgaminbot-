from discord.ext import commands
import discord

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='on_ready')
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type = discord.ActivityType.playing, name="DM ME TO CONTACT STAFF"))
        print(f"{self.bot.user} is online")
      
      
    @commands.command(name='ping')
    async def ping(self, ctx):      
        latency = round(self.bot.latency * 1000)  
        await ctx.send(f'Pong! `{latency}ms` latency.')

async def setup(bot):
  await bot.add_cog(Ping(bot))