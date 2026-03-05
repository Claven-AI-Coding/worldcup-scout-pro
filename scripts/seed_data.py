"""Seed data script for World Cup 2026 (48 teams / 12 groups / 104 matches).

Usage:
    python scripts/seed_data.py

Populates the database with:
- 48 teams (12 groups, A-L)
- 240+ players (5 per team)
- 104 matches (72 group + 32 knockout)
"""

import asyncio
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 项目根路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.config import settings  # noqa: E402
from app.database import Base, async_session, engine  # noqa: E402
from app.models import Match, Player, Team  # noqa: E402

# ============================================================
# FIFA World Cup 2026 — 48 支参赛球队（12 组，A-L）
# ============================================================
TEAMS = [
    # Group A — 东道主美国所在组
    {"name": "美国", "name_en": "USA", "code": "USA", "group_name": "A", "coach": "波切蒂诺",
     "stats": {"fifa_ranking": 11, "confederation": "CONCACAF", "appearances": 11, "best_result": "四分之一决赛"}},
    {"name": "墨西哥", "name_en": "Mexico", "code": "MEX", "group_name": "A", "coach": "阿吉雷",
     "stats": {"fifa_ranking": 15, "confederation": "CONCACAF", "appearances": 17, "best_result": "四分之一决赛"}},
    {"name": "加拿大", "name_en": "Canada", "code": "CAN", "group_name": "A", "coach": "马尔施",
     "stats": {"fifa_ranking": 41, "confederation": "CONCACAF", "appearances": 3, "best_result": "小组赛"}},
    {"name": "塞内加尔", "name_en": "Senegal", "code": "SEN", "group_name": "A", "coach": "西塞",
     "stats": {"fifa_ranking": 17, "confederation": "CAF", "appearances": 4, "best_result": "四分之一决赛"}},
    # Group B
    {"name": "阿根廷", "name_en": "Argentina", "code": "ARG", "group_name": "B", "coach": "斯卡洛尼",
     "stats": {"fifa_ranking": 1, "confederation": "CONMEBOL", "appearances": 18, "best_result": "冠军"}},
    {"name": "澳大利亚", "name_en": "Australia", "code": "AUS", "group_name": "B", "coach": "波波维奇",
     "stats": {"fifa_ranking": 24, "confederation": "AFC", "appearances": 6, "best_result": "十六强"}},
    {"name": "尼日利亚", "name_en": "Nigeria", "code": "NGA", "group_name": "B", "coach": "佩塞罗",
     "stats": {"fifa_ranking": 28, "confederation": "CAF", "appearances": 7, "best_result": "十六强"}},
    {"name": "秘鲁", "name_en": "Peru", "code": "PER", "group_name": "B", "coach": "弗萨蒂",
     "stats": {"fifa_ranking": 32, "confederation": "CONMEBOL", "appearances": 6, "best_result": "四分之一决赛"}},
    # Group C
    {"name": "法国", "name_en": "France", "code": "FRA", "group_name": "C", "coach": "德尚",
     "stats": {"fifa_ranking": 2, "confederation": "UEFA", "appearances": 16, "best_result": "冠军"}},
    {"name": "丹麦", "name_en": "Denmark", "code": "DEN", "group_name": "C", "coach": "胡尔曼德",
     "stats": {"fifa_ranking": 21, "confederation": "UEFA", "appearances": 6, "best_result": "四分之一决赛"}},
    {"name": "沙特阿拉伯", "name_en": "Saudi Arabia", "code": "KSA", "group_name": "C", "coach": "曼奇尼",
     "stats": {"fifa_ranking": 56, "confederation": "AFC", "appearances": 7, "best_result": "十六强"}},
    {"name": "厄瓜多尔", "name_en": "Ecuador", "code": "ECU", "group_name": "C", "coach": "贝塞拉",
     "stats": {"fifa_ranking": 33, "confederation": "CONMEBOL", "appearances": 4, "best_result": "十六强"}},
    # Group D
    {"name": "巴西", "name_en": "Brazil", "code": "BRA", "group_name": "D", "coach": "多里瓦尔",
     "stats": {"fifa_ranking": 3, "confederation": "CONMEBOL", "appearances": 22, "best_result": "冠军"}},
    {"name": "日本", "name_en": "Japan", "code": "JPN", "group_name": "D", "coach": "森保一",
     "stats": {"fifa_ranking": 18, "confederation": "AFC", "appearances": 7, "best_result": "十六强"}},
    {"name": "塞尔维亚", "name_en": "Serbia", "code": "SRB", "group_name": "D", "coach": "皮克西",
     "stats": {"fifa_ranking": 26, "confederation": "UEFA", "appearances": 13, "best_result": "第四名"}},
    {"name": "喀麦隆", "name_en": "Cameroon", "code": "CMR", "group_name": "D", "coach": "松",
     "stats": {"fifa_ranking": 43, "confederation": "CAF", "appearances": 8, "best_result": "四分之一决赛"}},
    # Group E
    {"name": "英格兰", "name_en": "England", "code": "ENG", "group_name": "E", "coach": "图赫尔",
     "stats": {"fifa_ranking": 4, "confederation": "UEFA", "appearances": 16, "best_result": "冠军"}},
    {"name": "荷兰", "name_en": "Netherlands", "code": "NED", "group_name": "E", "coach": "科曼",
     "stats": {"fifa_ranking": 7, "confederation": "UEFA", "appearances": 11, "best_result": "亚军"}},
    {"name": "韩国", "name_en": "South Korea", "code": "KOR", "group_name": "E", "coach": "洪明甫",
     "stats": {"fifa_ranking": 23, "confederation": "AFC", "appearances": 11, "best_result": "第四名"}},
    {"name": "乌拉圭", "name_en": "Uruguay", "code": "URU", "group_name": "E", "coach": "比尔萨",
     "stats": {"fifa_ranking": 14, "confederation": "CONMEBOL", "appearances": 14, "best_result": "冠军"}},
    # Group F
    {"name": "西班牙", "name_en": "Spain", "code": "ESP", "group_name": "F", "coach": "德拉富恩特",
     "stats": {"fifa_ranking": 5, "confederation": "UEFA", "appearances": 16, "best_result": "冠军"}},
    {"name": "德国", "name_en": "Germany", "code": "GER", "group_name": "F", "coach": "纳格尔斯曼",
     "stats": {"fifa_ranking": 8, "confederation": "UEFA", "appearances": 20, "best_result": "冠军"}},
    {"name": "哥伦比亚", "name_en": "Colombia", "code": "COL", "group_name": "F", "coach": "洛伦索",
     "stats": {"fifa_ranking": 12, "confederation": "CONMEBOL", "appearances": 7, "best_result": "四分之一决赛"}},
    {"name": "摩洛哥", "name_en": "Morocco", "code": "MAR", "group_name": "F", "coach": "雷格拉吉",
     "stats": {"fifa_ranking": 13, "confederation": "CAF", "appearances": 7, "best_result": "第四名"}},
    # Group G
    {"name": "葡萄牙", "name_en": "Portugal", "code": "POR", "group_name": "G", "coach": "马丁内斯",
     "stats": {"fifa_ranking": 6, "confederation": "UEFA", "appearances": 8, "best_result": "第三名"}},
    {"name": "瑞士", "name_en": "Switzerland", "code": "SUI", "group_name": "G", "coach": "亚金",
     "stats": {"fifa_ranking": 19, "confederation": "UEFA", "appearances": 12, "best_result": "四分之一决赛"}},
    {"name": "加纳", "name_en": "Ghana", "code": "GHA", "group_name": "G", "coach": "阿杜",
     "stats": {"fifa_ranking": 44, "confederation": "CAF", "appearances": 4, "best_result": "四分之一决赛"}},
    {"name": "伊朗", "name_en": "Iran", "code": "IRN", "group_name": "G", "coach": "盖拉尼",
     "stats": {"fifa_ranking": 22, "confederation": "AFC", "appearances": 6, "best_result": "小组赛"}},
    # Group H
    {"name": "意大利", "name_en": "Italy", "code": "ITA", "group_name": "H", "coach": "斯帕莱蒂",
     "stats": {"fifa_ranking": 9, "confederation": "UEFA", "appearances": 18, "best_result": "冠军"}},
    {"name": "克罗地亚", "name_en": "Croatia", "code": "CRO", "group_name": "H", "coach": "达利奇",
     "stats": {"fifa_ranking": 10, "confederation": "UEFA", "appearances": 6, "best_result": "亚军"}},
    {"name": "智利", "name_en": "Chile", "code": "CHI", "group_name": "H", "coach": "加雷卡",
     "stats": {"fifa_ranking": 36, "confederation": "CONMEBOL", "appearances": 10, "best_result": "第三名"}},
    {"name": "波兰", "name_en": "Poland", "code": "POL", "group_name": "H", "coach": "普罗比茨",
     "stats": {"fifa_ranking": 25, "confederation": "UEFA", "appearances": 9, "best_result": "第三名"}},
    # Group I — 新增
    {"name": "比利时", "name_en": "Belgium", "code": "BEL", "group_name": "I", "coach": "特代斯科",
     "stats": {"fifa_ranking": 16, "confederation": "UEFA", "appearances": 14, "best_result": "第三名"}},
    {"name": "奥地利", "name_en": "Austria", "code": "AUT", "group_name": "I", "coach": "朗尼克",
     "stats": {"fifa_ranking": 20, "confederation": "UEFA", "appearances": 8, "best_result": "第三名"}},
    {"name": "巴拉圭", "name_en": "Paraguay", "code": "PAR", "group_name": "I", "coach": "阿尔法罗",
     "stats": {"fifa_ranking": 47, "confederation": "CONMEBOL", "appearances": 9, "best_result": "四分之一决赛"}},
    {"name": "中国", "name_en": "China PR", "code": "CHN", "group_name": "I", "coach": "伊万科维奇",
     "stats": {"fifa_ranking": 70, "confederation": "AFC", "appearances": 2, "best_result": "小组赛"}},
    # Group J — 新增
    {"name": "土耳其", "name_en": "Turkey", "code": "TUR", "group_name": "J", "coach": "蒙特拉",
     "stats": {"fifa_ranking": 27, "confederation": "UEFA", "appearances": 3, "best_result": "第三名"}},
    {"name": "威尔士", "name_en": "Wales", "code": "WAL", "group_name": "J", "coach": "佩奇",
     "stats": {"fifa_ranking": 29, "confederation": "UEFA", "appearances": 2, "best_result": "四分之一决赛"}},
    {"name": "突尼斯", "name_en": "Tunisia", "code": "TUN", "group_name": "J", "coach": "卡德里",
     "stats": {"fifa_ranking": 37, "confederation": "CAF", "appearances": 6, "best_result": "小组赛"}},
    {"name": "牙买加", "name_en": "Jamaica", "code": "JAM", "group_name": "J", "coach": "哈勒格里姆松",
     "stats": {"fifa_ranking": 52, "confederation": "CONCACAF", "appearances": 2, "best_result": "小组赛"}},
    # Group K — 新增
    {"name": "乌克兰", "name_en": "Ukraine", "code": "UKR", "group_name": "K", "coach": "雷布罗夫",
     "stats": {"fifa_ranking": 30, "confederation": "UEFA", "appearances": 2, "best_result": "四分之一决赛"}},
    {"name": "苏格兰", "name_en": "Scotland", "code": "SCO", "group_name": "K", "coach": "克拉克",
     "stats": {"fifa_ranking": 39, "confederation": "UEFA", "appearances": 9, "best_result": "小组赛"}},
    {"name": "阿尔及利亚", "name_en": "Algeria", "code": "ALG", "group_name": "K", "coach": "佩特科维奇",
     "stats": {"fifa_ranking": 42, "confederation": "CAF", "appearances": 5, "best_result": "十六强"}},
    {"name": "洪都拉斯", "name_en": "Honduras", "code": "HON", "group_name": "K", "coach": "鲁埃达",
     "stats": {"fifa_ranking": 73, "confederation": "CONCACAF", "appearances": 4, "best_result": "小组赛"}},
    # Group L — 新增
    {"name": "捷克", "name_en": "Czech Republic", "code": "CZE", "group_name": "L", "coach": "哈塞克",
     "stats": {"fifa_ranking": 31, "confederation": "UEFA", "appearances": 10, "best_result": "亚军"}},
    {"name": "挪威", "name_en": "Norway", "code": "NOR", "group_name": "L", "coach": "索尔巴肯",
     "stats": {"fifa_ranking": 35, "confederation": "UEFA", "appearances": 3, "best_result": "小组赛"}},
    {"name": "科特迪瓦", "name_en": "Ivory Coast", "code": "CIV", "group_name": "L", "coach": "法耶",
     "stats": {"fifa_ranking": 38, "confederation": "CAF", "appearances": 4, "best_result": "小组赛"}},
    {"name": "新西兰", "name_en": "New Zealand", "code": "NZL", "group_name": "L", "coach": "海",
     "stats": {"fifa_ranking": 93, "confederation": "OFC", "appearances": 3, "best_result": "小组赛"}},
]

