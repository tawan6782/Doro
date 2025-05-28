import discord
import os
import random
import asyncio
import aiohttp
from discord import FFmpegPCMAudio
from keep_alive import keep_alive

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Global state variables
is_sleeping = True

# Predefined responses for Doro
falas_doro = [
    "Doro!", "DORO DORO", "Doro?", "Doro......",
    "Dorodorodorodorodorodorodorodoro", "# DORO", "d o r o", "*doro*",
    "**DORO?!**", "doroooooooooooooo", "D.o.r.o.", "d o r o ?", "d-Doro...",
    "DoRoDoRoDoRo", "dorodododorododoro", "💥 DORO 💥",
    "doro.exe has stopped working", "> Doro está digitando...",
    "🧠 DORO THOUGHTS 🧠", "D-O-R-O", "doro (em choque)", "doro: o retorno",
    "doro v2.0", "Doro...? DORO!! DOROOOOOO!!", "doro... doro... doro...",
    "D O R O", "doro doro doro doro doro doro doro doro doro doro doro",
    "*DORO ESTÁ ENTRE NÓS*", "Dorororororororororororororororororo!",
    "Doro entrou no chat.", "Doro saindo do servidor... adeus.",
    "Doro foi banida por excesso de Doro.", "⚠️ ALARME DE DORO ⚠️",
    "Dorantástico!", "💣💣**DORO!**💣💣",
    "Você já parou pra pensar... que talvez tudo seja Doro?", "doro :3",
    "# **DORO ACTIVATED**",
    "doro doro? doro doro! DORO!!! doro https://c.tenor.com/aDdEI4la1V0AAAAd/tenor.gif",
    "~doro~", "ドロ ドロ ドロ ドロ ドロ"
]

