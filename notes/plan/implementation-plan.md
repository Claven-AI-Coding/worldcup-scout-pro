# 2026 美加墨世界杯·球探 Pro — 全面实施计划

> 基于 PRD V1.0 产品需求文档，结合现有代码库分析，制定分阶段实施计划。

---

## 一、PRD 与现有实现差异分析

### 1.1 关键数据差异

| 维度 | PRD 要求 | 现有实现 | 差距 |
|------|---------|---------|------|
| 参赛球队 | **48 支**（2026 扩军） | 32 支 | 需新增 16 支球队 |
| 小组数量 | **12 组**（每组 4 队） | 8 组 | 需重构分组 |
| 总比赛场次 | **104 场** | 48 场（仅小组赛） | 需补充淘汰赛 56 场 |
| 出线规则 | 小组前 2 + 最好 4 个小组第三 | 小组前 2 | 需新增第三名排名逻辑 |
| 底部导航 | 首页/赛程/**数据**/社交/我的 | 首页/赛程/圈子/竞猜/我的 | Tab 结构需调整 |

### 1.2 模块差异

| PRD 模块 | 优先级 | 现有实现 | 差距说明 |
|----------|--------|---------|---------|
| 模块 1：智能赛程与提醒 | P0 | ✅ 80% | 缺少：赛程筛选（按小组/球队/阶段）、已结束赛事灰化、进行中红色标注、出线形势展示 |
| 模块 2：AI 球探·深度数据 | P1 | ✅ 60% | 缺少：战力数据可视化、历史交锋记录、伤病信息、AI 赛果预测（胜率/比分区间）、射手榜/助攻榜 |
| 模块 3：世界杯社交场 | P2 | ✅ 70% | 缺少：圈主管理、热门排序算法、违规检测、竞猜扩展（比分区间/进球数/关键球员）、积分任务系统、勋章系统、世界杯足迹 |
| 模块 4：观赛场景工具 | P2 | ❌ 0% | 全新模块：观赛套餐推荐、应援物料生成（壁纸/头像/海报/文案） |
| 模块 5：内容创作工具箱 | P2 | ❌ 0% | 全新模块：AI 战报生成、高光片段文案、热门话题库 |
| 模块 6：个人中心与会员体系 | P1 | ⚠️ 30% | 缺少：会员体系（月卡/季卡/年卡）、支付接口、会员权益控制、积分明细、安全记录 |
| 模块 7：合规与风控 | P0 | ❌ 0% | 全新模块：关键词过滤、违规检测、举报审核、隐私政策、用户协议 |

### 1.3 设计规范差异

| 维度 | PRD 要求 | 现有实现 |
|------|---------|---------|
| 主色调 | 足球绿 + 白色，辅助红/蓝 | TailwindCSS 默认蓝色系 |
| 图标风格 | 统一线性图标 | 无统一图标体系 |
| 已结束赛事 | 灰色弱化 | 无区分 |
| 进行中赛事 | 红色标注"直播中" | 有 LiveScore 组件但样式不完善 |
| 数据图表 | 折线图/柱状图/环形图 | 无图表库 |

---

## 二、版本规划总览

```
V1.0 MVP（15 天）──→ 测试优化（5 天）──→ V1.1 爆发期（10 天）──→ V1.2 长尾期（10 天）
   5月1日预热                                  6月1日前完成            7月20日前完成
```

### 版本范围

| 版本 | 包含模块 | 核心目标 |
|------|---------|---------|
| **V1.0 MVP** | 模块 1（P0）+ 模块 2 核心（P1）+ 模块 3 核心（P2）+ 模块 4 核心（P2）+ 模块 6 核心（P1）+ 模块 7（P0） | 基础刚需可用，合规达标 |
| **V1.1** | 模块 3 完整 + 模块 5 + 模块 6 完整 | 社交爆发 + 内容创作 + 变现 |
| **V1.2** | 全模块完善 + 数据可视化 + 长尾功能 | 功能闭环，长期留存 |

---

## 三、技术架构升级

### 3.1 技术栈调整

