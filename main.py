import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from VK_API import get_post_info
import requests
import os
from config import TG_TOKEN
date_post = None
answer = None
save_path = "photo.jpeg"

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


def cut_link(link) -> str:
    post_id = link.split('wall')[-1]
    return post_id

def download_photo_from_url(photo_url, save_path) -> None:
    response = requests.get(photo_url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

def remove_photo(save_path):
    os.remove(save_path)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> str:
    await message.answer("Отправь ссылку на пост в ВКонтакте!")

@dp.message()
async def link_answer(message: Message)-> str:
    if "https://vk.com/" in str(message.text):
        global answer, date_post
        link = str(message.text)
        post_id = cut_link(link)
        ANSWER = []
        ANSWER = get_post_info(post_id)
        await message.answer(f"Текст: {ANSWER[0]}\nДата: {ANSWER[1]}")     
        i = 0
        while i != len(ANSWER[2]):
            download_photo_from_url(ANSWER[2][i], save_path)
            await message.answer_document(document=FSInputFile(save_path))
            remove_photo(save_path)
            del ANSWER[2][i]
    else:
        await message.answer("Не валидная ссылка")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())