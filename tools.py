from environs import Env
from dataclasses import dataclass
from aiogram.filters import BaseFilter
from aiogram.types import InlineQuery


@dataclass
class Config:
    bot_token: str
    channel_id: str
    admin_ids: list[int]


def get_config():
    env = Env()
    env.read_env(".env")
    return Config(
        bot_token=env.str("BOT_TOKEN"),
        channel_id=env.str("CHANNEL_ID"),
        admin_ids=[int(i) for i in env.list("ADMIN_IDS")],
    )


class AdminFilter(BaseFilter):
    is_admin: bool = True
    config = get_config()

    async def __call__(self, obj: InlineQuery, config: Config = config) -> bool:
        return (obj.from_user.id in config.admin_ids) == self.is_admin