# GIF URLs for Doro responses
gifs_doro = [
    "https://tenor.com/view/doro-gif-1748499123257475241",
    "https://cdn.discordapp.com/attachments/1273933801860366348/1371509159584993430/s.gif",
    "https://i.redd.it/d4fjkyrwjkid1.gif",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374538002243522640/1fi2qb1iu9yb1.png?ex=6833afc5&is=68325e45&hm=e856ecc7c56241403324a2600897d73973151a96ee1e90f915da64a465368229&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374543223745151037/222a7uciafie1.gif?ex=6833b4a2&is=68326322&hm=65b64230c52e8ce47f0123d40b1168c01821d1376e1a1c90427821c049d29b42&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374543223405416458/a8ghchaqafie1.gif?ex=6833b4a2&is=68326322&hm=3a77185ea49aa8835dcbc305f3c9e4e8c09126d58d5c6d3e2dc7e17e3753637b&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374543223061614715/r92v8l72bfie1.gif?ex=6833b4a2&is=68326322&hm=4ccaa12a8d79b18d4e24ca0c69ce297cfb573f7f4efb19e60197080d9a57fe0a&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374543224106127450/6icng4sis84e1.gif?ex=6833b4a2&is=68326322&hm=5d845b79d6038ee7b9b201f01049b897820876e008888c766e2c089263f6b014&",
    "https://c.tenor.com/sV9KcBQ_xlcAAAAd/tenor.gif",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374540077514100809/67c02629a06991QJ.gif?ex=6833b1b4&is=68326034&hm=fcb4ce861f0cba52caf0c565c5da10486a1fc864863ec2521ce4c8b78a9ce3ce&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374264845280481322/doro_elegante.gif?ex=68335a1f&is=6832089f&hm=4e13cad8459e12aab98397144079c825e2a92f69e4ea428ad58e024756d8d0e9&",
    "https://cdn.discordapp.com/attachments/803745174886678599/1352135656565899275/IMG_6281.gif?ex=68334435&is=6831f2b5&hm=508670f44b1a1b53d8268909aebf6cf14a593536ce29d0ad4a705890e33409bb&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374537057388593202/Dorosaur.gif?ex=6833aee4&is=68325d64&hm=6b33d6b32842b2381e4f7b188130b70af76f226b6b0711b2ba5aace366ad26ad&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374271786710995104/05054-ezgif.com-speed.gif?ex=68336096&is=68320f16&hm=5111805097cc8e257f7e55da6d05963136c7de500643cb7b6c5b1bd5ad01e423&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374533653534871683/hooyg8l4420f1.gif?ex=6833abb8&is=68325a38&hm=1f608272d379547420382d5b6120e69160761355c0f69c2dbab3aa0b072a1c5a&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374533587285839966/HnVideoEditor_2025_05_17_074702035.gif?ex=6833aba8&is=68325a28&hm=89c61176f5e00a4d61c3b48e50f9bdb1a6ef3074accad4b40def767862433c5a&",
    "https://cdn.discordapp.com/attachments/525224345514147842/1348974746364153967/IMG_3514.gif?ex=6833a1e2&is=68325062&hm=98e20e9c16c4433d135312c2acfa79be70d6b13d623592c414b30522c41baf73&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1371196568421662830/IMG_5055.gif?ex=68336551&is=683213d1&hm=174135ba02ddfc68db45a575e59232cae325544985c3f4fa2180fab22dc4ee96&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1372797570879066183/editoro8-ezgif.com-video-to-gif-converter.gif?ex=6833499e&is=6831f81e&hm=2eb055c4c5d1d3255ec31ee5b6aedb2a6e2b9d5e5622c544b75cb46962549e52&",
    "https://cdn.discordapp.com/attachments/603549683897597952/1373508856117858345/HnVideoEditor_2025_05_18_083250977-ezgif.com-loop-count.gif?ex=68333d0d&is=6831eb8d&hm=08a42ec1b91c49313d1d62a658ceaea4242612d5631804ddc2941fd061ee18d2&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1341091403425644574/IMG_4712.gif?ex=68334c32&is=6831fab2&hm=3c541e4e4db0a0c32b38fe3c99da7577e0a9ac37bf29b8156d94b963331d6563&",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1356553156397633669/IMG_5373.gif?ex=68338454&is=683232d4&hm=1ea4919616271dad47e53768acf919dff97eba082ea1a62bfb4946d9df704320&",
    "https://cdn.discordapp.com/attachments/1340040586232598538/1359782702714458193/IMG_5554.gif?ex=68336693&is=68321513&hm=3fad226af02a5a33468f1cc7df5e1a027b5a7f65efb6c701a2f728818909b16e&",
    "https://c.tenor.com/aDdEI4la1V0AAAAd/tenor.gif",
    "https://tenor.com/view/doro-nikke-middle-finger-funny-gif-9412621914012263607",
    "https://tenor.com/view/doro-dorothy-fat-doritos-nikke-gif-3638811687278101957",
    "https://tenor.com/view/dorothy-nikke-doro-gif-7509545823082567005",
    "https://cdn.discordapp.com/attachments/1273933998762229845/1374534306516439111/doro-made-a-drink-for-you-how-nice-v0-ipjcl6hu95zb1.png?ex=6833ac54&is=68325ad4&hm=77660fb34086e12db36a4e625810889665e863c76376a7f8a4e671843a425af2&",
    "https://tenor.com/view/doro-dorothy-nikke-gif-3492096921929364235"
]

# Good morning GIFs
gifs_bom_dia = [
    "https://cdn.discordapp.com/attachments/1060437247524077608/1355851381902147705/0742422FA27C6A6C9663A71F9F25F7C1.gif",
    "https://media.discordapp.net/attachments/634987495712358400/1302236316477685780/doro_rise.gif"
]

# Emojis for image reactions
image_reaction_emojis = [
    '😍', '🤩', '😎', '🥳', '😂', '🤣', '😭', '😱', '🤯', '🔥', '💯', '👀', '👍', '👎', '❤️',
    '💖', '💕', '🤗', '😊', '😏', '🤭', '🙄', '😬', '🤔', '🧐', '😳', '🥺', '😌', '🤤', '🤡',
    '👻', '💀', '⭐', '✨', '💥', '💫', '🌟', '🎉', '🎊', '🙏'
]


