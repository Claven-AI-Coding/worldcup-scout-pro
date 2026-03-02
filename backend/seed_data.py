"""Seed data script for World Cup 2026.

Usage:
    python scripts/seed_data.py

Populates the database with:
- 32 teams (with group assignments)
- Sample players for key teams
- Sample group stage matches
"""

import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.config import settings  # noqa: E402
from app.database import async_session, engine  # noqa: E402
from app.models import Match, Player, Team  # noqa: E402
from app.database import Base  # noqa: E402

# FIFA World Cup 2026 - 32 teams (projected)
TEAMS = [
    # Group A
    {"name": "美国", "name_en": "USA", "code": "USA", "group_name": "A", "coach": "波切蒂诺"},
    {"name": "墨西哥", "name_en": "Mexico", "code": "MEX", "group_name": "A", "coach": "阿吉雷"},
    {"name": "加拿大", "name_en": "Canada", "code": "CAN", "group_name": "A", "coach": "马尔施"},
    {"name": "塞内加尔", "name_en": "Senegal", "code": "SEN", "group_name": "A", "coach": "西塞"},
    # Group B
    {"name": "阿根廷", "name_en": "Argentina", "code": "ARG", "group_name": "B", "coach": "斯卡洛尼"},
    {"name": "澳大利亚", "name_en": "Australia", "code": "AUS", "group_name": "B", "coach": "波波维奇"},
    {"name": "尼日利亚", "name_en": "Nigeria", "code": "NGA", "group_name": "B", "coach": "佩塞罗"},
    {"name": "秘鲁", "name_en": "Peru", "code": "PER", "group_name": "B", "coach": "弗萨蒂"},
    # Group C
    {"name": "法国", "name_en": "France", "code": "FRA", "group_name": "C", "coach": "德尚"},
    {"name": "丹麦", "name_en": "Denmark", "code": "DEN", "group_name": "C", "coach": "胡尔曼德"},
    {"name": "沙特阿拉伯", "name_en": "Saudi Arabia", "code": "KSA", "group_name": "C", "coach": "曼奇尼"},
    {"name": "厄瓜多尔", "name_en": "Ecuador", "code": "ECU", "group_name": "C", "coach": "贝塞拉"},
    # Group D
    {"name": "巴西", "name_en": "Brazil", "code": "BRA", "group_name": "D", "coach": "多里瓦尔"},
    {"name": "日本", "name_en": "Japan", "code": "JPN", "group_name": "D", "coach": "森保一"},
    {"name": "塞尔维亚", "name_en": "Serbia", "code": "SRB", "group_name": "D", "coach": "皮克西"},
    {"name": "喀麦隆", "name_en": "Cameroon", "code": "CMR", "group_name": "D", "coach": "松"},
    # Group E
    {"name": "英格兰", "name_en": "England", "code": "ENG", "group_name": "E", "coach": "图赫尔"},
    {"name": "荷兰", "name_en": "Netherlands", "code": "NED", "group_name": "E", "coach": "科曼"},
    {"name": "韩国", "name_en": "South Korea", "code": "KOR", "group_name": "E", "coach": "洪明甫"},
    {"name": "乌拉圭", "name_en": "Uruguay", "code": "URU", "group_name": "E", "coach": "比尔萨"},
    # Group F
    {"name": "西班牙", "name_en": "Spain", "code": "ESP", "group_name": "F", "coach": "德拉富恩特"},
    {"name": "德国", "name_en": "Germany", "code": "GER", "group_name": "F", "coach": "纳格尔斯曼"},
    {"name": "哥伦比亚", "name_en": "Colombia", "code": "COL", "group_name": "F", "coach": "洛伦索"},
    {"name": "摩洛哥", "name_en": "Morocco", "code": "MAR", "group_name": "F", "coach": "雷格拉吉"},
    # Group G
    {"name": "葡萄牙", "name_en": "Portugal", "code": "POR", "group_name": "G", "coach": "马丁内斯"},
    {"name": "瑞士", "name_en": "Switzerland", "code": "SUI", "group_name": "G", "coach": "亚金"},
    {"name": "加纳", "name_en": "Ghana", "code": "GHA", "group_name": "G", "coach": "阿杜"},
    {"name": "伊朗", "name_en": "Iran", "code": "IRN", "group_name": "G", "coach": "盖拉尼"},
    # Group H
    {"name": "意大利", "name_en": "Italy", "code": "ITA", "group_name": "H", "coach": "斯帕莱蒂"},
    {"name": "克罗地亚", "name_en": "Croatia", "code": "CRO", "group_name": "H", "coach": "达利奇"},
    {"name": "智利", "name_en": "Chile", "code": "CHI", "group_name": "H", "coach": "加雷卡"},
    {"name": "波兰", "name_en": "Poland", "code": "POL", "group_name": "H", "coach": "普罗比茨"},
]

