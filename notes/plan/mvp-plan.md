# 世界杯全能助手・球探 Pro — MVP 实施计划

## Context

构建一款世界杯全能助手产品，15 天内上线 MVP。核心定位：赛事工具 + 社区互动 + AI 创意生成。

## 技术选型

| 层级 | 技术 | 理由 |
|------|------|------|
| 后端 | Python 3.12 + FastAPI | 开发极快，AI 集成方便 |
| 前端 Web | Vue 3 + Vite + TailwindCSS | 轻量高效，国内生态好 |
| 小程序 | uni-app (Vue 3) | 一套代码多端复用 |
| 数据库 | PostgreSQL 16 | 主库，JSONB 存储灵活数据 |
| 缓存 | Redis 7 | 实时比分缓存、排行榜、消息队列 |
| 实时推送 | WebSocket (FastAPI) | 赛程提醒、比分实时更新 |
| AI 壁纸 | Stable Diffusion API / DALL-E | 球队主题壁纸生成 |
| AI 分析 | Claude API | 赛事分析文案 |
| 任务队列 | Celery + Redis | 定时提醒、壁纸生成异步任务 |
| 部署 | Docker Compose | 一键启动开发/生产环境 |

## 五大核心模块

### 模块 1：赛程 + 提醒
- 世界杯完整赛程表（小组赛→淘汰赛→决赛）
- 比赛实时比分 WebSocket 推送
- 用户订阅关注球队，赛前 N 分钟提醒（站内 + 微信模板消息）
- 数据源：Football-Data.org 免费 API

### 模块 2：基础数据
- 32 支参赛球队资料（阵容、教练、历史战绩）
- 球员数据库（身价、位置、数据统计、职业履历）
- 小组积分榜、射手榜、助攻榜实时排名
- 数据源：API-Football 免费层 + 静态种子数据

### 模块 3：球队圈子
- 每支球队一个专属讨论圈
- 发帖（文字 + 图片）、评论、点赞
- 热门帖子排序、圈子活跃度排行
- 用户主队认证标识

### 模块 4：竞猜积分
- 每场比赛开放竞猜（胜/平/负 + 比分预测）
- 虚拟积分制（非现金），注册送初始积分
- 全站积分排行榜（日榜/总榜）
- 连胜奖励、大神称号系统

### 模块 5：壁纸生成
- 选择球队/球员 → AI 生成专属壁纸
- 多种风格模板（赛博朋克、水墨、漫画、极简）
- 生成后可下载/分享到朋友圈
- 每日免费生成次数限制 + 积分兑换

## 项目结构

```
worldcup-scout-pro/
├── CLAUDE.md                    # 项目宪法
├── docker-compose.yml           # 一键启动
├── docker-compose.prod.yml      # 生产配置
├── .env.example                 # 环境变量模板
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml           # uv 包管理
│   ├── alembic/                 # 数据库迁移
│   │   └── versions/
│   ├── app/
│   │   ├── main.py              # FastAPI 入口
│   │   ├── config.py            # 配置管理
│   │   ├── database.py          # DB 连接
│   │   ├── models/              # SQLAlchemy 模型
│   │   │   ├── user.py
│   │   │   ├── match.py
│   │   │   ├── team.py
│   │   │   ├── player.py
│   │   │   ├── post.py
│   │   │   ├── prediction.py
│   │   │   └── wallpaper.py
│   │   ├── schemas/             # Pydantic 校验
│   │   ├── api/                 # 路由
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── matches.py
│   │   │   │   ├── teams.py
│   │   │   │   ├── players.py
│   │   │   │   ├── community.py
│   │   │   │   ├── predictions.py
│   │   │   │   └── wallpapers.py
│   │   │   └── websocket.py
│   │   ├── services/            # 业务逻辑
│   │   │   ├── match_service.py
│   │   │   ├── data_sync.py     # 外部 API 数据同步
│   │   │   ├── reminder.py      # 提醒服务
│   │   │   ├── prediction.py    # 竞猜结算
│   │   │   ├── wallpaper.py     # AI 壁纸生成
│   │   │   └── ai_analysis.py   # AI 赛事分析
│   │   ├── tasks/               # Celery 异步任务
│   │   │   ├── sync_matches.py
│   │   │   ├── send_reminders.py
│   │   │   └── generate_wallpaper.py
│   │   └── utils/
│   │       ├── football_api.py  # 外部 API 封装
│   │       └── auth.py          # JWT 工具
│   └── tests/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── router/
│   │   ├── stores/              # Pinia 状态管理
│   │   ├── api/                 # API 请求封装
│   │   ├── composables/         # 组合式函数
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── match/           # 赛程组件
│   │   │   ├── team/            # 球队组件
│   │   │   ├── community/       # 圈子组件
│   │   │   ├── prediction/      # 竞猜组件
│   │   │   └── wallpaper/       # 壁纸组件
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── Schedule.vue
│   │   │   ├── TeamDetail.vue
│   │   │   ├── PlayerDetail.vue
│   │   │   ├── Community.vue
│   │   │   ├── Prediction.vue
│   │   │   ├── Wallpaper.vue
│   │   │   └── Profile.vue
│   │   └── assets/
│   └── public/
├── miniprogram/                 # uni-app 小程序
│   ├── package.json
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── utils/
│   └── manifest.json
└── scripts/
    ├── seed_data.py             # 种子数据导入
    └── init_db.sh               # 数据库初始化
```

