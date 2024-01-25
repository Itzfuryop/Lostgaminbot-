import os
import random
import keep_alive
import asyncio
import discord
from discord.ext import commands

def get_prefix(bot, message):
    prefixes = ['$'] 
    if message.guild is None: 
        return commands.when_mentioned_or(*prefixes)(bot, message)

    return commands.when_mentioned_or(*prefixes)(bot, message)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)
token = os.environ['TOKEN']

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
           await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    try:
        await load()
        await bot.start(os.environ['TOKEN'])
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await bot.close()

class CustomHelpCommand(commands.DefaultHelpCommand):
  async def send_command_help(self, command):
      embed = discord.Embed(
          title=f"Help for {command.name}",
          description=command.description or "No help available.",
          color=discord.Color.blue()
      )
      await self.get_destination().send(embed=embed)

  async def send_bot_help(self, mapping):
      embed = discord.Embed(
          title="Command List",
          description="Here is a list of all available commands:",
          color=discord.Color.blue()
      )

      for cog, commands_list in mapping.items():
          if not commands_list:
              continue

          command_signatures = [f"{self.context.clean_prefix}{command.qualified_name}" for command in commands_list]
          cog_name = getattr(cog, "qualified_name", "No Category")

          embed.add_field(name=cog_name, value=", ".join(command_signatures), inline=False)

      await self.get_destination().send(embed=embed)

# Set the custom help command
bot.help_command = CustomHelpCommand()


@bot.command()
async def main_test(ctx):
    await ctx.message.reply("main.py is loaded and working.")
keep_alive.keep_alive()
asyncio.run(main())