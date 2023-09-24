import asyncio
import logging
import betterlogging as bl
from uuid import uuid4
from tools import get_config, AdminFilter
from bardapi import BardAsync
from aiogram import Bot, Dispatcher
from aiogram.types import (
    InlineQuery,
    InlineQueryResultCachedVoice,
    FSInputFile,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

logger = logging.getLogger("Bard_Voice_Bot")
LOG_LEVEL = logging.INFO
bl.basic_colorized_config(level=LOG_LEVEL)
config = get_config()
bard = BardAsync(
    token="bQisFobFeHNP_eFK16vXGAdT2--B6_2pNJ0kLexePtUK-Ix14aLzHl7-FddB5hkRHWwE8w.."
)
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
)
bot = Bot(token=config.bot_token, parse_mode="HTML")
dp = Dispatcher()


async def tts(text: str) -> list:
    try:
        with open("bard_speech.ogg", "wb") as file:
            file.write(bytes(await bard.speech(text)))
        return [True]
    except Exception as e:
        logger.warning(e)
        return [e, False]


@dp.inline_query(AdminFilter())
async def inline(inline_query: InlineQuery) -> None:
    text = inline_query.query
    speech = await tts(text)
    if all(speech):
        send = await bot.send_voice(
            chat_id=config.channel_id, voice=FSInputFile("bard_speech.ogg")
        )
        with_text = InlineQueryResultCachedVoice(
            id=str(uuid4()),
            title="Speech + Text",
            voice_file_id=send.voice.file_id,
            caption=f"<code>{text}</code>",
        )
        without_text = InlineQueryResultCachedVoice(
            id=str(uuid4()), title="Speech", voice_file_id=send.voice.file_id
        )
        await inline_query.answer(results=[without_text, with_text], cache_time=10)
    else:
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title="Error",
                    input_message_content=InputTextMessageContent(
                        message_text=f"{speech[0]}"
                    ),
                )
            ],
            cache_time=10,
        )


async def start(bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start(bot))
