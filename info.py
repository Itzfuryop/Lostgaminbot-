from discord.ext import commands
import discord

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Info.py is loaded")

    @commands.command(name='Botinfo', aliases=['botinfo', 'bi'])
    async def botinfo(self, ctx):
        try:
            embed = discord.Embed(title='Bot Information', description=f'Hey, I am a bot made by <@!1076116730620940298> for support-related commands and generally used commands. Thank you for using this bot. If you have any suggestions, please let us know about it by using `{ctx.prefix}suggest <suggestion>` or if you wanna report a bug, please report it by using `{ctx.prefix}report <bug details>`', color=discord.Color.blue())
            embed.add_field(name='Bot Name', value=self.bot.user.name)
            embed.add_field(name='Bot ID', value=self.bot.user.id)
            embed.add_field(name='Bot Owner', value='<@!1135912361664979055>')
            embed.add_field(name='Bot Developer', value='<@!709998479732113429>')
            embed.add_field(name='Bot Prefix', value=f'`{ctx.prefix}`')
            embed.add_field(name='Bot Library', value='discord.py')
            
            embed.add_field(name='Official server', value='[Click Here](https://discord.gg/YcRbXjurf7)')
            embed.set_thumbnail(url='https://files.shapes.inc/c78950b8.png')
            embed.set_footer(text='Thanks for using me!')

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            await ctx.send("An error occurred while sending the bot information. Please try again later.")

async def setup(bot):
  await bot.add_cog(Info(bot))
