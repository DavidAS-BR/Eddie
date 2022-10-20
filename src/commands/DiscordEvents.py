import discord


class DiscordEvents:
    def __init__(self, client: discord.Client):
        self.client = client

        client.event(self.on_message)

        print(f"[{self.__class__.__name__}] Registrado com sucesso!")

    async def on_message(self, message: discord.Message):
        pass

    @staticmethod
    def _isdiscordevent():
        return True


