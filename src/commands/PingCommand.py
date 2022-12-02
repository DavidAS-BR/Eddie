import discord

from src.commands.DiscordEvents import DiscordEvents


class PingCommand(DiscordEvents):

    @staticmethod
    async def on_message(message: discord.Message):
        if message.content.startswith("..ping"):

            await message.channel.send("Pong!")
