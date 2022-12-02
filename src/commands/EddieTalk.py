import requests
import discord

from src.commands.DiscordEvents import DiscordEvents
from googletrans import Translator


class EddieTalk(DiscordEvents):

    async def on_message(self, message: discord.Message):

        # Retornar caso o úsuario seja um BOT
        if message.author.bot:
            return

        # Especeficação de canais de texto que podem interagir
        if 'text' in message.channel.type:
            if message.channel.name != 'eddie_conversas':
                return

        # Lists nessesario para alguns erros de str
        traduzP = ['ss', 'sim', 'bom', 'boa', 'legal']
        traduzI = ['yes', 'yes', 'good', 'good', 'nice']
        cErro = ['Next?', 'Good.', 'Sure.', 'Help desk', 'My dear great botmaster']
        sErro = ['Proximo?', 'Boa.', 'Claro.', 'Central de Ajuda', 'Meu querido grande mestre']
        eliminar = ['<tips> enquotes <\/tips>', '<tips> enJoke </tips>']

        # método de tradução
        translator = Translator()

        # Traduz a mensagem recebida para Ingles
        ingles = translator.translate(message.content.lower(), dest='en').text

        # Traduz str que não foram traduzidos direito
        for a in traduzP:
            if a in ingles:
                n = traduzP.index(a)
                ingles = ingles.replace(traduzP[n], traduzI[n])

        # Enviar para API a mensagem
        rapi = requests.get(
            f"http://api.brainshop.ai/get?bid=170235&key=9L8K9wRRuZGGQzE0&uid=[{message.author.name}]&msg=[{ingles}]")
        dados = rapi.json()
        resposta = dados.get("cnt")

        # Eliminação de certos caracteres na resposta
        for e in eliminar:
            if e in resposta:
                resposta = resposta.replace(e, '')

        # Método para não haver erros ao traduzir
        for b in cErro:
            if b in resposta:
                n = cErro.index(b)
                resposta = resposta.replace(cErro[n], sErro[n])

        # Traduz a resposta da API para portugues
        portugues = translator.translate(f'{resposta}', dest='pt').text

        # Envia a mensagem final
        await message.reply(portugues)
