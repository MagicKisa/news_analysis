from aiogram import F, Router, types

router = Router()


@router.callback_query(F.data == "Классифицировать новость")
async def callback_check(callback: types.CallbackQuery):
    await callback.message.answer(
        text="Пришлите текст новости:)"
    )

@router.callback_query(F.data == "Классифицировать новость")
async def callback_check(callback: types.CallbackQuery):
    await callback.message.answer(
        text="Пришлите текст новости:)"
    )