# ============================================================
# 球员数据 — 每队 5 名核心球员，共 240 名
# ============================================================
PLAYERS = {
    # Group A
    "USA": [
        {"name": "普利西奇", "name_en": "Christian Pulisic", "number": 10, "position": "FW", "age": 27, "club": "AC米兰"},
        {"name": "麦肯尼", "name_en": "Weston McKennie", "number": 8, "position": "MF", "age": 27, "club": "尤文图斯"},
        {"name": "亚当斯", "name_en": "Tyler Adams", "number": 4, "position": "MF", "age": 27, "club": "伯恩茅斯"},
        {"name": "韦阿", "name_en": "Timothy Weah", "number": 11, "position": "FW", "age": 26, "club": "尤文图斯"},
        {"name": "特纳", "name_en": "Matt Turner", "number": 1, "position": "GK", "age": 32, "club": "诺丁汉森林"},
    ],
    "MEX": [
        {"name": "洛萨诺", "name_en": "Hirving Lozano", "number": 22, "position": "FW", "age": 30, "club": "PSV"},
        {"name": "阿尔瓦雷斯", "name_en": "Edson Alvarez", "number": 4, "position": "MF", "age": 28, "club": "西汉姆"},
        {"name": "希门尼斯", "name_en": "Raul Jimenez", "number": 9, "position": "FW", "age": 35, "club": "富勒姆"},
        {"name": "奥乔亚", "name_en": "Guillermo Ochoa", "number": 13, "position": "GK", "age": 41, "club": "萨莱尼塔纳"},
        {"name": "罗莫", "name_en": "Luis Romo", "number": 7, "position": "MF", "age": 29, "club": "蒙特雷"},
    ],
    "CAN": [
        {"name": "戴维斯", "name_en": "Alphonso Davies", "number": 19, "position": "DF", "age": 25, "club": "拜仁慕尼黑"},
        {"name": "大卫", "name_en": "Jonathan David", "number": 20, "position": "FW", "age": 26, "club": "里尔"},
        {"name": "布坎南", "name_en": "Tajon Buchanan", "number": 11, "position": "FW", "age": 27, "club": "国际米兰"},
        {"name": "尤斯塔基奥", "name_en": "Stephen Eustaquio", "number": 7, "position": "MF", "age": 28, "club": "波尔图"},
        {"name": "博尔扬", "name_en": "Milan Borjan", "number": 18, "position": "GK", "age": 38, "club": "贝尔格莱德红星"},
    ],
    "SEN": [
        {"name": "马内", "name_en": "Sadio Mane", "number": 10, "position": "FW", "age": 34, "club": "利雅得新月"},
        {"name": "库利巴利", "name_en": "Kalidou Koulibaly", "number": 3, "position": "DF", "age": 35, "club": "利雅得青年"},
        {"name": "门迪", "name_en": "Edouard Mendy", "number": 16, "position": "GK", "age": 34, "club": "利雅得新月"},
        {"name": "萨尔", "name_en": "Ismaila Sarr", "number": 18, "position": "FW", "age": 28, "club": "马赛"},
        {"name": "格耶", "name_en": "Idrissa Gueye", "number": 5, "position": "MF", "age": 36, "club": "埃弗顿"},
    ],
    # Group B
    "ARG": [
        {"name": "梅西", "name_en": "Lionel Messi", "number": 10, "position": "FW", "age": 38, "club": "迈阿密国际"},
        {"name": "阿尔瓦雷斯", "name_en": "Julian Alvarez", "number": 9, "position": "FW", "age": 26, "club": "马德里竞技"},
        {"name": "德保罗", "name_en": "Rodrigo De Paul", "number": 7, "position": "MF", "age": 32, "club": "马德里竞技"},
        {"name": "麦卡利斯特", "name_en": "Alexis Mac Allister", "number": 20, "position": "MF", "age": 27, "club": "利物浦"},
        {"name": "马丁内斯", "name_en": "Emiliano Martinez", "number": 23, "position": "GK", "age": 33, "club": "阿斯顿维拉"},
    ],
    "AUS": [
        {"name": "赫鲁斯蒂奇", "name_en": "Ajdin Hrustic", "number": 10, "position": "MF", "age": 28, "club": "赫罗纳"},
        {"name": "库奥尔", "name_en": "Awer Mabil", "number": 11, "position": "FW", "age": 29, "club": "博洛尼亚"},
        {"name": "麦克拉伦", "name_en": "Jamie Maclaren", "number": 9, "position": "FW", "age": 33, "club": "墨尔本城"},
        {"name": "杰克逊·欧文", "name_en": "Jackson Irvine", "number": 22, "position": "MF", "age": 33, "club": "圣保利"},
        {"name": "瑞安", "name_en": "Mat Ryan", "number": 1, "position": "GK", "age": 34, "club": "罗马"},
    ],
    "NGA": [
        {"name": "奥西梅恩", "name_en": "Victor Osimhen", "number": 9, "position": "FW", "age": 27, "club": "那不勒斯"},
        {"name": "恩迪迪", "name_en": "Wilfred Ndidi", "number": 4, "position": "MF", "age": 29, "club": "莱斯特城"},
        {"name": "卢克曼", "name_en": "Ademola Lookman", "number": 18, "position": "FW", "age": 28, "club": "亚特兰大"},
        {"name": "伊海纳乔", "name_en": "Kelechi Iheanacho", "number": 14, "position": "FW", "age": 29, "club": "塞维利亚"},
        {"name": "恩瓦巴利", "name_en": "Francis Uzoho", "number": 23, "position": "GK", "age": 27, "club": "奥莫尼亚"},
    ],
    "PER": [
        {"name": "拉帕杜拉", "name_en": "Gianluca Lapadula", "number": 9, "position": "FW", "age": 36, "club": "卡利亚里"},
        {"name": "佩尼亚", "name_en": "Sergio Pena", "number": 8, "position": "MF", "age": 31, "club": "马尔默"},
        {"name": "弗洛雷斯", "name_en": "Edison Flores", "number": 20, "position": "MF", "age": 32, "club": "阿特拉斯"},
        {"name": "阿德文库拉", "name_en": "Luis Advincula", "number": 17, "position": "DF", "age": 34, "club": "博卡青年"},
        {"name": "加耶塞", "name_en": "Pedro Gallese", "number": 1, "position": "GK", "age": 36, "club": "奥兰多城"},
    ],
    # Group C
    "FRA": [
        {"name": "姆巴佩", "name_en": "Kylian Mbappe", "number": 10, "position": "FW", "age": 27, "club": "皇家马德里"},
        {"name": "格列兹曼", "name_en": "Antoine Griezmann", "number": 7, "position": "FW", "age": 35, "club": "马德里竞技"},
        {"name": "琼阿梅尼", "name_en": "Aurelien Tchouameni", "number": 8, "position": "MF", "age": 26, "club": "皇家马德里"},
        {"name": "坎特", "name_en": "N'Golo Kante", "number": 13, "position": "MF", "age": 35, "club": "伊蒂哈德"},
        {"name": "梅尼昂", "name_en": "Mike Maignan", "number": 16, "position": "GK", "age": 31, "club": "AC米兰"},
    ],
    "DEN": [
        {"name": "霍伊伦", "name_en": "Rasmus Hojlund", "number": 9, "position": "FW", "age": 23, "club": "曼联"},
        {"name": "埃里克森", "name_en": "Christian Eriksen", "number": 10, "position": "MF", "age": 34, "club": "曼联"},
        {"name": "霍伊别尔", "name_en": "Pierre-Emile Hojbjerg", "number": 23, "position": "MF", "age": 30, "club": "马赛"},
        {"name": "克里斯滕森", "name_en": "Andreas Christensen", "number": 6, "position": "DF", "age": 30, "club": "巴塞罗那"},
        {"name": "舒梅切尔", "name_en": "Kasper Schmeichel", "number": 1, "position": "GK", "age": 39, "club": "凯尔特人"},
    ],
    "KSA": [
        {"name": "阿尔道萨里", "name_en": "Salem Al-Dawsari", "number": 10, "position": "FW", "age": 33, "club": "利雅得新月"},
        {"name": "阿尔布雷坎", "name_en": "Firas Al-Buraikan", "number": 11, "position": "FW", "age": 26, "club": "利雅得新月"},
        {"name": "坎诺", "name_en": "Salman Al-Faraj", "number": 7, "position": "MF", "age": 35, "club": "利雅得新月"},
        {"name": "阿尔奥维斯", "name_en": "Mohammed Al-Owais", "number": 1, "position": "GK", "age": 34, "club": "利雅得新月"},
        {"name": "阿尔沙赫拉尼", "name_en": "Yasser Al-Shahrani", "number": 13, "position": "DF", "age": 34, "club": "利雅得新月"},
    ],
    "ECU": [
        {"name": "巴伦西亚", "name_en": "Enner Valencia", "number": 13, "position": "FW", "age": 36, "club": "国际队"},
        {"name": "卡塞雷斯", "name_en": "Moises Caicedo", "number": 23, "position": "MF", "age": 24, "club": "切尔西"},
        {"name": "埃斯图皮尼安", "name_en": "Pervis Estupinan", "number": 7, "position": "DF", "age": 28, "club": "布莱顿"},
        {"name": "普拉塔", "name_en": "Gonzalo Plata", "number": 19, "position": "FW", "age": 25, "club": "弗拉门戈"},
        {"name": "多明格斯", "name_en": "Alexander Dominguez", "number": 22, "position": "GK", "age": 39, "club": "基多体育"},
    ],
    # Group D
    "BRA": [
        {"name": "维尼修斯", "name_en": "Vinicius Jr", "number": 7, "position": "FW", "age": 25, "club": "皇家马德里"},
        {"name": "罗德里戈", "name_en": "Rodrygo", "number": 11, "position": "FW", "age": 25, "club": "皇家马德里"},
        {"name": "卡塞米罗", "name_en": "Casemiro", "number": 5, "position": "MF", "age": 34, "club": "曼联"},
        {"name": "帕奎塔", "name_en": "Lucas Paqueta", "number": 10, "position": "MF", "age": 28, "club": "西汉姆"},
        {"name": "阿利松", "name_en": "Alisson", "number": 1, "position": "GK", "age": 33, "club": "利物浦"},
    ],
    "JPN": [
        {"name": "久保建英", "name_en": "Takefusa Kubo", "number": 11, "position": "FW", "age": 25, "club": "皇家社会"},
        {"name": "三�的薰", "name_en": "Kaoru Mitoma", "number": 9, "position": "FW", "age": 29, "club": "布莱顿"},
        {"name": "远藤航", "name_en": "Wataru Endo", "number": 6, "position": "MF", "age": 33, "club": "利物浦"},
        {"name": "富安健洋", "name_en": "Takehiro Tomiyasu", "number": 2, "position": "DF", "age": 27, "club": "阿森纳"},
        {"name": "权田修一", "name_en": "Shuichi Gonda", "number": 12, "position": "GK", "age": 37, "club": "清水脉动"},
    ],
    "SRB": [
        {"name": "弗拉霍维奇", "name_en": "Dusan Vlahovic", "number": 9, "position": "FW", "age": 26, "club": "尤文图斯"},
        {"name": "米特罗维奇", "name_en": "Aleksandar Mitrovic", "number": 9, "position": "FW", "age": 31, "club": "利雅得胜利"},
        {"name": "塔迪奇", "name_en": "Dusan Tadic", "number": 10, "position": "MF", "age": 37, "club": "费内巴切"},
        {"name": "米林科维奇", "name_en": "Sergej Milinkovic-Savic", "number": 20, "position": "MF", "age": 31, "club": "利雅得新月"},
        {"name": "拉伊科维奇", "name_en": "Predrag Rajkovic", "number": 1, "position": "GK", "age": 31, "club": "马略卡"},
    ],
    "CMR": [
        {"name": "舒波-莫廷", "name_en": "Eric Maxim Choupo-Moting", "number": 13, "position": "FW", "age": 37, "club": "拜仁慕尼黑"},
        {"name": "恩库杜", "name_en": "Andre-Frank Zambo Anguissa", "number": 8, "position": "MF", "age": 30, "club": "那不勒斯"},
        {"name": "埃基蒂克", "name_en": "Carlos Baleba", "number": 22, "position": "MF", "age": 22, "club": "布莱顿"},
        {"name": "穆科迪", "name_en": "Christopher Wooh", "number": 4, "position": "DF", "age": 24, "club": "朗斯"},
        {"name": "奥纳纳", "name_en": "Andre Onana", "number": 16, "position": "GK", "age": 30, "club": "曼联"},
    ],
    # Group E
    "ENG": [
        {"name": "凯恩", "name_en": "Harry Kane", "number": 9, "position": "FW", "age": 32, "club": "拜仁慕尼黑"},
        {"name": "贝林厄姆", "name_en": "Jude Bellingham", "number": 10, "position": "MF", "age": 22, "club": "皇家马德里"},
        {"name": "萨卡", "name_en": "Bukayo Saka", "number": 7, "position": "FW", "age": 24, "club": "阿森纳"},
        {"name": "赖斯", "name_en": "Declan Rice", "number": 4, "position": "MF", "age": 27, "club": "阿森纳"},
        {"name": "皮克福德", "name_en": "Jordan Pickford", "number": 1, "position": "GK", "age": 32, "club": "埃弗顿"},
    ],
    "NED": [
        {"name": "加克波", "name_en": "Cody Gakpo", "number": 11, "position": "FW", "age": 26, "club": "利物浦"},
        {"name": "德容", "name_en": "Frenkie de Jong", "number": 21, "position": "MF", "age": 29, "club": "巴塞罗那"},
        {"name": "希克马", "name_en": "Virgil van Dijk", "number": 4, "position": "DF", "age": 34, "club": "利物浦"},
        {"name": "德佩", "name_en": "Memphis Depay", "number": 10, "position": "FW", "age": 32, "club": "科林蒂安"},
        {"name": "维尔布鲁根", "name_en": "Bart Verbruggen", "number": 1, "position": "GK", "age": 23, "club": "布莱顿"},
    ],
    "KOR": [
        {"name": "孙兴慜", "name_en": "Son Heung-min", "number": 7, "position": "FW", "age": 33, "club": "热刺"},
        {"name": "李在城", "name_en": "Lee Jae-sung", "number": 17, "position": "MF", "age": 34, "club": "美因茨"},
        {"name": "金玟哉", "name_en": "Kim Min-jae", "number": 3, "position": "DF", "age": 29, "club": "拜仁慕尼黑"},
        {"name": "黄喜灿", "name_en": "Hwang Hee-chan", "number": 11, "position": "FW", "age": 30, "club": "狼队"},
        {"name": "金承奎", "name_en": "Kim Seung-gyu", "number": 1, "position": "GK", "age": 36, "club": "利雅得青年"},
    ],
    "URU": [
        {"name": "努涅斯", "name_en": "Darwin Nunez", "number": 11, "position": "FW", "age": 27, "club": "利物浦"},
        {"name": "巴尔韦德", "name_en": "Federico Valverde", "number": 15, "position": "MF", "age": 27, "club": "皇家马德里"},
        {"name": "阿劳霍", "name_en": "Ronald Araujo", "number": 4, "position": "DF", "age": 27, "club": "巴塞罗那"},
        {"name": "苏亚雷斯", "name_en": "Luis Suarez", "number": 9, "position": "FW", "age": 39, "club": "迈阿密国际"},
        {"name": "罗切特", "name_en": "Sergio Rochet", "number": 1, "position": "GK", "age": 33, "club": "国际队"},
    ],
    # Group F
    "ESP": [
        {"name": "亚马尔", "name_en": "Lamine Yamal", "number": 19, "position": "FW", "age": 18, "club": "巴塞罗那"},
        {"name": "佩德里", "name_en": "Pedri", "number": 8, "position": "MF", "age": 23, "club": "巴塞罗那"},
        {"name": "莫拉塔", "name_en": "Alvaro Morata", "number": 7, "position": "FW", "age": 33, "club": "AC米兰"},
        {"name": "罗德里", "name_en": "Rodri", "number": 16, "position": "MF", "age": 29, "club": "曼城"},
        {"name": "西蒙", "name_en": "Unai Simon", "number": 23, "position": "GK", "age": 27, "club": "毕尔巴鄂"},
    ],
    "GER": [
        {"name": "穆西亚拉", "name_en": "Jamal Musiala", "number": 10, "position": "MF", "age": 23, "club": "拜仁慕尼黑"},
        {"name": "维尔茨", "name_en": "Florian Wirtz", "number": 17, "position": "MF", "age": 23, "club": "勒沃库森"},
        {"name": "哈弗茨", "name_en": "Kai Havertz", "number": 7, "position": "FW", "age": 27, "club": "阿森纳"},
        {"name": "京多安", "name_en": "Ilkay Gundogan", "number": 21, "position": "MF", "age": 35, "club": "巴塞罗那"},
        {"name": "诺伊尔", "name_en": "Manuel Neuer", "number": 1, "position": "GK", "age": 40, "club": "拜仁慕尼黑"},
    ],
    "COL": [
        {"name": "路易斯·迪亚斯", "name_en": "Luis Diaz", "number": 7, "position": "FW", "age": 29, "club": "利物浦"},
        {"name": "哈梅斯", "name_en": "James Rodriguez", "number": 10, "position": "MF", "age": 34, "club": "巴列卡诺"},
        {"name": "阿里亚斯", "name_en": "Santiago Arias", "number": 4, "position": "DF", "age": 34, "club": "巴列卡诺"},
        {"name": "穆里尔", "name_en": "Rafael Santos Borre", "number": 19, "position": "FW", "age": 30, "club": "国际米兰"},
        {"name": "奥斯皮纳", "name_en": "David Ospina", "number": 1, "position": "GK", "age": 37, "club": "利雅得新月"},
    ],
    "MAR": [
        {"name": "哈基米", "name_en": "Achraf Hakimi", "number": 2, "position": "DF", "age": 27, "club": "巴黎圣日耳曼"},
        {"name": "齐耶赫", "name_en": "Hakim Ziyech", "number": 7, "position": "FW", "age": 33, "club": "加拉塔萨雷"},
        {"name": "恩内斯里", "name_en": "Youssef En-Nesyri", "number": 19, "position": "FW", "age": 29, "club": "塞维利亚"},
        {"name": "阿姆拉巴特", "name_en": "Sofyan Amrabat", "number": 4, "position": "MF", "age": 29, "club": "费内巴切"},
        {"name": "布努", "name_en": "Yassine Bounou", "number": 1, "position": "GK", "age": 33, "club": "利雅得新月"},
    ],
    # Group G
    "POR": [
        {"name": "C罗", "name_en": "Cristiano Ronaldo", "number": 7, "position": "FW", "age": 41, "club": "利雅得胜利"},
        {"name": "B·费尔南德斯", "name_en": "Bruno Fernandes", "number": 8, "position": "MF", "age": 31, "club": "曼联"},
        {"name": "B·席尔瓦", "name_en": "Bernardo Silva", "number": 10, "position": "MF", "age": 31, "club": "曼城"},
        {"name": "迪亚斯", "name_en": "Ruben Dias", "number": 4, "position": "DF", "age": 29, "club": "曼城"},
        {"name": "迪奥戈·科斯塔", "name_en": "Diogo Costa", "number": 1, "position": "GK", "age": 26, "club": "波尔图"},
    ],
    "SUI": [
        {"name": "恩多耶", "name_en": "Dan Ndoye", "number": 17, "position": "FW", "age": 25, "club": "博洛尼亚"},
        {"name": "扎卡", "name_en": "Granit Xhaka", "number": 10, "position": "MF", "age": 33, "club": "勒沃库森"},
        {"name": "阿坎吉", "name_en": "Manuel Akanji", "number": 5, "position": "DF", "age": 30, "club": "曼城"},
        {"name": "恩博洛", "name_en": "Breel Embolo", "number": 7, "position": "FW", "age": 29, "club": "摩纳哥"},
        {"name": "佐默", "name_en": "Yann Sommer", "number": 1, "position": "GK", "age": 37, "club": "国际米兰"},
    ],
    "GHA": [
        {"name": "库杜斯", "name_en": "Mohammed Kudus", "number": 10, "position": "MF", "age": 25, "club": "西汉姆"},
        {"name": "因纳基·威廉姆斯", "name_en": "Inaki Williams", "number": 9, "position": "FW", "age": 32, "club": "毕尔巴鄂"},
        {"name": "帕尔蒂", "name_en": "Thomas Partey", "number": 5, "position": "MF", "age": 33, "club": "阿森纳"},
        {"name": "安德烈·阿尤", "name_en": "Andre Ayew", "number": 10, "position": "FW", "age": 36, "club": "勒阿弗尔"},
        {"name": "阿提苏", "name_en": "Lawrence Ati-Zigi", "number": 1, "position": "GK", "age": 28, "club": "圣加仑"},
    ],
    "IRN": [
        {"name": "阿兹蒙", "name_en": "Sardar Azmoun", "number": 20, "position": "FW", "age": 31, "club": "罗马"},
        {"name": "塔雷米", "name_en": "Mehdi Taremi", "number": 9, "position": "FW", "age": 33, "club": "国际米兰"},
        {"name": "贾汉巴赫什", "name_en": "Alireza Jahanbakhsh", "number": 18, "position": "FW", "age": 33, "club": "费耶诺德"},
        {"name": "普阿利甘吉", "name_en": "Saeid Ezatolahi", "number": 15, "position": "MF", "age": 30, "club": "韦斯特罗"},
        {"name": "贝兰万德", "name_en": "Alireza Beiranvand", "number": 1, "position": "GK", "age": 33, "club": "柏塞波利斯"},
    ],
    # Group H
    "ITA": [
        {"name": "巴雷拉", "name_en": "Nicolo Barella", "number": 18, "position": "MF", "age": 29, "club": "国际米兰"},
        {"name": "基耶萨", "name_en": "Federico Chiesa", "number": 14, "position": "FW", "age": 28, "club": "利物浦"},
        {"name": "斯卡马卡", "name_en": "Gianluca Scamacca", "number": 9, "position": "FW", "age": 27, "club": "亚特兰大"},
        {"name": "巴斯托尼", "name_en": "Alessandro Bastoni", "number": 6, "position": "DF", "age": 27, "club": "国际米兰"},
        {"name": "多纳鲁马", "name_en": "Gianluigi Donnarumma", "number": 21, "position": "GK", "age": 27, "club": "巴黎圣日耳曼"},
    ],
    "CRO": [
        {"name": "莫德里奇", "name_en": "Luka Modric", "number": 10, "position": "MF", "age": 40, "club": "皇家马德里"},
        {"name": "科瓦契奇", "name_en": "Mateo Kovacic", "number": 8, "position": "MF", "age": 32, "club": "曼城"},
        {"name": "格瓦迪奥尔", "name_en": "Josko Gvardiol", "number": 20, "position": "DF", "age": 24, "club": "曼城"},
        {"name": "克拉马里奇", "name_en": "Andrej Kramaric", "number": 9, "position": "FW", "age": 34, "club": "霍芬海姆"},
        {"name": "利瓦科维奇", "name_en": "Dominik Livakovic", "number": 1, "position": "GK", "age": 31, "club": "费内巴切"},
    ],
    "CHI": [
        {"name": "桑切斯", "name_en": "Alexis Sanchez", "number": 7, "position": "FW", "age": 37, "club": "马赛"},
        {"name": "比达尔", "name_en": "Arturo Vidal", "number": 23, "position": "MF", "age": 39, "club": "科洛科洛"},
        {"name": "巴尔加斯", "name_en": "Eduardo Vargas", "number": 11, "position": "FW", "age": 36, "club": "智利大学"},
        {"name": "梅德尔", "name_en": "Gary Medel", "number": 17, "position": "DF", "age": 38, "club": "博卡青年"},
        {"name": "布拉沃", "name_en": "Claudio Bravo", "number": 1, "position": "GK", "age": 43, "club": "皇家贝蒂斯"},
    ],
    "POL": [
        {"name": "莱万多夫斯基", "name_en": "Robert Lewandowski", "number": 9, "position": "FW", "age": 37, "club": "巴塞罗那"},
        {"name": "泽林斯基", "name_en": "Piotr Zielinski", "number": 20, "position": "MF", "age": 32, "club": "国际米兰"},
        {"name": "什琴斯尼", "name_en": "Wojciech Szczesny", "number": 1, "position": "GK", "age": 36, "club": "巴塞罗那"},
        {"name": "基维奥尔", "name_en": "Jakub Kiwior", "number": 14, "position": "DF", "age": 26, "club": "阿森纳"},
        {"name": "扎莱夫斯基", "name_en": "Nicola Zalewski", "number": 17, "position": "MF", "age": 24, "club": "罗马"},
    ],
    # Group I
    "BEL": [
        {"name": "德布劳内", "name_en": "Kevin De Bruyne", "number": 7, "position": "MF", "age": 35, "club": "曼城"},
        {"name": "卢卡库", "name_en": "Romelu Lukaku", "number": 9, "position": "FW", "age": 33, "club": "那不勒斯"},
        {"name": "多库", "name_en": "Jeremy Doku", "number": 11, "position": "FW", "age": 24, "club": "曼城"},
        {"name": "蒂勒曼斯", "name_en": "Youri Tielemans", "number": 8, "position": "MF", "age": 29, "club": "阿斯顿维拉"},
        {"name": "库尔图瓦", "name_en": "Thibaut Courtois", "number": 1, "position": "GK", "age": 34, "club": "皇家马德里"},
    ],
    "AUT": [
        {"name": "阿瑙托维奇", "name_en": "Marko Arnautovic", "number": 7, "position": "FW", "age": 37, "club": "国际米兰"},
        {"name": "萨比策尔", "name_en": "Marcel Sabitzer", "number": 9, "position": "MF", "age": 32, "club": "多特蒙德"},
        {"name": "绍布", "name_en": "Xaver Schlager", "number": 14, "position": "MF", "age": 29, "club": "莱比锡"},
        {"name": "阿拉巴", "name_en": "David Alaba", "number": 8, "position": "DF", "age": 33, "club": "皇家马德里"},
        {"name": "彭茨", "name_en": "Patrick Pentz", "number": 1, "position": "GK", "age": 29, "club": "布吕日"},
    ],
    "PAR": [
        {"name": "阿尔米隆", "name_en": "Miguel Almiron", "number": 10, "position": "MF", "age": 32, "club": "纽卡斯尔"},
        {"name": "桑切斯", "name_en": "Antonio Sanabria", "number": 9, "position": "FW", "age": 30, "club": "都灵"},
        {"name": "罗梅罗", "name_en": "Oscar Romero", "number": 11, "position": "FW", "age": 34, "club": "博卡青年"},
        {"name": "阿尔德雷特", "name_en": "Omar Alderete", "number": 4, "position": "DF", "age": 29, "club": "赫塔费"},
        {"name": "席尔瓦", "name_en": "Antony Silva", "number": 1, "position": "GK", "age": 43, "club": "自由队"},
    ],
    "CHN": [
        {"name": "武磊", "name_en": "Wu Lei", "number": 7, "position": "FW", "age": 34, "club": "上海海港"},
        {"name": "颜骏凌", "name_en": "Yan Junling", "number": 1, "position": "GK", "age": 35, "club": "上海海港"},
        {"name": "张玉宁", "name_en": "Zhang Yuning", "number": 9, "position": "FW", "age": 29, "club": "北京国安"},
        {"name": "蒋光太", "name_en": "Jiang Guangtai", "number": 5, "position": "DF", "age": 32, "club": "广州队"},
        {"name": "吴曦", "name_en": "Wu Xi", "number": 8, "position": "MF", "age": 37, "club": "上海申花"},
    ],
    # Group J
    "TUR": [
        {"name": "居勒尔", "name_en": "Arda Guler", "number": 8, "position": "MF", "age": 21, "club": "皇家马德里"},
        {"name": "恰尔汗奥卢", "name_en": "Hakan Calhanoglu", "number": 10, "position": "MF", "age": 32, "club": "国际米兰"},
        {"name": "于尔迪兹", "name_en": "Kenan Yildiz", "number": 18, "position": "FW", "age": 21, "club": "尤文图斯"},
        {"name": "德米拉尔", "name_en": "Merih Demiral", "number": 4, "position": "DF", "age": 28, "club": "利雅得青年"},
        {"name": "居纳什", "name_en": "Ugurcan Cakir", "number": 1, "position": "GK", "age": 29, "club": "特拉布宗"},
    ],
    "WAL": [
        {"name": "贝尔", "name_en": "Gareth Bale", "number": 11, "position": "FW", "age": 36, "club": "退役"},
        {"name": "拉姆塞", "name_en": "Aaron Ramsey", "number": 10, "position": "MF", "age": 35, "club": "卡迪夫城"},
        {"name": "詹姆斯", "name_en": "Daniel James", "number": 20, "position": "FW", "age": 28, "club": "利兹联"},
        {"name": "罗登", "name_en": "Joe Rodon", "number": 6, "position": "DF", "age": 28, "club": "利兹联"},
        {"name": "沃德", "name_en": "Danny Ward", "number": 1, "position": "GK", "age": 33, "club": "莱斯特城"},
    ],
    "TUN": [
        {"name": "赫纳伊西", "name_en": "Wahbi Khazri", "number": 10, "position": "FW", "age": 35, "club": "蒙彼利埃"},
        {"name": "斯利马尼", "name_en": "Youssef Msakni", "number": 7, "position": "FW", "age": 36, "club": "利雅得青年"},
        {"name": "利德里", "name_en": "Aissa Laidouni", "number": 14, "position": "MF", "age": 30, "club": "柏林联合"},
        {"name": "塔尔比", "name_en": "Montassar Talbi", "number": 6, "position": "DF", "age": 28, "club": "洛里昂"},
        {"name": "达赫曼", "name_en": "Aymen Dahmen", "number": 16, "position": "GK", "age": 29, "club": "蒙彼利埃"},
    ],
    "JAM": [
        {"name": "安东尼奥", "name_en": "Michail Antonio", "number": 9, "position": "FW", "age": 36, "club": "西汉姆"},
        {"name": "贝利", "name_en": "Leon Bailey", "number": 11, "position": "FW", "age": 29, "club": "阿斯顿维拉"},
        {"name": "尼科尔森", "name_en": "Shamar Nicholson", "number": 10, "position": "FW", "age": 28, "club": "斯帕达克"},
        {"name": "鲍威尔", "name_en": "Kemar Lawrence", "number": 20, "position": "DF", "age": 34, "club": "迈阿密国际"},
        {"name": "布莱克", "name_en": "Andre Blake", "number": 1, "position": "GK", "age": 35, "club": "费城联合"},
    ],
    # Group K
    "UKR": [
        {"name": "穆德里克", "name_en": "Mykhailo Mudryk", "number": 10, "position": "FW", "age": 25, "club": "切尔西"},
        {"name": "津琴科", "name_en": "Oleksandr Zinchenko", "number": 17, "position": "DF", "age": 29, "club": "阿森纳"},
        {"name": "多夫比克", "name_en": "Artem Dovbyk", "number": 9, "position": "FW", "age": 28, "club": "罗马"},
        {"name": "马利诺夫斯基", "name_en": "Ruslan Malinovskyi", "number": 8, "position": "MF", "age": 31, "club": "马赛"},
        {"name": "卢宁", "name_en": "Andriy Lunin", "number": 1, "position": "GK", "age": 27, "club": "皇家马德里"},
    ],
    "SCO": [
        {"name": "罗伯逊", "name_en": "Andrew Robertson", "number": 3, "position": "DF", "age": 32, "club": "利物浦"},
        {"name": "麦克金", "name_en": "John McGinn", "number": 7, "position": "MF", "age": 31, "club": "阿斯顿维拉"},
        {"name": "亚当斯", "name_en": "Che Adams", "number": 10, "position": "FW", "age": 29, "club": "都灵"},
        {"name": "麦克托米奈", "name_en": "Scott McTominay", "number": 4, "position": "MF", "age": 29, "club": "那不勒斯"},
        {"name": "冈恩", "name_en": "Angus Gunn", "number": 1, "position": "GK", "age": 30, "club": "诺维奇"},
    ],
    "ALG": [
        {"name": "马赫雷斯", "name_en": "Riyad Mahrez", "number": 7, "position": "FW", "age": 35, "club": "利雅得新月"},
        {"name": "布奈贾", "name_en": "Baghdad Bounedjah", "number": 9, "position": "FW", "age": 34, "club": "萨德"},
        {"name": "贝纳赛尔", "name_en": "Ismael Bennacer", "number": 8, "position": "MF", "age": 28, "club": "AC米兰"},
        {"name": "贝拉姆里", "name_en": "Djamel Benlamri", "number": 5, "position": "DF", "age": 36, "club": "里昂"},
        {"name": "穆斯塔法", "name_en": "Raïs M'Bolhi", "number": 16, "position": "GK", "age": 40, "club": "巴黎FC"},
    ],
    "HON": [
        {"name": "奎奥托", "name_en": "Romell Quioto", "number": 12, "position": "FW", "age": 35, "club": "蒙特利尔"},
        {"name": "洛萨诺", "name_en": "Alberth Elis", "number": 17, "position": "FW", "age": 28, "club": "波尔多"},
        {"name": "查韦斯", "name_en": "Anthony Lozano", "number": 9, "position": "FW", "age": 31, "club": "加的斯"},
        {"name": "伊萨吉雷", "name_en": "Emilio Izaguirre", "number": 7, "position": "DF", "age": 40, "club": "莫塔瓜"},
        {"name": "洛佩斯", "name_en": "Luis Lopez", "number": 1, "position": "GK", "age": 33, "club": "皇家西班牙"},
    ],
    # Group L
    "CZE": [
        {"name": "希克", "name_en": "Patrik Schick", "number": 9, "position": "FW", "age": 30, "club": "勒沃库森"},
        {"name": "绍切克", "name_en": "Tomas Soucek", "number": 28, "position": "MF", "age": 31, "club": "西汉姆"},
        {"name": "库赫塔", "name_en": "Adam Hlozek", "number": 17, "position": "FW", "age": 24, "club": "勒沃库森"},
        {"name": "科维奇", "name_en": "Vladimir Coufal", "number": 5, "position": "DF", "age": 33, "club": "西汉姆"},
        {"name": "瓦茨利克", "name_en": "Tomas Vaclik", "number": 1, "position": "GK", "age": 37, "club": "奥林匹亚科斯"},
    ],
    "NOR": [
        {"name": "哈兰德", "name_en": "Erling Haaland", "number": 9, "position": "FW", "age": 25, "club": "曼城"},
        {"name": "厄德高", "name_en": "Martin Odegaard", "number": 8, "position": "MF", "age": 27, "club": "阿森纳"},
        {"name": "瑟尔洛特", "name_en": "Alexander Sorloth", "number": 11, "position": "FW", "age": 30, "club": "马德里竞技"},
        {"name": "阿耶尔", "name_en": "Kristoffer Ajer", "number": 4, "position": "DF", "age": 28, "club": "布伦特福德"},
        {"name": "尼兰", "name_en": "Orjan Nyland", "number": 12, "position": "GK", "age": 35, "club": "塞维利亚"},
    ],
    "CIV": [
        {"name": "佩佩", "name_en": "Nicolas Pepe", "number": 19, "position": "FW", "age": 31, "club": "特拉布宗"},
        {"name": "凯西", "name_en": "Franck Kessie", "number": 8, "position": "MF", "age": 29, "club": "巴塞罗那"},
        {"name": "哈勒", "name_en": "Sebastien Haller", "number": 9, "position": "FW", "age": 32, "club": "多特蒙德"},
        {"name": "巴伊", "name_en": "Eric Bailly", "number": 2, "position": "DF", "age": 32, "club": "贝西克塔斯"},
        {"name": "桑加雷", "name_en": "Ibrahim Sangare", "number": 6, "position": "MF", "age": 28, "club": "诺丁汉森林"},
    ],
    "NZL": [
        {"name": "伍德", "name_en": "Chris Wood", "number": 9, "position": "FW", "age": 34, "club": "诺丁汉森林"},
        {"name": "萨维奇", "name_en": "Liberato Cacace", "number": 3, "position": "DF", "age": 25, "club": "恩波利"},
        {"name": "辛格", "name_en": "Sarpreet Singh", "number": 17, "position": "MF", "age": 25, "club": "雷根斯堡"},
        {"name": "怀纳马", "name_en": "Joe Bell", "number": 7, "position": "MF", "age": 26, "club": "布伦瑞克"},
        {"name": "马里诺维奇", "name_en": "Oliver Sail", "number": 1, "position": "GK", "age": 28, "club": "华沙军团"},
    ],
}