async def get_league_of_legends_image():
    """
    Fetch a random League of Legends image from Danbooru API.
    Returns the image URL or None if failed.
    """
    try:
        async with aiohttp.ClientSession() as session:
            # Search for random posts with League of Legends tags
            url = "https://danbooru.donmai.us/posts.json"
            params = {
                'limit': 20,
                'tags':
                'league_of_legends rating:safe',  # League of Legends content only, safe rating
            }

            print(
                f"Tentando buscar imagem do League of Legends no Danbooru...")

            async with session.get(url, params=params) as response:
                print(f"Status da resposta Danbooru (LoL): {response.status}")

                if response.status == 200:
                    posts = await response.json()
                    print(
                        f"Encontrados {len(posts)} posts do League of Legends")

                    if posts and len(posts) > 0:
                        # Seleciona um post aleatório dos resultados
                        post = random.choice(posts)

                        # Tenta diferentes campos de URL
                        for url_field in [
                                'file_url', 'large_file_url',
                                'preview_file_url'
                        ]:
                            if url_field in post and post[url_field]:
                                image_url = post[url_field]
                                print(
                                    f"URL da imagem do LoL encontrada: {image_url}"
                                )
                                return image_url

                        print("Nenhuma URL válida encontrada no post do LoL")
                else:
                    print(f"Erro da API Danbooru (LoL): {response.status}")
    except Exception as e:
        print(f"Error fetching League of Legends image: {e}")

    return None


async def get_random_danbooru_image():
    """
    Fetch a random image from Danbooru API.
    Returns the image URL or None if failed.
    """
    try:
        async with aiohttp.ClientSession() as session:
            # Search for random posts with safe tags
            url = "https://danbooru.donmai.us/posts.json"
            params = {
                'limit': 20,
                'tags': 'rating:safe',  # Only safe content
            }

            print(f"Tentando buscar imagem do Danbooru...")

            async with session.get(url, params=params) as response:
                print(f"Status da resposta Danbooru: {response.status}")

                if response.status == 200:
                    posts = await response.json()
                    print(f"Encontrados {len(posts)} posts do Danbooru")

                    if posts and len(posts) > 0:
                        # Seleciona um post aleatório dos resultados
                        post = random.choice(posts)

                        # Tenta diferentes campos de URL
                        for url_field in [
                                'file_url', 'large_file_url',
                                'preview_file_url'
                        ]:
                            if url_field in post and post[url_field]:
                                image_url = post[url_field]
                                print(f"URL da imagem encontrada: {image_url}")
                                return image_url

                        print("Nenhuma URL válida encontrada no post")
                else:
                    print(f"Erro da API Danbooru: {response.status}")
    except Exception as e:
        print(f"Error fetching Danbooru image: {e}")

    return None


@client.event
async def on_ready():
    """Event triggered when the bot is ready and connected."""
    print(f'Bot conectado como {client.user}')
    await client.change_presence(status=discord.Status.invisible)
    # Start the voice channel monitoring task
    client.loop.create_task(check_voice_channel())


async def check_voice_channel():
    """
    Continuously monitors voice channels to:
    1. Disconnect if alone in a voice channel
    2. Play random audio at intervals when others are present
    """
    while True:
        try:
            for guild in client.guilds:
                if guild.voice_client:
                    channel = guild.voice_client.channel
                    # Disconnect if alone in voice channel
                    if len(channel.members) <= 1:
                        await guild.voice_client.disconnect()
                        print(
                            f"Disconnected from {channel.name} - alone in channel"
                        )
                    else:
                        # Play random audio if not currently playing
                        if not guild.voice_client.is_playing():
                            # Random delay between 5-30 minutes
                            delay = random.randint(300, 1800)
                            await asyncio.sleep(delay)

                            # Check if still connected and others are present
                            if guild.voice_client and len(channel.members) > 1:
                                sound_file = f'Sounds/doro{random.randint(1, 10)}.ogg'
                                if os.path.exists(sound_file):
                                    try:
                                        source = FFmpegPCMAudio(sound_file)
                                        guild.voice_client.play(source)
                                        print(
                                            f"Playing {sound_file} in {channel.name}"
                                        )
                                    except Exception as e:
                                        print(f"Error playing audio: {e}")
                                else:
                                    print(f"Audio file {sound_file} not found")
        except Exception as e:
            print(f"Error in check_voice_channel: {e}")

        await asyncio.sleep(5)


