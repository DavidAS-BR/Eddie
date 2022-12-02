import commands
import discord
import pathlib
import inspect
import json
import requests
from discord.ext import commands
from googletrans import Translator

if __name__ == '__main__':
    # Lendo o arquivo com o token do BOT (ESTE ARQUIVO NÃO DEVE SER POSTADO NO GITHUB)
    # O arquivo deve ter o nome "token.json" e conter o seguinte conteúdo: {"token": "TOKEN_DO_BOT"}
    with open(pathlib.Path(__file__).parent.parent / 'data' / 'token.json', 'r') as token_file:
        token = json.load(token_file)

    # Permissão para o bot ler conteúdos de eventos de mensagem
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    # método de tradução
    translator = Translator()
    
    # Construindo o client do BOT
    client = commands.Bot(command_prefix='/',intents=intents)
    
    # Lists nessesario para alguns erros de str
    traduzP = ['ss', 'sim', 'bom', 'boa', 'legal']
    traduzI = ['yes', 'yes', 'good', 'good', 'nice']
    cErro = ['Next?', 'Good.', 'Sure.', 'Help desk', 'My dear great botmaster']
    sErro = ['Proximo?', 'Boa.', 'Claro.', 'Central de Ajuda', 'Meu querido grande mestre' ]
    eliminar = ['<tips> enquotes <\/tips>', '<tips> enJoke </tips>']

    """
    REGISTRANDO OS COMANDOS
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Registrar (chamar) aqui os comandos para que eles possam funcionar corretamente
    
    Fazendo isso de maneira automática para não precisarmos ficar alterando direto este arquivo.
    """
    cmd_list: list[commands.DiscordEvents] = []

    for command_name, command in inspect.getmembers(commands, inspect.isclass):
        assert hasattr(command, '_isdiscordevent'), "Não é um comando"

        if command.__name__ == 'DiscordEvents':
            continue

        try:
            cmd_list.append(command())
        except Exception as e:
            print(f"[{command.__name__}] Não foi registrado, algum erro ocorreu!", e)

    @client.event
    async def on_message(message):
        for cmd in cmd_list:
            await cmd.on_message(message=message)
            
        # Retornar caso o úsuario seja um BOT
        if message.author.bot == True:
            return

        # Especeficação de canais de texto que podem interagir
        if 'text' in message.channel.type:
            if message.channel.name != 'eddie_conversas':
                return

        # Traduz a mensagem recebida para Ingles
        ingles = translator.translate(message.content.lower(), dest='en').text

        # Traduz str que não foram traduzidos direito
        for a in traduzP:
            if a in ingles:
                n = traduzP.index(a)
                ingles = ingles.replace(traduzP[n], traduzI[n])

        # Enviar para API a mensagem
        rapi = requests.get(f"http://api.brainshop.ai/get?bid=170235&key=9L8K9wRRuZGGQzE0&uid=[{message.author.name}]&msg=[{ingles}]")
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

    # Executando o BOT
    client.run(token['token'])