# Sample players for key teams
PLAYERS = {
    "ARG": [
        {"name": "梅西", "name_en": "Lionel Messi", "number": 10, "position": "FW", "age": 38, "club": "迈阿密国际"},
        {"name": "阿尔瓦雷斯", "name_en": "Julian Alvarez", "number": 9, "position": "FW", "age": 26, "club": "马德里竞技"},
        {"name": "德保罗", "name_en": "Rodrigo De Paul", "number": 7, "position": "MF", "age": 32, "club": "马德里竞技"},
        {"name": "麦卡利斯特", "name_en": "Alexis Mac Allister", "number": 20, "position": "MF", "age": 27, "club": "利物浦"},
        {"name": "马丁内斯", "name_en": "Emiliano Martinez", "number": 23, "position": "GK", "age": 33, "club": "阿斯顿维拉"},
    ],
    "FRA": [
        {"name": "姆巴佩", "name_en": "Kylian Mbappe", "number": 10, "position": "FW", "age": 27, "club": "皇家马德里"},
        {"name": "格列兹曼", "name_en": "Antoine Griezmann", "number": 7, "position": "FW", "age": 35, "club": "马德里竞技"},
        {"name": "琼阿梅尼", "name_en": "Aurelien Tchouameni", "number": 8, "position": "MF", "age": 26, "club": "皇家马德里"},
        {"name": "坎特", "name_en": "N'Golo Kante", "number": 13, "position": "MF", "age": 35, "club": "伊蒂哈德"},
        {"name": "梅尼昂", "name_en": "Mike Maignan", "number": 16, "position": "GK", "age": 31, "club": "AC米兰"},
    ],
    "BRA": [
        {"name": "维尼修斯", "name_en": "Vinicius Jr", "number": 7, "position": "FW", "age": 25, "club": "皇家马德里"},
        {"name": "罗德里戈", "name_en": "Rodrygo", "number": 11, "position": "FW", "age": 25, "club": "皇家马德里"},
        {"name": "卡塞米罗", "name_en": "Casemiro", "number": 5, "position": "MF", "age": 34, "club": "曼联"},
        {"name": "帕奎塔", "name_en": "Lucas Paqueta", "number": 10, "position": "MF", "age": 28, "club": "西汉姆"},
        {"name": "阿利松", "name_en": "Alisson", "number": 1, "position": "GK", "age": 33, "club": "利物浦"},
    ],
    "ENG": [
        {"name": "凯恩", "name_en": "Harry Kane", "number": 9, "position": "FW", "age": 32, "club": "拜仁慕尼黑"},
        {"name": "贝林厄姆", "name_en": "Jude Bellingham", "number": 10, "position": "MF", "age": 22, "club": "皇家马德里"},
        {"name": "萨卡", "name_en": "Bukayo Saka", "number": 7, "position": "FW", "age": 24, "club": "阿森纳"},
        {"name": "赖斯", "name_en": "Declan Rice", "number": 4, "position": "MF", "age": 27, "club": "阿森纳"},
        {"name": "皮克福德", "name_en": "Jordan Pickford", "number": 1, "position": "GK", "age": 32, "club": "埃弗顿"},
    ],
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
}

