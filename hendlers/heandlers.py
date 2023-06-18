from aiogram import Router, F, types
from aiogram.types import Message, FSInputFile
from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
import sys

from hendlers.answers import answers

sys.path.append("./DB")

import database

router = Router()


# создаем свой callback для выбора билета
class MyCallback_bilet(CallbackData, prefix="bilet"):
    num_bilet: Optional[str]


# создаем свой callback для вывода ответа
class MyCallback_answer(CallbackData, prefix="answer"):
    num_question: Optional[str]


# Хэндлер на /start
@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f"Привет, *{message.from_user.first_name}*\!", parse_mode="MarkdownV2"
    )
    database.register_user(message.from_user.id)
    kb = [
        [types.KeyboardButton(text="Посмотреть ответ")],
        [types.KeyboardButton(text="Сменить билет")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        text="Это телеграмм бот для просмотра ответов по инглишу", reply_markup=keyboard
    )


# Хендлер для смены билета
@router.message(Text("Сменить билет"))
async def with_puree(message: types.Message):
    await change_bilet(message)


# Хендлер для просмотра ответа
@router.message(Text("Посмотреть ответ"))
async def with_puree(message: types.Message):
    if database.get_bilet(message.from_user.id) == "None":
        await message.answer("Сначала выбери билет!")
    else:
        await choose_answer(message)


# колбек для вывода ответа
@router.callback_query(MyCallback_bilet.filter())
async def my_callback_output(query, callback_data: MyCallback_bilet):
    database.update_user_data(query.from_user.id, callback_data.num_bilet)
    await query.message.delete()
    await query.message.answer("Билет выбран, смотри ответы")
    await query.answer(cache_time=10)


# колбек для вывода ответа
@router.callback_query(MyCallback_answer.filter())
async def my_callback_group(query, callback_data: MyCallback_answer):
    await query.message.delete()
    if database.get_bilet(query.from_user.id) == "None":
        await query.message.answer("Ты еще не выбрал билет!")
    elif callback_data.num_question == "all":
        x = range(1, 21)
        await query.message.answer(
            f"для билета {database.get_bilet(query.from_user.id)}"
        )
        for i in x:
            await query.message.answer(
                f"вопрос {i}, ответ {get_answer(database.get_bilet(query.from_user.id),str(i))}"
            )
    else:
        await query.message.answer(
            f"в билете {database.get_bilet(query.from_user.id)}, в вопросе {callback_data.num_question}, ответ {get_answer(database.get_bilet(query.from_user.id),callback_data.num_question)}"
        )


# выбор билета
async def change_bilet(message):
    builder = InlineKeyboardBuilder()
    all_bilet = range(15)
    for bilet in all_bilet:
        builder.add(
            types.InlineKeyboardButton(
                text=str(bilet + 1),
                callback_data=MyCallback_bilet(num_bilet=str(bilet + 1)).pack(),
            )
        )
    builder.adjust(5)
    await message.answer("Выберите билеты:", reply_markup=builder.as_markup())


# вывод ответа
async def choose_answer(message):
    builder = InlineKeyboardBuilder()
    all_question = range(20)
    for question in all_question:
        builder.add(
            types.InlineKeyboardButton(
                text=str(question + 1),
                callback_data=MyCallback_answer(num_question=str(question + 1)).pack(),
            )
        )
    builder.add(
        types.InlineKeyboardButton(
            text="все ответы",
            callback_data=MyCallback_answer(num_question="all").pack(),
        )
    )
    builder.adjust(5)
    await message.answer("Выберите номер вопроса:", reply_markup=builder.as_markup())


def get_answer(num_bilet: str, num_question: str) -> str:
    bilet = answers.get(num_bilet)
    if bilet == None:
        return "None"
    answer = bilet.get(num_question)
    if answer == None:
        return "None"
    return answer
