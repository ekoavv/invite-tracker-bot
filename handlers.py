from aiogram import Router, types, F
from config import ADMIN_ID
from db import save_invite, get_user_added_count_by, get_all_stats
from datetime import datetime

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Salom! Bu bot guruhga kim nechta odam qo‘shganini hisoblaydi.\n"
        "🔎 ID, @username yoki telefon raqam yuboring."
    )

@router.message(F.text == "/admin")
async def admin_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Siz admin emassiz.")
    
    text = "🔐 Admin panel:\n"            "/top – Eng ko‘p odam qo‘shganlar\n"            "/stats – Umumiy yozuvlar soni\n"            "/find @username yoki ID yoki raqam"
    await message.answer(text)

@router.message(F.text == "/top")
async def top_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    rows = await get_all_stats()
    if not rows:
        return await message.answer("❌ Hech qanday yozuv yo‘q.")
    text = "🏆 Eng ko‘p odam qo‘shganlar:\n\n"
    for i, (adder_id, count) in enumerate(rows, start=1):
        text += f"{i}. 👤 ID: {adder_id} – {count} ta odam\n"
    await message.answer(text)

@router.message(F.text == "/stats")
async def stats_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    import aiosqlite
    async with aiosqlite.connect("invites.db") as db:
        async with db.execute("SELECT COUNT(*) FROM invites") as cursor:
            total = (await cursor.fetchone())[0]
    await message.answer(f"📊 Umumiy yozuvlar: {total} ta")

@router.message(F.text.startswith("/find "))
async def find_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    query = message.text[6:].strip()
    result = await get_user_added_count_by(query)
    if result:
        adder_id, count = result
        await message.answer(f"👤 ID: {adder_id} – {count} ta odam qo‘shgan.")
    else:
        await message.answer("❌ Ma’lumot topilmadi.")

@router.message(F.text)
async def search_handler(message: types.Message):
    query = message.text.strip()
    result = await get_user_added_count_by(query)
    if result:
        adder_id, count = result
        await message.answer(f"👤 Bu foydalanuvchi {count} ta odamni guruhga qo‘shgan.")
    else:
        await message.answer("❌ Ma’lumot topilmadi.")

@router.chat_member()
async def track_invites(event: types.ChatMemberUpdated):
    if event.old_chat_member.status == "left" and event.new_chat_member.status == "member":
        adder = event.from_user
        added = event.new_chat_member.user

        await save_invite(
            adder_id=adder.id,
            added_id=added.id,
            added_username=added.username,
            added_phone=None,
            added_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
