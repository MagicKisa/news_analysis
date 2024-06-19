from aiogram import Router, F
from aiogram import types

from keyboards.simple_row import make_row_keyboard, make_inline_keyboard
router = Router()

@router.callback_query(F.data == "Рассказать о моей работе")
async def callback_check(callback: types.CallbackQuery):
    await callback.message.answer(
        text=(
            "Бот разработан в рамках проектной деятельности на программе \"Искусственный интеллект\" НИУ ВШЭ\n\n"
            "Решается задача классификации текста с использованием модели RoBERTa на новостных данных. "
            "Произвольному новостному тексту сопоставляется одна из 7 категорий: "
            "'Культура', 'Россия', 'Мир', 'Наука и технологии', 'Спорт', 'Экономика', 'Путешествия'."
        )
    )
