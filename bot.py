import asyncio
import logging
import signal
import sys
from aiogram import Bot, Dispatcher
from hendlers import heandlers


# обработчик завершения скрипта
def signal_handler(sig, frame):
    print("Bot has stoped!")
    sys.exit(0)


# Запуск процесса поллинга новых апдейтов
async def main():
    # Включаем обработчик завершения и логгирование
    signal.signal(signal.SIGINT, signal_handler)
    logging.basicConfig(level=logging.INFO)

    # получаем токен и создаем объект бота
    with open("token.txt", "r") as token:
        api_token: str = token.read()
    bot = Bot(token=api_token)

    # Диспетчер
    dp = Dispatcher()
    dp.include_router(heandlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
