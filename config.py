from environs import Env
from dataclasses import dataclass

@dataclass
class Token:
    bot_token: str
    bard_token: str = None
    
def pars_bard_token():
    pass
    
def get_config():
    env = Env()
    env.read_env(".env")
    return Token(
        env.str("BOT_TOKEN"),
        pars_bard_token()
    )