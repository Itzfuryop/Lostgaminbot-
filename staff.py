import discord
from discord.ext import commands
import typing
import asyncio
from datetime import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message): 
        try:
            if ":close" in message.content:
                pass

            else:
                if str(message.channel.type) == "private":
                    return
                else:
                    if message.author == self.bot.user:
                        return  

                    else:
                        user = await message.guild.fetch_member(int(message.channel.name))
                        emb = discord.Embed(
                            title="Message from Staff",
                            description=f"{message.content}",
                            timestamp=datetime.utcnow(),
                            colour=discord.Colour.random()       
                        )
                        await user.send(embed=emb)

        except Exception as e:
            print(e)
            pass

    @commands.command()
    async def close(self, ctx):
        user = await ctx.guild.fetch_member(int(ctx.channel.name))
        await user.send("Thread has been closed")
        await ctx.send("This channel will be deleted in 5 seconds")
        await asyncio.sleep(5)
        await ctx.channel.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Staff commands are working")

    async def modify_channel_permissions(self, ctx, allow_sending, hide_channel=False):
        channel = ctx.channel
        if len(ctx.message.channel_mentions) == 1:
            # If a channel is mentioned, use that channel
            channel = ctx.message.channel_mentions[0]

        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=allow_sending, read_messages=not hide_channel)
            action = "unlocked" if allow_sending else "locked"
            visibility = "visible" if not hide_channel else "hidden"
            return f"{channel} is now {action} and {visibility}."
        except discord.Forbidden:
            return "I don't have the required permissions to manage channels."

    @commands.command(name='lock', aliases=['lockchannel', 'lock_channel'])
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        message = await self.modify_channel_permissions(ctx, allow_sending=False)
        await ctx.send(message)

    @commands.command(name='unlock', aliases=['unlockchannel', 'unlock_channel'])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        message = await self.modify_channel_permissions(ctx, allow_sending=True)
        await ctx.send(message)

    @commands.command(name='hide')
    @commands.has_permissions(manage_channels=True)
    async def hide(self, ctx):
        message = await self.modify_channel_permissions(ctx, allow_sending=True, hide_channel=True)
        await ctx.send(message)

    @commands.command(name='unhide')
    @commands.has_permissions(manage_channels=True)
    async def unhide(self, ctx):
        message = await self.modify_channel_permissions(ctx, allow_sending=True, hide_channel=False)
        await ctx.send(message)

    @commands.command(name='staff')
    async def staff_test(self, ctx):   
        await ctx.send(f'staff commands are working')
        return

    @commands.command(name='setslowmode', aliases=['sm', 'slowmodeset', 'set_slowmode'])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        if seconds < 0 or seconds > 21600:  # 6 hours maximum
            await ctx.send("Invalid slowmode duration. Please provide a value between 0 and 21600 seconds.")
            return

        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Slowmode for this channel set to {seconds} seconds.")

    @slowmode.error
    async def setslowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to manage channels.")

    @commands.command(name='clearslowmode', aliases=['csm', 'clearsm', 'removeslowmode'])
    @commands.has_permissions(manage_channels=True)
    async def clearslowmode(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send("Slowmode for this channel has been removed.")

    @clearslowmode.error
    async def remove_slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to manage channels.")

    @commands.command(name='dm')
    async def dm(self, ctx, user: discord.User, *, message):
        # Send a direct message to the mentioned user
        try:
            await user.send(message)
            await ctx.send(f'Message sent to {user.name}')
        except discord.Forbidden:
            await ctx.send('Unable to send the message. Make sure the user allows direct messages.')

    @commands.command(name='check_role', alises=['cr', 'checkrole', 'check_roles','role_members'])
    async def check_role(self, ctx, role1: typing.Union[commands.RoleConverter, int], role2: typing.Union[commands.RoleConverter, int] = None, role3: typing.Union[commands.RoleConverter, int] = None):
        # Convert role IDs to roles
        role1 = ctx.guild.get_role(role1) if isinstance(role1, int) else role1
        role2 = ctx.guild.get_role(role2) if isinstance(role2, int) else role2
        role3 = ctx.guild.get_role(role3) if isinstance(role3, int) else role3

        members_with_role1 = [member.mention for member in ctx.guild.members if role1 in member.roles]

        if role2:
            members_with_role2 = [member.mention for member in ctx.guild.members if role2 in member.roles]
            members_with_both_roles = list(set(members_with_role1) & set(members_with_role2))
            members_list = '\n'.join(members_with_both_roles)
        else:
            members_list = '\n'.join(members_with_role1)

        embed = discord.Embed(
            title='Members with the specified role(s)',
            description=members_list,
            color=discord.Colour.random()
        )

        await ctx.send(embed=embed)

    @commands.command(name='timeout', aliases=['mute'])
    async def mute(self, ctx, member: discord.Member, duration: int = 60, *, reason: str = 'No reason provided'):
        try:
            # Check if the command invoker has the necessary permissions
            if ctx.author.guild_permissions.manage_roles:
                # Find the Muted role or create it if it doesn't exist
                muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
                if muted_role is None:
                    muted_role = await ctx.guild.create_role(name='Muted', reason='Creating Muted role for timeouts', color=discord.Color.default())
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(muted_role, send_messages=False)

                # Add the Muted role to the specified member
                await member.add_roles(muted_role, reason=f'Timeout: {reason}')

                # Send a timeout message to the channel
                await ctx.send(f"{member.mention} has been timed out for {duration} seconds. Reason: {reason}")

                # Schedule the removal of the Muted role after the specified duration
                await asyncio.sleep(duration)

                # Remove the Muted role
                await member.remove_roles(muted_role, reason='Timeout duration ended')

                # Send an untimeout message to the channel
                await ctx.send(f"{member.mention} has been untimed out.")

            else:
                raise commands.CheckFailure("You don't have the necessary permissions to use this command.")
        except discord.Forbidden:
            await ctx.send("Error: The bot doesn't have the required permissions to perform this action.")
        except commands.CheckFailure as e:
            await ctx.send(f"Error: {e}")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
  await bot.add_cog(Moderation(bot))
