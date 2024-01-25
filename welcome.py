import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = 1199422991373713609  # Replace with your desired channel ID

        channel = self.bot.get_channel(channel_id)
        if channel is None:
            print(f"Error: Channel with ID {channel_id} not found.")
            return

        try:
            embed = discord.Embed(
                title=f"Welcome {member.name}!",
                description=f"Welcome to the server {member.mention}! We hope you enjoy your stay!",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"You are the {len(list(member.guild.members))}th member of the server")
            embed.set_thumbnail(url="https://files.shapes.inc/c78950b8.png")
            embed.set_image(url="https://tenor.com/view/welcome-cat-cute-gif-13266078267237062818")

            role = discord.utils.get(member.guild.roles, name="Member")
            if role is not None:
                await member.add_roles(role)

            print("Welcome message sent!")
            await channel.send(embed=embed)

        except Exception as e:
            print(f"An error occurred: {e}")

async def setup(bot):
  await bot.add_cog(Welcome(bot))
