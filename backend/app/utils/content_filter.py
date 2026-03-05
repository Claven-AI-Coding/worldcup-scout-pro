"""内容过滤工具 — 违禁词检测与替换"""

import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.banned_word import BannedWord

# 内存缓存，启动后加载一次
_banned_words_cache: dict[str, list[str]] | None = None


async def load_banned_words(db: AsyncSession) -> dict[str, list[str]]:
    """从数据库加载违禁词到内存缓存"""
    global _banned_words_cache
    if _banned_words_cache is not None:
        return _banned_words_cache

    result = await db.execute(select(BannedWord))
    words = result.scalars().all()

    cache: dict[str, list[str]] = {}
    for w in words:
        cat = w.category or "other"
        if cat not in cache:
            cache[cat] = []
        cache[cat].append(w.word)

    _banned_words_cache = cache
    return cache


def reset_cache() -> None:
    """重置缓存（违禁词库更新后调用）"""
    global _banned_words_cache
    _banned_words_cache = None


async def check_content(text: str, db: AsyncSession) -> dict:
    """检查文本是否包含违禁词

    Returns:
        {
            "is_clean": bool,
            "matched_words": list[str],
            "categories": list[str],
        }
    """
    banned = await load_banned_words(db)
    matched_words: list[str] = []
    categories: set[str] = set()

    # 预处理：去除空格和特殊字符干扰
    clean_text = re.sub(r"[\s\u200b\u200c\u200d\ufeff]", "", text.lower())

    for category, words in banned.items():
        for word in words:
            clean_word = word.lower()
            if clean_word in clean_text:
                matched_words.append(word)
                categories.add(category)

    return {
        "is_clean": len(matched_words) == 0,
        "matched_words": matched_words,
        "categories": list(categories),
    }


async def filter_content(text: str, db: AsyncSession, replacement: str = "**") -> str:
    """过滤文本中的违禁词，替换为 ** """
    banned = await load_banned_words(db)
    filtered = text

    for _category, words in banned.items():
        for word in words:
            # 大小写不敏感替换
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            filtered = pattern.sub(replacement, filtered)

    return filtered
