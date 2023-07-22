from bardapi import Bard
from environs import Env

env = Env()
env.read_env(".env")

bot_token = env.str("BOT_TOKEN")
bard_token = env.str("BARD_TOKEN")

bard = Bard(bard_token)

def tts(text: str) -> None:
    with open("bard_speech.ogg", "wb") as file:
        file.write(bard.speech(text))