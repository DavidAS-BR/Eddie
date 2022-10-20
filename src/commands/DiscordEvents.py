import discord


class DiscordEvents:
    def __init__(self):

        print(f"[{self.__class__.__name__}] Registrado com sucesso!")

    @staticmethod
    async def on_message(message: discord.Message):
        """Função que será executada em todos os comandos toda vez que o BOT receber uma nova mensagem

        :param message:
        :return:
        """
        pass

    @staticmethod
    def _isdiscordevent():
        return True