| 层级 | 现有 | 新增/调整 | 用途 |
|------|------|----------|------|
| 后端 | FastAPI + SQLAlchemy + Alembic | + **slowapi**（限流） | API 限流保护 |
| 后端 | — | + **better-profanity / 自定义词库** | 违规内容检测 |
| 前端 | Vue 3 + TailwindCSS | + **ECharts**（图表库） | 数据可视化 |
| 前端 | — | + **lucide-vue-next**（图标库） | 统一线性图标 |
| 前端 | — | 调整 TailwindCSS 主题色 | 足球绿主色调 |
| 支付 | — | + 微信支付 / 支付宝 SDK | 会员订阅（V1.1） |

### 3.2 数据库 Schema 变更

#### 需修改的表

```sql
-- teams: group_name 从 A-H 扩展到 A-L（12组）
ALTER TABLE teams ALTER COLUMN group_name TYPE VARCHAR(2);

-- users: 新增会员字段
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users ADD COLUMN is_member BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN member_expire_at TIMESTAMP;
ALTER TABLE users ADD COLUMN member_type VARCHAR(20);  -- monthly/quarterly/yearly
ALTER TABLE users ADD COLUMN daily_sign_in DATE;       -- 每日签到
ALTER TABLE users ADD COLUMN badges JSONB DEFAULT '[]'; -- 勋章列表
```

#### 需新增的表

```sql
-- 积分流水记录
CREATE TABLE point_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    amount INTEGER NOT NULL,        -- 正=获取，负=扣除
    reason VARCHAR(50) NOT NULL,    -- sign_in/prediction/task/exchange
    detail VARCHAR(200),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 用户任务系统
CREATE TABLE user_tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    task_type VARCHAR(50) NOT NULL, -- daily_sign_in/view_schedule/share/join_circle/predict
    completed BOOLEAN DEFAULT FALSE,
    points_reward INTEGER NOT NULL,
    completed_at TIMESTAMP,
    date DATE NOT NULL              -- 任务所属日期
);

-- 举报记录
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    reporter_id INTEGER REFERENCES users(id),
    target_type VARCHAR(20) NOT NULL, -- post/comment/user
    target_id INTEGER NOT NULL,
    reason VARCHAR(200),
    status VARCHAR(20) DEFAULT 'pending', -- pending/reviewed/dismissed
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 违禁词库
CREATE TABLE banned_words (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50),           -- profanity/gambling/political/spam
    created_at TIMESTAMP DEFAULT NOW()
);

-- AI 生成内容（V1.1）
CREATE TABLE ai_contents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    match_id INTEGER REFERENCES matches(id),
    content_type VARCHAR(30) NOT NULL, -- preview/summary/highlight/meme
    style VARCHAR(20),              -- serious/funny/passionate
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 用户足迹与勋章（V1.1）
CREATE TABLE user_footprints (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action_type VARCHAR(30) NOT NULL, -- view_match/join_circle/post/predict/sign_in
    target_id INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3.3 导航结构调整

```
当前底部 Tab：首页 | 赛程 | 圈子 | 竞猜 | 我的
PRD 底部 Tab： 首页 | 赛程 | 数据 | 社交 | 我的

调整方案：
  首页 → 保持（核心入口，快捷导航）
  赛程 → 保持（赛程列表 + 筛选 + 提醒）
  数据 → 新增（球队/球员数据 + AI 预测 + 排行榜）
  社交 → 合并（球迷圈 + 竞猜 + 足迹）
  我的 → 扩展（个人中心 + 会员 + 积分 + 设置）
```

### 3.4 新增 API 端点

```
# ---- 合规与风控 ----
POST   /api/v1/reports                    # 举报内容/用户
GET    /api/v1/legal/privacy-policy       # 隐私政策
GET    /api/v1/legal/user-agreement       # 用户协议

# ---- 积分任务 ----
GET    /api/v1/tasks/daily                # 每日任务列表
POST   /api/v1/tasks/:task_id/complete    # 完成任务
POST   /api/v1/sign-in                    # 每日签到
GET    /api/v1/points/records             # 积分流水