# ============================================================
# 世界杯 2026 比赛场馆（美国/墨西哥/加拿大 16 座场馆）
# ============================================================
VENUES = [
    "MetLife Stadium, New York",
    "SoFi Stadium, Los Angeles",
    "AT&T Stadium, Dallas",
    "Hard Rock Stadium, Miami",
    "NRG Stadium, Houston",
    "Mercedes-Benz Stadium, Atlanta",
    "Lumen Field, Seattle",
    "Lincoln Financial Field, Philadelphia",
    "Arrowhead Stadium, Kansas City",
    "Gillette Stadium, Boston",
    "Levi's Stadium, San Francisco",
    "BC Place, Vancouver",
    "BMO Field, Toronto",
    "Estadio Azteca, Mexico City",
    "Estadio BBVA, Monterrey",
    "Estadio Akron, Guadalajara",
]


async def seed():
    """种子数据入库"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        # ---- 1. 球队入库 ----
        team_map: dict[str, int] = {}
        for team_data in TEAMS:
            team = Team(**team_data)
            db.add(team)
            await db.flush()
            team_map[team_data["code"]] = team.id
            print(f"  Added team: {team_data['name']} ({team_data['code']}) - Group {team_data['group_name']}")

        # ---- 2. 球员入库 ----
        total_players = 0
        for code, players in PLAYERS.items():
            team_id = team_map[code]
            for p in players:
                # 默认世界杯统计数据
                stats = {
                    "goals": 0, "assists": 0, "appearances": 0,
                    "yellow_cards": 0, "red_cards": 0,
                    "shots": 0, "passes": 0, "minutes_played": 0,
                }
                player = Player(team_id=team_id, stats=stats, **p)
                db.add(player)
            total_players += len(players)
            print(f"  Added {len(players)} players for {code}")

        await db.flush()

        # ---- 3. 小组赛赛程（72 场） ----
        groups: dict[str, list[str]] = {}
        for t in TEAMS:
            g = t["group_name"]
            if g not in groups:
                groups[g] = []
            groups[g].append(t["code"])

        venue_idx = 0
        match_count = 0
        # 小组赛日期安排：每轮间隔 4 天
        md_dates = [
            datetime(2026, 6, 11, tzinfo=timezone.utc),  # MD1
            datetime(2026, 6, 15, tzinfo=timezone.utc),  # MD2
            datetime(2026, 6, 19, tzinfo=timezone.utc),  # MD3
        ]
        # 每天的开球时间（UTC）
        kick_off_hours = [16, 19, 22]

        for group_name, codes in sorted(groups.items()):
            # 每组 4 队的循环赛 = 6 场
            # MD1: 1v2, 3v4
            # MD2: 1v3, 4v2
            # MD3: 4v1, 2v3
            matchups = [
                (0, 1, 0),  # MD1
                (2, 3, 0),  # MD1
                (0, 2, 1),  # MD2
                (3, 1, 1),  # MD2
                (3, 0, 2),  # MD3
                (1, 2, 2),  # MD3
            ]
            for home_idx, away_idx, md in matchups:
                hour = kick_off_hours[match_count % 3]
                match_date = md_dates[md].replace(hour=hour)
                match = Match(
                    stage="group",
                    group_name=group_name,
                    home_team_id=team_map[codes[home_idx]],
                    away_team_id=team_map[codes[away_idx]],
                    status="upcoming",
                    start_time=match_date,
                    venue=VENUES[venue_idx % len(VENUES)],
                    matchday=md + 1,
                )
                db.add(match)
                venue_idx += 1
                match_count += 1

            print(f"  Added 6 group matches for Group {group_name}")

        # ---- 4. 淘汰赛赛程（32 场） ----
        # 32 强赛（16 场）6/25 - 6/28
        knockout_base = datetime(2026, 6, 25, tzinfo=timezone.utc)
        for i in range(16):
            day_offset = i // 4
            hour = kick_off_hours[i % 3]
            match = Match(
                stage="round_32",
                group_name=None,
                home_team_id=team_map["USA"],  # 占位，赛后根据出线更新
                away_team_id=team_map["MEX"],
                status="upcoming",
                start_time=knockout_base + timedelta(days=day_offset, hours=hour),
                venue=VENUES[venue_idx % len(VENUES)],
                matchday=None,
            )
            db.add(match)
            venue_idx += 1
            match_count += 1
        print(f"  Added 16 round of 32 matches")

        # 16 强赛（8 场）7/1 - 7/2
        r16_base = datetime(2026, 7, 1, tzinfo=timezone.utc)
        for i in range(8):
            day_offset = i // 4
            hour = kick_off_hours[i % 3]
            match = Match(
                stage="round_16",
                group_name=None,
                home_team_id=team_map["USA"],
                away_team_id=team_map["MEX"],
                status="upcoming",
                start_time=r16_base + timedelta(days=day_offset, hours=hour),
                venue=VENUES[venue_idx % len(VENUES)],
                matchday=None,
            )
            db.add(match)
            venue_idx += 1
            match_count += 1
        print(f"  Added 8 round of 16 matches")

        # 四分之一决赛（4 场）7/5 - 7/6
        qf_base = datetime(2026, 7, 5, tzinfo=timezone.utc)
        for i in range(4):
            day_offset = i // 2
            hour = kick_off_hours[i % 2]
            match = Match(
                stage="quarter",
                group_name=None,
                home_team_id=team_map["USA"],
                away_team_id=team_map["MEX"],
                status="upcoming",
                start_time=qf_base + timedelta(days=day_offset, hours=hour),
                venue=VENUES[venue_idx % len(VENUES)],
                matchday=None,
            )
            db.add(match)
            venue_idx += 1
            match_count += 1
        print(f"  Added 4 quarter-final matches")

        # 半决赛（2 场）7/9 - 7/10
        sf_base = datetime(2026, 7, 9, tzinfo=timezone.utc)
        for i in range(2):
            match = Match(
                stage="semi",
                group_name=None,
                home_team_id=team_map["USA"],
                away_team_id=team_map["MEX"],
                status="upcoming",
                start_time=sf_base + timedelta(days=i, hours=19),
                venue=VENUES[venue_idx % len(VENUES)],
                matchday=None,
            )
            db.add(match)
            venue_idx += 1
            match_count += 1
        print(f"  Added 2 semi-final matches")

        # 三四名决赛（1 场）7/13
        match = Match(
            stage="third_place",
            group_name=None,
            home_team_id=team_map["USA"],
            away_team_id=team_map["MEX"],
            status="upcoming",
            start_time=datetime(2026, 7, 13, 19, 0, tzinfo=timezone.utc),
            venue="MetLife Stadium, New York",
            matchday=None,
        )
        db.add(match)
        match_count += 1
        print(f"  Added third-place match")

        # 决赛（1 场）7/19
        match = Match(
            stage="final",
            group_name=None,
            home_team_id=team_map["USA"],
            away_team_id=team_map["MEX"],
            status="upcoming",
            start_time=datetime(2026, 7, 19, 19, 0, tzinfo=timezone.utc),
            venue="MetLife Stadium, New York",
            matchday=None,
        )
        db.add(match)
        match_count += 1
        print(f"  Added final match")

        await db.commit()
        print(f"\nSeed data imported successfully!")
        print(f"  Teams: {len(TEAMS)}")
        print(f"  Players: {total_players}")
        print(f"  Matches: {match_count} (72 group + 32 knockout = 104)")


if __name__ == "__main__":
    print("Seeding World Cup 2026 data (48 teams / 12 groups / 104 matches)...")
    asyncio.run(seed())