@client.event
async def on_message(message):
    """Handle incoming messages and respond based on content."""
    global is_sleeping

    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    conteudo = message.content.lower()
    print(
        f"DEBUG: Mensagem recebida: '{message.content}' -> processada como: '{conteudo}'"
    )

    try:
        # Special response for "doro lol" - League of Legends images (check first)
        if 'doro lol' in conteudo:
            print(
                f"DEBUG: Comando 'doro lol' detectado! Conteúdo da mensagem: '{conteudo}'"
            )
            try:
                print("Tentando buscar imagem do League of Legends...")
                danbooru_image = await get_league_of_legends_image()
                if danbooru_image:
                    sent_message = await message.channel.send(
                        f"DORO LOL"! {danbooru_image}")

                    # Reage à própria mensagem com emojis aleatórios
                    try:
                        # Escolhe 1-2 emojis aleatórios para reagir
                        num_reactions = random.randint(1, 2)
                        chosen_emojis = random.sample(
                            image_reaction_emojis,
                            min(num_reactions, len(image_reaction_emojis)))

                        for emoji in chosen_emojis:
                            await sent_message.add_reaction(emoji)
                            await asyncio.sleep(
                                0.5)  # Pequeno delay entre reações
                    except Exception as e:
                        print(f"Erro ao reagir à própria mensagem: {e}")
                else:
                    await message.channel.send(
                        "Doro não conseguiu encontrar uma imagem do LoL... 😔")
            except Exception as e:
                print(f"Erro ao buscar imagem do League of Legends: {e}")
                await message.channel.send(
                    "Doro deu erro tentando buscar LoL... 😵")
            return

        # Special response for "doro hentai"
        elif 'doro hentai' in conteudo:
            # 50% chance to fetch from Danbooru, 50% chance for regular response
            if random.randint(1, 100) <= 50:
                try:
                    print("Tentando buscar imagem do Danbooru...")
                    danbooru_image = await get_random_danbooru_image()
                    if danbooru_image:
                        sent_message = await message.channel.send(
                            f"Doro encontrou isso! {danbooru_image}")

                        # Reage à própria mensagem com emojis aleatórios
                        try:
                            # Escolhe 1-2 emojis aleatórios para reagir
                            num_reactions = random.randint(1, 2)
                            chosen_emojis = random.sample(
                                image_reaction_emojis,
                                min(num_reactions, len(image_reaction_emojis)))

                            for emoji in chosen_emojis:
                                await sent_message.add_reaction(emoji)
                                await asyncio.sleep(
                                    0.5)  # Pequeno delay entre reações
                        except Exception as e:
                            print(f"Erro ao reagir à própria mensagem: {e}")

                        return
                    else:
                        print(
                            "Danbooru não retornou imagem, usando resposta padrão"
                        )
                except Exception as e:
                    print(f"Erro ao buscar imagem do Danbooru: {e}")

            # Default response
            await message.channel.send(
                "https://media.discordapp.net/stickers/1291711474917445673.gif"
            )
            return

        # Special "libertar carga" command sequence
        elif message.content.lower().startswith("doro libertar carga"):
            await message.channel.send("⚠️ ***Sobrecarga detectada...***")
            await asyncio.sleep(3)
            await message.channel.send(
                "💓 *Pressurizando reservatório de dados...*")
            await asyncio.sleep(4)
            await message.channel.send(
                "💦💥 *EJACULANDO PACOTES BINÁRIOS EM DIREÇÃO AO PLANO MATERIAL!!!*"
            )
            return

        # Alternative hentai command
        elif 'doro hental' in conteudo:
            await message.channel.send(
                "https://cdn2.hentaigifz.com/93580/hardfuck.gif")
            return

        # Good night commands
        elif any(kw in conteudo for kw in [
                'boa noite doro', 'doro boa noite', 'dorme doro',
                'vai dormir doro'
        ]):
            if not is_sleeping:
                await message.channel.send(
                    "https://cdn.discordapp.com/attachments/1238539497537540137/1375663363140354128/image.png"
                )
                is_sleeping = True
                await client.change_presence(status=discord.Status.invisible)
            return

        # Good morning commands
        elif any(kw in conteudo for kw in [
                'doro bom dia', 'doro bomdia', 'bom dia doro', 'bomdia doro',
                'acorda doro', 'doro acorda'
        ]):
            is_sleeping = False
            await client.change_presence(status=discord.Status.online)
            await message.channel.send(random.choice(gifs_bom_dia))
            return

        # Kill command
        elif 'doro kill' in conteudo:
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/1273933801860366348/1365152597337444433/sk6knfnktlmd1.gif"
            )
            return

        # Hostile commands
        elif any(x in conteudo for x in [
                'morre doro', 'vai se foder doro', 'vai se fude doro',
                'doro se mata', 'se mata doro'
        ]):
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/684383483640152094/1375662630097915914/image.png"
            )
            return

        # Join voice channel command
        elif 'entra doro' in conteudo and not is_sleeping:
            if message.author.voice:
                channel = message.author.voice.channel
                try:
                    # Disconnect from current channel if connected elsewhere
                    if message.guild.voice_client:
                        await message.guild.voice_client.disconnect()

                    voice_client = await channel.connect()
                    sound_file = f'Sounds/doro{random.randint(1, 10)}.ogg'

                    if os.path.exists(sound_file):
                        source = FFmpegPCMAudio(sound_file)
                        voice_client.play(source)
                        await message.channel.send("DORO! 🎵")
                    else:
                        await message.channel.send(
                            "DORO! 🎵 (audio file not found)")

                except Exception as e:
                    print(f"Erro ao entrar na call: {e}")
                    await message.channel.send(
                        f"Erro ao entrar no canal: {str(e)}")
                    if message.guild.voice_client:
                        await message.guild.voice_client.disconnect()
            else:
                await message.channel.send(
                    "Você precisa estar em um canal de voz primeiro!")
            return

        # Leave voice channel command
        elif 'sai doro' in conteudo:
            if message.guild.voice_client:
                await message.guild.voice_client.disconnect()
                await message.channel.send("Tchau... 👋")
            else:
                await message.channel.send(
                    "Eu não estou em nenhum canal de voz!")
            return

        # Question mark reaction
        elif 'doro?' in conteudo:
            emojis = [
                '👀', '❓', '🧐', '😳', '🤨', '😶', '👍', '👎', '❤️', '🔥', '🤭', '🐂',
                '🙏', '🤫'
            ]
            emoji = random.choice(emojis)
            await message.add_reaction(emoji)
            return

        # Check for image attachments and react with 50% chance
        if message.attachments:
            for attachment in message.attachments:
                # Check if attachment is an image
                if any(attachment.filename.lower().endswith(ext) for ext in
                       ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp']):
                    # 50% chance to react to images
                    if random.randint(1, 100) <= 50:
                        try:
                            # Choose 1-3 random emojis to react with
                            num_reactions = random.randint(1, 3)
                            chosen_emojis = random.sample(
                                image_reaction_emojis,
                                min(num_reactions, len(image_reaction_emojis)))

                            for emoji in chosen_emojis:
                                await message.add_reaction(emoji)
                                # Small delay between reactions to avoid rate limiting
                                await asyncio.sleep(0.5)
                        except Exception as e:
                            print(f"Error reacting to image: {e}")
                    return

        # 10% chance to respond "doro" to any message (before general doro responses)
        elif random.randint(1, 100) <= 10:
            await message.channel.send("doro")
            return

        # General "doro" mentions - random response
        elif 'doro' in conteudo:
            if not is_sleeping:
                escolha = random.choice(falas_doro + gifs_doro)
                await message.channel.send(escolha)
            return

    except Exception as e:
        print(f"Error handling message: {e}")
        # Don't send error messages to users to avoid spam


def main():
    """Main function to start the bot."""
    # Start the keep-alive server
    keep_alive()

    # Get Discord token from environment variable
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("ERROR: DISCORD_TOKEN environment variable not set!")
        print(
            "Please set your Discord bot token in the environment variables.")
        return

    try:
        # Run the Discord bot
        client.run(token)
    except discord.LoginFailure:
        print("ERROR: Invalid Discord token!")
    except Exception as e:
        print(f"ERROR: Failed to start bot: {e}")


if __name__ == "__main__":
    main()
