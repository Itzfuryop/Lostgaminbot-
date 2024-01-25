import discord
from discord.ext import commands
import datetime

class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    GUILD_ID = 1153533613195935775

    @commands.Cog.listener(name='on_message')
    async def on_message(self, message):
        if str(message.channel.type) == "private":
            if message.author == self.bot.user:
                return

            else:
                guild = self.bot.get_guild(self.GUILD_ID)
                channels = await guild.fetch_channels()  # Changed from guild.fetch_channels() to await guild.fetch_channels()
                channel = discord.utils.get(channels, name=str(message.author.id))

                if channel is None:
                    category = discord.utils.get(guild.categories, name="Modmail")
                    channel = await guild.create_text_channel(name=str(message.author.id), category=category)

                    await message.author.send("Your thread has been created successfully")
                    em = discord.Embed(
                        title=f"{message.author.name}#{message.author.discriminator}",
                        description=f"{message.content}",
                        timestamp=datetime.datetime.utcnow(),
                        colour=discord.Colour.random()
                    )
                    await channel.send(embed=em)

                else:
                    em = discord.Embed(
                        title=f"{message.author.name}#{message.author.discriminator}",
                        description=f"{message.content}",
                        timestamp=datetime.datetime.utcnow(),
                        colour=discord.Colour.random()
                    )
                    await channel.send(embed=em)


async def setup(bot):
    await bot.add_cog(Modmail(bot))
