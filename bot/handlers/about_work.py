from aiogram import Router, F
from aiogram import types

from keyboards.simple_row import make_row_keyboard, make_inline_keyboard
router = Router()


@router.callback_query(F.data == "Рассказать о моей работе")
async def callback_check(callback: types.CallbackQuery):
    await callback.message.answer(
        text="Я в отпуске хахах:)"
    )




