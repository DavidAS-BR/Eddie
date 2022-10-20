import discord

from src.commands.DiscordEvents import DiscordEvents


class PingCommand(DiscordEvents):

    async def on_message(self, message: discord.Message):
        if message.content.startswith("..ping"):

            await message.channel.send("Pong!")
