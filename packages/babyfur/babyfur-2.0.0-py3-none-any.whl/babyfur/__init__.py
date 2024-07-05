from colorama import Fore, Style
import discord
from discord.ext import commands
import sys
import hypercorn.asyncio
import asyncio
from aiohttp import ClientSession
import os
from flask import Flask

"""Author's pypi package"""
bright = Style.BRIGHT
red = Fore.RED
normal = Style.NORMAL
white = Fore.WHITE


def warn(content=""):
    print(f"{red}{bright}WARNING{white}:{content}{normal}")


class Interaction:
    """
    Parameters: interaction : discord interaction
    Used to retrieve the interaction's user, send messages, send direct messages, etc.
    Usage example
    ```py
    #assuming you have all the imports and bot set up
    @bot.event
    async def on_ready():
        print("We have logged in as {0.user}".format(bot))
        #assuming we are using bot.tree.sync:
        try:
            synced = await bot.tree.sync()
            print(f'synced {len(synced)} command(s)')
        except Exception as e:
            raise e

    #make a command
    @bot.tree.command(name='testing')
    async def testing(interaction:discord.Interaction):
        user_interaction = user(interaction) # you can change user_interaction
        #eg. returning a message
        await user_interaction.send_message('hi!',ephemeral=True) # other kwargs like ephemeral are accepted

    ```
    """

    def __init__(self, interaction):
        """
        initialises the interation for usage.
        """
        self.interaction = interaction

    # commands
    async def get_id(self):
        """
        Retrieves the user ID of the interaction given.
        returns an `int`
        """
        try:
            return self.interaction.user.id
        except:
            print("Unable to retrieve user id via interaction. Please try again later.")

    async def defer(self, **kwargs):
        """
        Defers the current interaction.
        Current known `kwargs`: thinking : bool , ephemeral : bool . Both set to `False`
        Allows you to defer a message, increasing the expected response time from 3 seconds to 15 minutes.
        when deferring a message, you will require to use `interaction.followup.send()` when not in use of user() methods.
        send_message() on user() supports deferred messages.
        """
        try:
            await self.interaction.response.defer(**kwargs)
        except:
            print(
                f"{bright}{red}WARNING{white}: Unable to defer current interaction, this is likely due to the interaction already being deferred, or the interaction parameter is given as a context"
            )
            await self.interaction.response.send_message("Unable to defer message.")

    async def send_message(self, string: str = "", dms: str = False, **kwargs):
        """
        Parameters:
            `dms` : bool , set to False by default.
            `**kwargs` : other keyword arguments that `interaction.response.send_message` OR `interaction.followup.send` accepts.

        Sends a message to the target user `interaction`.
        Can be chosen to send via `dms`.
        Can include other args that `interaction.response.send_message` gives.
        """

        if dms == True:
            try:
                member_id = self.interaction.user.id
                try:
                    member = await self.interaction.guild.fetch_member(int(member_id))
                except:
                    warn(f"Unable to fetch member!")
                dm_channel = await member.create_dm()
                await dm_channel.send(content=f"{string}", **kwargs)
            except:
                await self.interaction.response.send_message(
                    content="Err: Unexpected error, Failed to send a message. This is due to there being an invalid arg. If dms are set to true, some args are invalid ( like ephemeral ). Or it may be due to your kwargs being undefined.",
                    ephemeral=True,
                )

        else:
            try:
                await self.interaction.response.send_message(
                    content=f"{string}", **kwargs
                )
            except:
                try:
                    await self.interaction.followup.send(content=f"{string}", **kwargs)
                except:
                    await self.interaction.response.send_message(
                        content="Err: Unexpected error, Failed to send a message. This is due to there being an invalid arg. If dms are part of the **kwargs, it will return an error. Or it may likely be that a part of your kwargs that you have given is undefined.",
                        ephemeral=True,
                    )

    async def create_dm(self):
        """
        Creates a direct message with that user
        use a variable to store this direct message path.
        """
        try:
            member_id = self.interaction.user.id
            try:
                member = await self.interaction.guild.fetch_member(int(member_id))
            except:
                warn("Unable to fetch member!")
            dm_channel = await member.create_dm()
            return dm_channel
        except:
            await self.interaction.response.send_message(
                content="Err: Unexpected error, Failed to retrieve user dm. This may be likely due to the user not having shared a guild with the bot.",
                ephemeral=True,
            )

    async def get_guild_id(self):
        """
        Retrieves the interaction's guild.
        """
        try:
            return self.interaction.guild.id
        except:
            try:
                await self.interaction.response.send_message(
                    content="Err: Unexpected error.", ephemeral=True
                )
            except:
                await self.interaction.followup.send_message(
                    content="Err: Unexpected error.", ephemeral=True
                )

    async def edit_message(self, string: str = "", **kwargs):
        """
        Allows message editing, only available after a message HAS been sent.
        For deferring messages, make sure that the message_id parameter IS filled out.
        The input of the string/message can be ignored.
        Accepts all `kwargs` that are needed for the message to edit
        Supports both `response` and `deferring` messages.
        """
        try:
            await self.interaction.response.edit_message(content=string, **kwargs)
        except:
            try:
                await self.interaction.followup.edit_message(content=string, **kwargs)
            except:
                try:
                    await self.interaction.response.send_message(
                        "Err: Unable to edit messages.", ephemeral=True
                    )
                except:
                    await self.interaction.followup.send(
                        "Err: Unable to edit messages.", ephemeral=True
                    )


class Context:
    """
    An easy way to use ctx prefix commands
    """

    def __init__(self, ctx):
        self.ctx = ctx

    async def send_message(self, dms: bool = False, **kwargs):
        if dms:
            member_id = self.ctx.author.id
            try:
                member = await self.ctx.guild.fetch_member(int(member_id))
            except:
                warn("Unable to fetch member!")
            dm_channel = await member.create_dm()
            await self.dm_channel.send(**kwargs)

        else:
            try:
                await self.ctx.send(**kwargs)
            except:
                raise Exception

    async def get_cog(self):
        """
        Retrieves the cog that contains the command.
        """
        return self.ctx.cog

    async def get_prefix(self):
        """
        Retrieves the prefix used to invoke the command.
        """
        return self.ctx.prefix

    async def typing_status(self):
        """
        Adds a typing status to your discord bot ( bot1234 is typing... )
        """
        await self.ctx.typing()

    async def edit_message(self, **kwargs):
        """
        Edits the message has been sent after the command has been invoked.
        Does not work if a message or reply has not been sent or the message could not be found.
        Accepts all `kwargs`, including embeds and message content
        """
        await self.ctx.edit(**kwargs)

    async def delete_message(self):
        """
        Deletes the current message that has been sent after the command has been invoked.
        Does not work if a message or reply has not been sent or the message could not be found.
        """
        try:
            await self.ctx.delete()
        except:
            warn("Unable to delete the message!")

    async def get_permissions(self):
        """
        Returns the context user's permissions
        """
        return self.ctx.permissions

    async def bot_instance(self):
        """
        Returns the bot instance
        """
        return self.ctx.bot

    async def voice_client(self):
        """
        Returns the voice client in the guild
        Only works if bot is connected to a voice channel/voice call.
        """
        return self.ctx.voice_client

    async def get_channel(self):
        """
        Returns the channel where the command was invoked in.
        """
        return self.ctx.channel

    async def get_message(self, **kwargs):
        """
        Returns a message via message ID.
        `kwargs` are accepted.
        """
        try:
            return await self.ctx.fetch_message(**kwargs)
        except:
            warn("Unable to fetch message!")
