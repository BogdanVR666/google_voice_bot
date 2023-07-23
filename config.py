from environs import Env
from dataclasses import dataclass

env = Env()
env.read_env(".env")

@dataclass
class Token:
    bot_token: str
    bard_token: str
    
def pars_bard_token():
    return (
        env.str("BARD_TOKEN")
    )
    
def get_config():
    return Token(
        env.str("BOT_TOKEN"),
        pars_bard_token()
    )