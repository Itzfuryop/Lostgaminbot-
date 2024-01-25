import discord
from discord.ext import commands
import random
import requests
import typing

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.blacklisted_words = ["@everyone", "@here", "@"]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} is loaded")

    @commands.command(name='say')
    async def say_command(self, ctx, *, message: str):
        if any(word in message for word in self.blacklisted_words):
            await ctx.send("Nice try.")
        else:
            await ctx.send(message)

    @commands.command(name='Word_meaning', aliases=['define', 'meaning', 'meaningof', 'meaning-of', 'define-of'], description="Search for a word's definition")
    async def search_word(self, ctx, *, word: typing.Optional[str] = None):
        if not word:
            if ctx.message.reference:
                referenced_message = await ctx.fetch_message(ctx.message.reference.message_id)
                word = referenced_message.content.strip()

        if not word:
            await ctx.send("Please provide a word to search or use this command by replying to a message.")
            return

        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and data[0].get('meanings'):
                meanings = data[0]['meanings']
                if meanings and meanings[0].get('definitions'):
                    meaning = meanings[0]['definitions'][0].get('definition')
                    await ctx.send(f"**{word.capitalize()}**: {meaning}")
                    return

        await ctx.send(f"Couldn't find the definition for '{word}'. Please check the word and try again.")

    @commands.command(name='roll', description="Roll a random number between 1 and 100")
    async def roll(self, ctx, *args):
        if not args:
            min_number, max_number = 1, 100
        elif len(args) == 1:
            try:
                max_number = int(args[0])
                if max_number < 1:
                    raise ValueError("Invalid maximum number. Please provide a positive number.")
                min_number = 1
            except ValueError:
                return await ctx.send("Please provide a valid number.")
        elif len(args) == 2:
            try:
                min_number, max_number = map(int, args)
                if min_number > max_number or min_number < 1 or max_number < 1:
                    raise ValueError("Invalid range. Please provide a valid range.")
            except ValueError:
                return await ctx.send("Please provide valid numbers for the range.")
        else:
            return await ctx.send("Too many arguments. Please provide at most two values.")

        result = random.randint(min_number, max_number)
        embed = discord.Embed(
            title=f"ROLLING BETWEEN {min_number} - {max_number}",
            description=f"{ctx.author.mention} Rolled: **{result}**",
            color=0x00ff00
        )
        await ctx.send(embed=embed)

    @commands.command(name='math', aliases=['calculate', 'calc', 'solve', 'solvemath', 'cal', 'solve-math', 'solve-calculate'], description="Solve a math problem")
    async def math(self, ctx, *, expression=None):
        if expression is None:
            await ctx.reply(f"Please provide an expression, For example `{ctx.prefix}math 2+2`.")
            return

        try:
            result = eval(expression)

            if isinstance(result, complex):
                raise ValueError("Complex numbers are not supported.")

            await ctx.reply(f"The result is: {result}")

        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")
            if "invalid syntax" in str(e).lower():
                await ctx.send("Please provide a valid mathematical expression.")

    @commands.command(name='rps', aliases=['rockpaperscissors'], description="Play rock-paper-scissors with the bot, and see if you can beat it!\nUsage: :rps [choice]\nChoices: rock, paper, scissors")
    async def rps(self, ctx, choice: str):
        choices = ['rock', 'paper', 'scissors']
        bot_choice = random.choice(choices)

        choice = choice.lower()
        if choice not in choices:
            await ctx.send("Invalid choice! Please choose 'rock', 'paper', or 'scissors'.")
            return

        result = self.determine_winner(choice, bot_choice)

        await ctx.send(f"**You chose:** {choice.capitalize()}\n**Bot chose:** {bot_choice.capitalize()}\n**Result:** {result}")

    def determine_winner(self, user_choice, bot_choice):
        if user_choice == bot_choice:
            return "It's a tie!"
        elif (
            (user_choice == 'rock' and bot_choice == 'scissors') or
            (user_choice == 'paper' and bot_choice == 'rock') or
            (user_choice == 'scissors' and bot_choice == 'paper')
        ):
            return "You won!"
        else:
            return "Bot won!"
    
async def setup(bot):
  await bot.add_cog(Fun(bot))
