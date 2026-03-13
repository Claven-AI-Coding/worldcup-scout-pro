"""初始违禁词库种子数据"""

# 分类违禁词库
BANNED_WORDS = {
    "profanity": [  # 脏话粗口
        "傻逼",
        "操你妈",
        "草泥马",
        "fuck",
        "shit",
        "damn",
    ],
    "gambling": [  # 赌博相关
        "赌球",
        "下注",
        "开盘",
        "赔率",
        "庄家",
        "博彩",
    ],
    "political": [  # 政治敏感
        # 根据实际需求添加
    ],
    "spam": [  # 垃圾广告
        "加微信",
        "扫码",
        "免费领取",
        "点击链接",
        "优惠券",
    ],
    "illegal": [  # 违法内容
        "假球",
        "黑哨",
        "操纵比赛",
    ],
}


def get_all_banned_words() -> list[tuple[str, str]]:
    """获取所有违禁词（word, category）"""
    result = []
    for category, words in BANNED_WORDS.items():
        for word in words:
            result.append((word, category))
    return result
