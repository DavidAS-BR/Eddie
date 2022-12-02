import discord

from src.commands.DiscordEvents import DiscordEvents


class HelloCommand(DiscordEvents):

    async def on_message(self, message: discord.Message):
        if message.content.startswith("..hello"):

            await message.channel.send("hi!")
