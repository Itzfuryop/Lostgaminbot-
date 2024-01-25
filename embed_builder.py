from discord.ext import commands
import discord

class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create_embed')
    async def create_embed(self, ctx, *, args):
        # Split the input into title, description, and footer
        parts = args.split(', ')
        
        # Extract values from the split parts
        title = description = footer = None
        for part in parts:
            key, value = part.split('=')
            if key == 'title':
                title = value
            elif key == 'description':
                description = value
            elif key == 'footer':
                footer = value
        
        # Create and send the embed
        embed = discord.Embed(title=title, description=description)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

async def setup(bot):
  await bot.add_cog(Embeds(bot))
          