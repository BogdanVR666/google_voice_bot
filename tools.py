import aiohttp
from environs import Env
from dataclasses import dataclass
from fake_useragent import FakeUserAgent
from aiogram.filters import BaseFilter
from aiogram.types import InlineQuery


@dataclass
class Config:
    bot_token: str
    service_chat_id: str
    admin_ids: list
    email: str
    password: str


def get_config() -> Config:
    env = Env()
    env.read_env(".env")
    return Config(
        bot_token=env.str("BOT_TOKEN"),
        service_chat_id=env.str("SERVICE_CHAT_ID"),
        admin_ids=[int(i) for i in env.list("ADMIN_IDS")],
        email=env.str("EMAIL"),
        password=env.str("PASSWORD")
    )

# For host 
async def login(email: str, password: str):
    async with aiohttp.ClientSession(headers=FakeUserAgent().random) as ses:
        async with ses.post(
            "https://accounts.google.com/signin/v2/identifier",
            data={
                "identifier": email, 
                "password": password}
        ) as res:
            return res.status

class AdminFilter(BaseFilter):
    is_admin: bool = True
    config = get_config()

    async def __call__(self, obj: InlineQuery, config: Config = config) -> bool:
        return (obj.from_user.id in config.admin_ids) == self.is_admin