# ---- AI 数据分析 ----
GET    /api/v1/matches/:id/prediction     # AI 赛果预测（胜率/比分区间）
GET    /api/v1/matches/:id/preview        # AI 赛前分析
GET    /api/v1/matches/:id/summary        # AI 赛后总结

# ---- 排行榜扩展 ----
GET    /api/v1/rankings/scorers           # 射手榜
GET    /api/v1/rankings/assists           # 助攻榜

# ---- 会员（V1.1） ----
GET    /api/v1/membership/plans           # 会员套餐
POST   /api/v1/membership/subscribe       # 订阅会员
GET    /api/v1/membership/status          # 会员状态

# ---- 内容创作（V1.1） ----
POST   /api/v1/ai-content/generate        # AI 生成内容
GET    /api/v1/ai-content/my              # 我的生成记录
GET    /api/v1/topics/trending            # 热门话题

# ---- 社交扩展（V1.1） ----
GET    /api/v1/footprint/my               # 我的足迹
GET    /api/v1/badges/my                  # 我的勋章
WS     /api/v1/ws/chat/:match_id          # 赛中聊天室
```

---

## 四、V1.0 MVP 15 天冲刺计划

> MVP 范围：PRD 第五章明确的 P0 + 核心 P1 功能

### 阶段一：基础重构（D1-D3）

#### D1：数据层重构 — 48 队 / 12 组 / 104 场

**目标**：将 32 队 8 组升级为 48 队 12 组，补全淘汰赛赛程

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 1.1 更新种子数据 | 新增 16 支球队（亚洲/非洲/中北美增补），调整为 12 组（A-L） | `scripts/seed_data.py` |
| 1.2 补全赛程 | 48 场小组赛 + 32 场 32 强赛 + 16 场 16 强赛 + 8 场 1/4 决赛 + 4 场半决赛 + 决赛 + 三四名 = 104 场 | `scripts/seed_data.py` |
| 1.3 更新出线规则 | 小组前 2（24 队）+ 8 个最佳小组第三 = 32 队进入淘汰赛 | `backend/app/api/v1/matches.py` |
| 1.4 数据库迁移 | 新增表（point_records, user_tasks, reports, banned_words），users 表新增字段 | `alembic/versions/002_*.py` |
| 1.5 新增球员数据 | 每队至少 5 名核心球员，共 240+ 球员 | `scripts/seed_data.py` |

**验证**：`GET /api/v1/teams` 返回 48 队，`GET /api/v1/matches` 返回 104 场

#### D2：合规与风控基础（P0）

**目标**：关键词过滤系统 + 免责声明 + 隐私政策

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 2.1 违禁词库 | 初始化中文违禁词库（脏话/赌博/政治敏感词），存入 banned_words 表 | `scripts/seed_banned_words.py` |
| 2.2 内容过滤中间件 | 发帖/评论/昵称过滤，命中违禁词自动拦截 | `backend/app/utils/content_filter.py` |
| 2.3 举报 API | POST 举报接口 + 举报记录查询 | `backend/app/api/v1/reports.py` |
| 2.4 法律文本 | 隐私政策、用户协议、免责声明（静态文本 API） | `backend/app/api/v1/legal.py` |
| 2.5 注册流程 | 注册时需同意用户协议 + 隐私政策 | `backend/app/api/v1/auth.py` |

**验证**：发帖包含违禁词返回 400，举报接口可用，法律文本可访问

#### D3：赛程模块升级（P0）

**目标**：完善赛程展示、筛选、已结束/进行中状态视觉区分

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 3.1 赛程筛选 API | 支持按小组、球队、赛事阶段、日期组合筛选 | `backend/app/api/v1/matches.py` |
| 3.2 小组分组展示 | 12 组积分榜，含积分/净胜球/进球/失球，按官方规则排序 | `backend/app/api/v1/matches.py` |
| 3.3 前端赛程重构 | 「今日→明日→全部」分类，筛选 UI，状态色彩（灰色/红色/绿色） | `frontend/src/views/Schedule.vue` |
| 3.4 赛程详情页 | 展示双方国旗/队名/时间/地点/阶段/赛果/事件 | `frontend/src/views/MatchDetail.vue`（新） |
| 3.5 小组积分页 | 12 组积分榜 Tab 切换，出线标识 | `frontend/src/components/match/GroupStandings.vue`（新） |

**验证**：赛程页面筛选正常，已结束赛事灰化，积分榜 12 组可切

### 阶段二：核心功能完善（D4-D7）

#### D4：提醒服务完善 + 前端 UI 优化

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 4.1 球队全赛程订阅 | 一键订阅球队所有比赛提醒 | `backend/app/api/v1/matches.py` |
| 4.2 自定义提醒时间 | 支持 30 分钟 / 1 小时 / 2 小时 | `frontend/src/components/match/ReminderSetting.vue`（新） |
| 4.3 主题色切换 | TailwindCSS 主色调改为足球绿(#16a34a)，辅助红/蓝 | `frontend/tailwind.config.js` |
| 4.4 全局图标体系 | 引入 lucide-vue-next，统一线性图标风格 | `frontend/package.json` + 各组件 |
| 4.5 底部 Tab 重构 | 首页/赛程/数据/社交/我的（5 Tab） | `frontend/src/components/common/TabBar.vue` |

**验证**：订阅球队后自动设置所有赛事提醒，UI 绿色主题，5 Tab 导航

#### D5：球队/球员数据页（数据 Tab）

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 5.1 数据首页 | 球队列表（按大洲/小组筛选）+ 搜索 | `frontend/src/views/Data.vue`（新） |
| 5.2 球队详情升级 | 基础信息 + 核心球员标星 + 伤病红色标注 + 历史战绩 | `frontend/src/views/TeamDetail.vue` |
| 5.3 球员详情升级 | 世界杯数据（出场/进球/助攻/射门/传球/红黄牌） | `frontend/src/views/PlayerDetail.vue` |
| 5.4 射手榜/助攻榜 | 独立排行页面，支持筛选 | `backend/app/api/v1/rankings.py`（新）+ `frontend/src/views/Rankings.vue`（新） |
| 5.5 球队数据模型扩展 | 战力字段（进攻/防守/控球率/射门/进球效率） | `backend/app/models/team.py` |

**验证**：数据 Tab 可浏览 48 队，球队详情有完整数据，射手榜排序正确

#### D6：AI 赛果预测（P1 核心）

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 6.1 预测 API | 基于球队数据生成胜率（主胜/客胜/平局百分比） | `backend/app/services/ai_analysis.py` |
| 6.2 比分区间预测 | 预测可能比分（如 1-0、2-1）及概率 | `backend/app/services/ai_analysis.py` |
| 6.3 预测展示页 | 环形图展示胜率，比分区间按概率排序，免责声明 | `frontend/src/components/match/AIPrediction.vue`（新） |
| 6.4 预测缓存 | 赛前 24h 生成，Redis 缓存，避免重复调用 AI | `backend/app/services/ai_analysis.py` |
| 6.5 免责声明组件 | "预测仅供参考，不构成任何投注建议" 全局复用 | `frontend/src/components/common/Disclaimer.vue`（新） |

**验证**：赛事详情页展示 AI 预测，有免责声明，缓存命中率 > 80%

#### D7：社交模块（社交 Tab）

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 7.1 社交首页 | 合并圈子 + 竞猜入口 | `frontend/src/views/Social.vue`（新） |
| 7.2 球迷圈升级 | 圈顶部展示国旗/队名/粉丝数，热门排序 | `frontend/src/views/Community.vue` |
| 7.3 竞猜扩展 | 基础胜负竞猜保留，UI 整合到社交 Tab | `frontend/src/views/Prediction.vue` |
| 7.4 举报入口 | 帖子/评论举报按钮 | `frontend/src/components/community/ReportButton.vue`（新） |
| 7.5 内容过滤前端 | 发帖/评论前端预检测 + 后端拦截 | `frontend/src/utils/contentFilter.ts`（新） |

**验证**：社交 Tab 统一入口，举报可用，违禁词发帖被拦截

### 阶段三：增值功能 + 完善（D8-D12）

#### D8：积分任务系统

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 8.1 每日签到 | 签到领积分（每日 10 分），连续签到加成 | `backend/app/api/v1/tasks.py`（新） |
| 8.2 任务系统 | 每日任务：查看赛程(5分)/分享内容(10分)/加入圈子(5分)/参与竞猜(10分) | `backend/app/services/task_service.py`（新） |
| 8.3 积分流水 | 收支明细 API + 前端展示 | `backend/app/api/v1/points.py`（新） |
| 8.4 前端任务中心 | 任务列表页 + 签到动效 | `frontend/src/views/TaskCenter.vue`（新） |

**验证**：签到领积分，任务完成自动发放，积分明细可查

#### D9：个人中心升级（P1）

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 9.1 个人信息编辑 | 修改头像/昵称，绑定手机号 | `backend/app/api/v1/auth.py` |
| 9.2 记录中心 | 积分记录/竞猜记录/发布记录/壁纸记录 Tab 切换 | `frontend/src/views/Profile.vue` |
| 9.3 基础会员 UI | 会员开通页面（去广告 + 无水印壁纸），暂不接支付 | `frontend/src/views/Membership.vue`（新） |
| 9.4 会员权限控制 | 后端中间件：区分普通/会员用户访问权限 | `backend/app/utils/membership.py`（新） |
| 9.5 设置页面 | 通知开关、隐私政策、用户协议、关于、注销入口 | `frontend/src/views/Settings.vue`（新） |

**验证**：个人信息可编辑，记录可查，会员页面展示权益对比

#### D10：壁纸/应援物料（P2 核心）

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 10.1 Celery 壁纸任务 | 打通 DALL-E 生成 → 存储 → 状态回调 | `backend/app/tasks/generate_wallpaper.py` |
| 10.2 固定模板壁纸 | 4 种风格预生成模板（无需 AI，快速出图） | `frontend/src/views/Wallpaper.vue` |
| 10.3 头像框生成 | 球队主题头像框（Canvas 合成） | `frontend/src/components/wallpaper/AvatarFrame.vue`（新） |
| 10.4 积分兑换 | 壁纸下载消耗积分（普通 50 分，高清 100 分，会员免费） | `backend/app/api/v1/wallpapers.py` |
| 10.5 分享功能 | 生成分享海报（Canvas），支持保存到相册 | `frontend/src/utils/shareCanvas.ts`（新） |

**验证**：AI 壁纸异步生成成功，模板壁纸即时可用，积分兑换逻辑正确

#### D11：前端 UI/UX 打磨

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 11.1 加载状态 | 全局骨架屏 + Loading 动画 + 加载失败重试 | 各页面 |
| 11.2 空状态 | 统一空状态组件（无数据/无网络/无权限） | `frontend/src/components/common/EmptyState.vue` |
| 11.3 Toast 提示 | 操作反馈统一 Toast（成功/失败/警告），≤3 秒 | `frontend/src/composables/useToast.ts`（新） |
| 11.4 路由守卫 | 登录跳转、会员页面拦截、返回逻辑优化 | `frontend/src/router/index.ts` |
| 11.5 响应式适配 | 不同手机尺寸适配 | 各组件 |

**验证**：全流程无白屏，操作有反馈，返回逻辑合理

#### D12：uni-app 小程序同步

| 任务 | 具体内容 | 涉及文件 |
|------|---------|---------|
| 12.1 页面同步 | 5 Tab 页面对齐 Web 端 | `miniprogram/src/pages/` |
| 12.2 微信登录 | 打通微信 OAuth → 后端 wx-login | `miniprogram/src/utils/auth.ts` |
| 12.3 微信支付准备 | 会员支付接口占位（V1.1 接入） | `backend/app/api/v1/payment.py`（新） |
| 12.4 模板消息 | 赛事提醒微信模板消息 | `backend/app/services/wechat.py`（新） |
| 12.5 分享卡片 | 小程序分享到微信好友/朋友圈 | `miniprogram/src/utils/share.ts` |

**验证**：小程序开发者工具预览正常，微信登录流程通，分享可用

### 阶段四：测试与上线（D13-D15）

#### D13：全端联调 + 自动化测试

| 任务 | 具体内容 |
|------|---------|
| 13.1 后端单元测试 | 核心 API 测试覆盖率 ≥ 70% |
| 13.2 合规测试 | 违禁词过滤、免责声明展示、隐私政策可访问 |
| 13.3 Web 端联调 | 全流程走通：注册→赛程→数据→社交→竞猜→壁纸→个人中心 |
| 13.4 小程序联调 | 微信登录→核心功能→分享 |
| 13.5 性能基线 | API 响应 ≤ 500ms，页面加载 ≤ 1s |

#### D14：Bug 修复 + UI 收尾

| 任务 | 具体内容 |
|------|---------|
| 14.1 Bug 修复 | D13 发现的问题全部修复 |
| 14.2 UI 对齐 PRD | 色彩/图标/字体/间距终审 |
| 14.3 边界情况 | 无网络、空数据、大量数据、并发请求 |
| 14.4 安全审查 | SQL 注入、XSS、CSRF、JWT 安全、密码加密 |
| 14.5 文档更新 | CLAUDE.md + README + API 文档 |

#### D15：部署上线

| 任务 | 具体内容 |
|------|---------|
| 15.1 生产环境部署 | 阿里云 ECS / 腾讯云，docker-compose.prod.yml |
| 15.2 域名 + SSL | 绑定域名 + Let's Encrypt SSL |
| 15.3 Nginx 配置 | 反向代理 + 静态文件 + WebSocket |
| 15.4 小程序提审 | 微信公众平台提交审核 |
| 15.5 监控告警 | 健康检查 + 错误日志 + 性能监控 |

---

## 五、V1.1 爆发期迭代计划（10 天）

> 6 月 1 日前完成，世界杯开赛前上线

| 天 | 任务 | 产出 |
|----|------|------|
| V1.1-D1 | 赛中实时弹幕/聊天室 WebSocket | 赛中互动可用 |
| V1.1-D2 | 弹幕 UI + 关键词过滤 + 屏蔽用户 | 弹幕体验完善 |
| V1.1-D3 | AI 内容生成（战报/梗图/短视频脚本） | 内容创作工具 |
| V1.1-D4 | 高光片段文案 + 热门话题库 | 创作引导完善 |
| V1.1-D5 | 会员支付接入（微信支付 + 支付宝） | 变现通道打通 |
| V1.1-D6 | 会员权益完善（去广告/深度预测/无水印） | 会员体验完整 |
| V1.1-D7 | 世界杯足迹 + 勋章系统 | 留存机制上线 |
| V1.1-D8 | 数据可视化（ECharts 折线图/柱状图/环形图） | 数据页体验升级 |
| V1.1-D9 | 竞猜扩展（比分区间/进球数/关键球员） | 竞猜玩法丰富 |
| V1.1-D10 | 全端联调 + Bug 修复 + 上线 | V1.1 正式发布 |

---

## 六、V1.2 长尾期迭代计划（10 天）

> 7 月 20 日前完成

| 天 | 任务 | 产出 |
|----|------|------|
| V1.2-D1~D2 | 出线形势 AI 推演（概率/条件/对阵图） | 核心差异化功能 |
| V1.2-D3~D4 | 观赛套餐推荐 + 电商 CPS 接入 | 商业化扩展 |
| V1.2-D5~D6 | 自定义应援素材编辑器（拖拽/文字/背景） | 创作深度增强 |
| V1.2-D7 | 赛事数据导出（图片格式） | 内容创作工具 |
| V1.2-D8 | 冠军纪念页 + 年度总结（世界杯回忆） | 长尾留存 |
| V1.2-D9 | 性能优化（缓存/懒加载/图片压缩） | 体验提升 |
| V1.2-D10 | 全端联调 + Bug 修复 + 上线 | V1.2 正式发布 |

---

## 七、项目结构（更新后）

```
worldcup-scout-pro/
├── CLAUDE.md
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── notes/
│   ├── 2026美加墨世界杯·球探Pro PRD产品需求文档.md
│   └── plan/
│       ├── mvp-plan.md              # 初始计划（已过时）
│       └── implementation-plan.md   # 本文档（当前计划）
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── alembic/
│   │   └── versions/
│   │       ├── 001_initial.py
│   │       ├── 002_expand_48_teams.py           # 新：48队扩展
│   │       └── 003_compliance_tasks_member.py   # 新：合规+任务+会员
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── user.py          # 改：新增会员/签到/勋章字段
│   │   │   ├── team.py
│   │   │   ├── player.py
│   │   │   ├── match.py
│   │   │   ├── post.py
│   │   │   ├── prediction.py
│   │   │   ├── wallpaper.py
│   │   │   ├── point_record.py  # 新：积分流水
│   │   │   ├── user_task.py     # 新：用户任务
│   │   │   ├── report.py        # 新：举报
│   │   │   └── banned_word.py   # 新：违禁词
│   │   ├── schemas/
│   │   │   ├── ... (现有)
│   │   │   ├── report.py        # 新
│   │   │   ├── task.py          # 新
│   │   │   └── point.py         # 新
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py      # 改：注册同意协议
│   │   │   │   ├── matches.py   # 改：48队/筛选/出线
│   │   │   │   ├── teams.py
│   │   │   │   ├── players.py
│   │   │   │   ├── community.py # 改：内容过滤
│   │   │   │   ├── predictions.py
│   │   │   │   ├── wallpapers.py # 改：积分兑换
│   │   │   │   ├── reports.py   # 新：举报
│   │   │   │   ├── legal.py     # 新：法律文本
│   │   │   │   ├── tasks.py     # 新：任务签到
│   │   │   │   ├── points.py    # 新：积分流水
│   │   │   │   └── rankings.py  # 新：排行榜
│   │   │   └── websocket.py
│   │   ├── services/
│   │   │   ├── match_service.py
│   │   │   ├── data_sync.py
│   │   │   ├── reminder.py
│   │   │   ├── prediction.py
│   │   │   ├── wallpaper.py
│   │   │   ├── ai_analysis.py  # 改：赛果预测/赛前分析
│   │   │   ├── task_service.py  # 新：任务系统
│   │   │   └── wechat.py        # 新：微信服务(V1.1)
│   │   ├── tasks/
│   │   │   ├── sync_matches.py
│   │   │   ├── send_reminders.py
│   │   │   └── generate_wallpaper.py
│   │   └── utils/
│   │       ├── auth.py
│   │       ├── football_api.py
│   │       ├── content_filter.py # 新：内容过滤
│   │       └── membership.py     # 新：会员中间件
│   └── tests/
│       ├── test_health.py
│       ├── test_auth.py         # 新
│       ├── test_matches.py      # 新
│       ├── test_compliance.py   # 新
│       └── test_predictions.py  # 新
├── frontend/
│   ├── Dockerfile
│   ├── package.json             # 改：+echarts +lucide-vue-next
│   ├── vite.config.ts
│   ├── tailwind.config.js       # 改：主题色改绿色
│   ├── src/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── router/index.ts     # 改：5 Tab 路由
│   │   ├── stores/
│   │   │   ├── user.ts
│   │   │   ├── matches.ts
│   │   │   └── teams.ts
│   │   ├── api/
│   │   │   ├── ... (现有)
│   │   │   ├── reports.ts       # 新
│   │   │   ├── tasks.ts         # 新
│   │   │   ├── points.ts        # 新
│   │   │   └── rankings.ts      # 新
│   │   ├── composables/
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useCountdown.ts
│   │   │   └── useToast.ts      # 新
│   │   ├── utils/
│   │   │   ├── contentFilter.ts # 新
│   │   │   └── shareCanvas.ts   # 新
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── TabBar.vue       # 改：5 Tab
│   │   │   │   ├── NavBar.vue
│   │   │   │   ├── LoadingSpinner.vue
│   │   │   │   ├── EmptyState.vue
│   │   │   │   └── Disclaimer.vue   # 新：免责声明
│   │   │   ├── match/
│   │   │   │   ├── MatchCard.vue     # 改：状态色彩
│   │   │   │   ├── StandingsTable.vue # 改：12组
│   │   │   │   ├── LiveScore.vue
│   │   │   │   ├── GroupStandings.vue # 新：小组积分
│   │   │   │   ├── ReminderSetting.vue # 新
│   │   │   │   └── AIPrediction.vue  # 新
│   │   │   ├── team/
│   │   │   ├── community/
│   │   │   │   ├── PostCard.vue
│   │   │   │   ├── PostForm.vue     # 改：内容过滤
│   │   │   │   ├── CommentItem.vue
│   │   │   │   └── ReportButton.vue # 新
│   │   │   ├── prediction/
│   │   │   └── wallpaper/
│   │   │       ├── WallpaperCard.vue
│   │   │       ├── StyleSelector.vue
│   │   │       └── AvatarFrame.vue  # 新
│   │   ├── views/
│   │   │   ├── Home.vue             # 改：48队
│   │   │   ├── Schedule.vue         # 改：筛选/状态色
│   │   │   ├── MatchDetail.vue      # 新
│   │   │   ├── Data.vue             # 新：数据 Tab
│   │   │   ├── TeamDetail.vue       # 改：战力数据
│   │   │   ├── PlayerDetail.vue     # 改：世界杯数据
│   │   │   ├── Rankings.vue         # 新：排行榜
│   │   │   ├── Social.vue           # 新：社交 Tab
│   │   │   ├── Community.vue        # 改：热门排序
│   │   │   ├── Prediction.vue       # 改：整合社交
│   │   │   ├── Wallpaper.vue
│   │   │   ├── Profile.vue          # 改：记录中心
│   │   │   ├── TaskCenter.vue       # 新
│   │   │   ├── Membership.vue       # 新
│   │   │   ├── Settings.vue         # 新
│   │   │   └── Login.vue            # 改：协议同意
│   │   └── assets/
│   └── public/
├── miniprogram/
│   └── ...（D12 同步）
└── scripts/
    ├── seed_data.py                 # 改：48队数据
    ├── seed_banned_words.py         # 新
    └── init_db.sh
