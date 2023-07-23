from bardapi import Bard
from config import get_tokens
import hashlib
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, InlineQueryResultCachedAudio

config = get_tokens()
bard = Bard(token_from_browser=True)


logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=config.bot_token)
dp = Dispatcher(bot)


def tts(text: str) -> None:
    with open("bard_speech.ogg", "wb") as file:
        file.write(bytes(bard.speech(text)))


@dp.inline_handler()
async def inline(inline_query: InlineQuery):
    text = inline_query.query
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    tts(text)
    url = ""
    logging.info(url)
    item = InlineQueryResultCachedAudio(
        id=result_id,
        audio_file_id= url,
        caption=f'Speech Result of {text}'
    )
    
    await inline_query.answer(results=[item], cache_time=10)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)