"""Seed banned words for content filtering.

Usage:
    python scripts/seed_banned_words.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.database import Base, async_session, engine  # noqa: E402
from app.models import BannedWord  # noqa: E402

# 违禁词库（分类）
BANNED_WORDS = {
    "profanity": [
        "操你", "他妈的", "傻逼", "草泥马", "妈的", "卧槽",
        "去死", "白痴", "垃圾", "废物", "滚蛋", "混蛋",
        "脑残", "贱人", "狗屎", "你妈",
    ],
    "gambling": [
        "赌博", "赌球", "下注", "庄家", "赔率", "盘口",
        "外围", "买球", "投注站", "菠菜", "博彩", "私彩",
        "地下盘", "让球", "黑庄", "杀猪盘",
    ],
    "political": [
        "颠覆", "分裂", "暴动", "政变",
    ],
    "spam": [
        "加微信", "加QQ", "免费领", "扫码领取", "点击链接",
        "日赚", "月入", "兼职", "代理", "刷单",
        "V信", "薇信", "➕V",
    ],
}


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        count = 0
        for category, words in BANNED_WORDS.items():
            for word in words:
                bw = BannedWord(word=word, category=category)
                db.add(bw)
                count += 1
            print(f"  Added {len(words)} words in category: {category}")

        await db.commit()
        print(f"\nBanned words seeded: {count} total")


if __name__ == "__main__":
    print("Seeding banned words...")
    asyncio.run(seed())
