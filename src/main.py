import commands
import discord
import pathlib
import inspect
import json

if __name__ == '__main__':
    # Lendo o arquivo com o token do BOT (ESTE ARQUIVO NÃO DEVE SER POSTADO NO GITHUB)
    # O arquivo deve ter o nome "token.json" e conter o seguinte conteúdo: {"token": "TOKEN_DO_BOT"}
    with open(pathlib.Path(__file__).parent.parent / 'data' / 'token.json', 'r') as token_file:
        token = json.load(token_file)

    # Permissão para o bot ler conteúdos de eventos de mensagem
    intents = discord.Intents.default()
    intents.message_content = True

    # Construindo o client do BOT
    client = discord.Client(intents=intents)

    """
    REGISTRANDO OS COMANDOS
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Registrar (chamar) aqui os comandos para que eles possam funcionar corretamente
    
    Fazendo isso de maneira automática para não precisarmos ficar alterando direto este arquivo.
    """
    for command_name, command in inspect.getmembers(commands, inspect.isclass):
        assert hasattr(command, '_isdiscordevent'), "Não é um comando"

        if command.__name__ == 'DiscordEvents':
            continue

        try:
            command(client)
        except Exception as e:
            print(f"[{command.__name__}] Não foi registrado, algum erro ocorreu!", e)

    # Executando o BOT
    client.run(token['token'])