# World Cup 2026 venues (USA, Mexico, Canada)
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
    "Estadio Azteca, Mexico City",
    "BMO Field, Toronto",
]


async def seed():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        # Seed teams
        team_map = {}
        for team_data in TEAMS:
            team = Team(**team_data)
            db.add(team)
            await db.flush()
            team_map[team_data["code"]] = team.id
            print(f"  Added team: {team_data['name']} ({team_data['code']})")

        # Seed players
        for code, players in PLAYERS.items():
            team_id = team_map[code]
            for p in players:
                player = Player(team_id=team_id, **p)
                db.add(player)
            print(f"  Added {len(players)} players for {code}")

        await db.flush()

        # Seed group stage matches (matchday 1)
        groups = {}
        for t in TEAMS:
            g = t["group_name"]
            if g not in groups:
                groups[g] = []
            groups[g].append(t["code"])

        match_id = 1
        base_date = datetime(2026, 6, 11, 18, 0, tzinfo=timezone.utc)
        venue_idx = 0

        for group_name, codes in sorted(groups.items()):
            # MD1: 1v2, 3v4
            for i in range(0, len(codes), 2):
                if i + 1 < len(codes):
                    match = Match(
                        stage="group",
                        group_name=group_name,
                        home_team_id=team_map[codes[i]],
                        away_team_id=team_map[codes[i + 1]],
                        status="upcoming",
                        start_time=base_date,
                        venue=VENUES[venue_idx % len(VENUES)],
                        matchday=1,
                    )
                    db.add(match)
                    venue_idx += 1

            # MD2: 1v3, 2v4
            match = Match(
                stage="group",
                group_name=group_name,
                home_team_id=team_map[codes[0]],
                away_team_id=team_map[codes[2]],
                status="upcoming",
                start_time=datetime(2026, 6, 15, 18, 0, tzinfo=timezone.utc),
                venue=VENUES[venue_idx % len(VENUES)],
                matchday=2,
            )
            db.add(match)
            venue_idx += 1

            match = Match(
                stage="group",
                group_name=group_name,
                home_team_id=team_map[codes[1]],
                away_team_id=team_map[codes[3]],
                status="upcoming",
                start_time=datetime(2026, 6, 15, 21, 0, tzinfo=timezone.utc),
                venue=VENUES[venue_idx % len(VENUES)],
                matchday=2,
            )
            db.add(match)
            venue_idx += 1

            # MD3: 1v4, 2v3
            match = Match(
                stage="group",
                group_name=group_name,
                home_team_id=team_map[codes[0]],
                away_team_id=team_map[codes[3]],
                status="upcoming",
                start_time=datetime(2026, 6, 19, 18, 0, tzinfo=timezone.utc),
                venue=VENUES[venue_idx % len(VENUES)],
                matchday=3,
            )
            db.add(match)
            venue_idx += 1

            match = Match(
                stage="group",
                group_name=group_name,
                home_team_id=team_map[codes[1]],
                away_team_id=team_map[codes[2]],
                status="upcoming",
                start_time=datetime(2026, 6, 19, 21, 0, tzinfo=timezone.utc),
                venue=VENUES[venue_idx % len(VENUES)],
                matchday=3,
            )
            db.add(match)
            venue_idx += 1

            print(f"  Added 6 matches for Group {group_name}")

        await db.commit()
        print("\nSeed data imported successfully!")
        print(f"  Teams: {len(TEAMS)}")
        print(f"  Players: {sum(len(p) for p in PLAYERS.values())}")
        print(f"  Matches: {len(groups) * 6}")


if __name__ == "__main__":
    print("Seeding World Cup 2026 data...")
    asyncio.run(seed())
