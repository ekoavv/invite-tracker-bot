import aiosqlite

DB_NAME = "invites.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS invites (
                adder_id INTEGER,
                added_id INTEGER,
                added_username TEXT,
                added_phone TEXT,
                added_date TEXT
            )
        """)
        await db.commit()

async def save_invite(adder_id, added_id, added_username=None, added_phone=None, added_date=None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO invites (adder_id, added_id, added_username, added_phone, added_date)
            VALUES (?, ?, ?, ?, ?)
        """, (adder_id, added_id, added_username, added_phone, added_date))
        await db.commit()

async def get_user_added_count_by(query):
    async with aiosqlite.connect(DB_NAME) as db:
        for col in ['added_id', 'added_username', 'added_phone']:
            async with db.execute(f"""
                SELECT adder_id, COUNT(*) FROM invites WHERE {col} = ? GROUP BY adder_id
            """, (query,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return row
    return None

async def get_all_stats(limit=10):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT adder_id, COUNT(*) as cnt
            FROM invites
            GROUP BY adder_id
            ORDER BY cnt DESC
            LIMIT ?
        """, (limit,)) as cursor:
            return await cursor.fetchall()
