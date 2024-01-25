import discord
from discord.ext import commands

class EmbedCopier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore messages from bots

        if message.reference and message.reference.cached_message:
            referenced_message = message.reference.cached_message
            content_lower = message.content.lower()

            if content_lower.startswith(",send_proof"):
                # Extracting the target channel from the command
                command_parts = content_lower.split()
                if len(command_parts) < 3:
                    await message.channel.send("Please specify the target channel using a mention, ID, or name.")
                    return

                target_channel_reference = command_parts[2]

                # Try to find the target channel
                target_channel = None

                # Check if the target is a mention
                if target_channel_reference.startswith("<#") and target_channel_reference.endswith(">"):
                    target_channel_id = int(target_channel_reference[2:-1])
                    target_channel = message.guild.get_channel(target_channel_id)

                # Check if the target is an ID
                elif target_channel_reference.isdigit():
                    target_channel = message.guild.get_channel(int(target_channel_reference))

                # Check if the target is a name
                else:
                    target_channel = discord.utils.get(message.guild.channels, name=target_channel_reference)

                if not target_channel:
                    await message.channel.send(f"Target channel '{target_channel_reference}' not found.")
                    return

                if referenced_message.author.bot and referenced_message.embeds:
                    embed_to_copy = referenced_message.embeds[0]

                    try:
                        # Send the copied embed using ctx
                        await target_channel.send(embed=embed_to_copy)
                        await message.channel.send(f"{message.author.mention} Your proof has been sent to {target_channel.mention}!")
                    except discord.Forbidden:
                        await message.channel.send(f"I don't have permission to send messages in {target_channel.mention}.")
                else:
                    await message.channel.send("Invalid proof format. Make sure to reply to a bot's embed.")
                return  # Stop further processing to avoid duplicate responses

async def setup(bot):
  await bot.add_cog(EmbedCopier(bot))
  print("EmbedCopier.py is loaded")
