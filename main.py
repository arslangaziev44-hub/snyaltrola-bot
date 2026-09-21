import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8881067785:AAF8W-ilVLxa9l1ec4skRd_2mGIOx…"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

chat_counters = {}

def get_random_target():
    return random.randint(15, 25)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для группы. Каждые 15–25 сообщений я буду автоматически "
        "радовать вас случайным подарком!"
    )

@dp.message()
async def count_messages(message: types.Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    chat_id = message.chat.id

    if chat_id not in chat_counters:
        chat_counters[chat_id] = {
            "count": 0,
            "target": get_random_target()
        }

    data = chat_counters[chat_id]
    data["count"] += 1

    if data["count"] >= data["target"]:
        gifts = [
            "🎁 Поздравляю! Вы выиграли эксклюзивный виртуальный стикер!",
            "🎉 Ура! Держите редкий цифровой подарок!",
            "🏆 Случайная награда нашла своего героя! Ловите бонус!",
            "⭐ Внезапный подарок! Вы получаете +100 к карме в этом чате!"
        ]
        winning_gift = random.choice(gifts)

        if message.from_user:
            user_mention = message.from_user.mention_html()
            text = f"Подарок за активность!\n{user_mention}, {winning_gift}"
        else:
            text = f"Подарок за активность!\n{winning_gift}"

        await message.answer(text, parse_mode="HTML")

        data["count"] = 0
        data["target"] = get_random_target()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