## 数据库核心表设计

- **users**: id, openid, nickname, avatar, fav_team_id, points, created_at
- **teams**: id, name, code, group, flag_url, coach, description, stats(jsonb)
- **players**: id, team_id, name, number, position, age, club, stats(jsonb)
- **matches**: id, stage, group, home_team_id, away_team_id, home_score, away_score, status(upcoming/live/finished), start_time, venue
- **match_events**: id, match_id, type(goal/card/sub), minute, player_id, detail
- **posts**: id, user_id, team_id, content, images(jsonb), likes, comments_count, created_at
- **comments**: id, post_id, user_id, content, created_at
- **predictions**: id, user_id, match_id, predicted_result, predicted_score, points_earned, created_at
- **wallpapers**: id, user_id, team_id, player_id, style, prompt, image_url, created_at
- **reminders**: id, user_id, match_id, remind_before_minutes, sent

## 15 天冲刺排期

| 天 | 任务 | 产出 |
|----|------|------|
| D1 | 项目初始化、Docker 环境、DB 建表、CLAUDE.md | 项目骨架可运行 |
| D2 | 用户认证 (JWT + 微信 OAuth)、基础 API 框架 | 登录注册可用 |
| D3 | 赛程模块后端 + 外部 API 数据同步 | 赛程数据入库 |
| D4 | 赛程前端页面 + 实时比分 WebSocket | 赛程页面可用 |
| D5 | 提醒服务 (Celery 定时任务 + 推送) | 赛前提醒可用 |
| D6 | 球队/球员数据模块后端 + 种子数据 | 数据 API 可用 |
| D7 | 球队/球员前端页面 (列表 + 详情) | 数据浏览可用 |
| D8 | 球队圈子后端 (发帖/评论/点赞) | 社区 API 可用 |
| D9 | 球队圈子前端页面 | 社区功能可用 |
| D10 | 竞猜模块后端 (下注/结算/排行) | 竞猜 API 可用 |
| D11 | 竞猜前端页面 + 排行榜 | 竞猜功能可用 |
| D12 | AI 壁纸生成后端 + 前端 | 壁纸功能可用 |
| D13 | uni-app 小程序核心页面移植 | 小程序基础可用 |
| D14 | 全端联调、Bug 修复、UI 打磨 | 全功能可测 |
| D15 | 部署上线、小程序提审、监控配置 | 正式上线 |

## API 设计概览

```
POST   /api/v1/auth/login          # 登录
POST   /api/v1/auth/wx-login       # 微信登录
GET    /api/v1/matches              # 赛程列表 (?stage=group&date=)
GET    /api/v1/matches/:id          # 比赛详情
GET    /api/v1/matches/:id/events   # 比赛事件
POST   /api/v1/matches/:id/remind   # 设置提醒
WS     /api/v1/ws/live/:match_id    # 实时比分推送

GET    /api/v1/teams                # 球队列表
GET    /api/v1/teams/:id            # 球队详情
GET    /api/v1/teams/:id/players    # 球队球员
GET    /api/v1/players/:id          # 球员详情
GET    /api/v1/standings            # 积分榜

GET    /api/v1/community/:team_id/posts  # 圈子帖子
POST   /api/v1/community/posts      # 发帖
POST   /api/v1/community/posts/:id/like     # 点赞
POST   /api/v1/community/posts/:id/comment  # 评论

GET    /api/v1/predictions/matches/:id  # 比赛竞猜信息
POST   /api/v1/predictions              # 提交竞猜
GET    /api/v1/predictions/leaderboard   # 排行榜
GET    /api/v1/predictions/my            # 我的竞猜

POST   /api/v1/wallpapers/generate   # 生成壁纸
GET    /api/v1/wallpapers/my         # 我的壁纸
GET    /api/v1/wallpapers/gallery    # 壁纸广场
```

## 部署方案

- 开发环境：`docker-compose up` 一键启动 (FastAPI + PostgreSQL + Redis + Celery)
- 生产环境：阿里云 ECS / 腾讯云轻量服务器
- 小程序：微信公众平台提审
- 域名 + SSL + Nginx 反代

## 验证方式

1. `docker-compose up` 启动全部服务
2. 访问 `http://localhost:8000/docs` 验证后端 API (Swagger)
3. 访问 `http://localhost:5173` 验证前端页面
4. 运行 `pytest` 通过后端单元测试
5. 小程序开发者工具预览

## 文件生成顺序

实施时按以下顺序生成文件：
1. CLAUDE.md（项目宪法）
2. docker-compose.yml + .env.example
3. backend/ 骨架（FastAPI + 模型 + 迁移）
4. frontend/ 骨架（Vue 3 + 路由 + 基础组件）
5. 种子数据脚本
6. 各功能模块逐步填充