```

---

## 八、关键风险与应对

| 风险 | 影响 | 应对方案 |
|------|------|---------|
| 48 队数据不完整 | 2026 世界杯尚未确定全部参赛队 | 使用预测名单（各大洲预选赛排名靠前的队伍），正式确定后快速替换 |
| AI API 调用限额 | DALL-E / Claude API 费用 | 预生成模板壁纸减少 API 调用；预测结果 Redis 缓存 24h；设每日生成上限 |
| 外部数据接口不稳定 | 赛程/比分数据延迟 | 对接 2+ 数据源备用切换；本地缓存历史数据；异常提示用户 |
| 支付接入审核 | 微信支付商户号审核周期长 | V1.0 仅做会员 UI 展示，V1.1 接入支付；提前申请商户号 |
| 小程序审核 | 含竞猜功能可能被拒 | 竞猜页面明确标注"虚拟积分，不可兑换现金"；免责声明前置 |

---

## 九、验收标准

### V1.0 MVP 验收清单

- [ ] `docker compose up` 一键启动全部服务
- [ ] 48 支球队、12 组、104 场比赛数据完整
- [ ] 赛程列表可按小组/球队/阶段/日期筛选
- [ ] 已结束赛事灰化，进行中赛事红色标注
- [ ] 赛事提醒设置可用（单场 + 球队订阅）
- [ ] 球队/球员数据详情页完整
- [ ] 射手榜/助攻榜排名正确
- [ ] AI 赛果预测展示（胜率 + 比分区间 + 免责声明）
- [ ] 球迷圈发帖/评论/点赞 + 违禁词过滤
- [ ] 竞猜投注/结算/排行榜可用
- [ ] AI 壁纸生成 + 固定模板壁纸可用
- [ ] 积分签到/任务系统可用
- [ ] 举报功能可用
- [ ] 隐私政策/用户协议/免责声明可访问
- [ ] 注册流程需同意协议
- [ ] 底部 5 Tab 导航：首页/赛程/数据/社交/我的
- [ ] 主题色：足球绿 + 统一线性图标
- [ ] uni-app 小程序核心功能可用
- [ ] 后端测试覆盖率 ≥ 70%
- [ ] API 响应 ≤ 500ms，页面加载 ≤ 1s
