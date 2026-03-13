# MEMORY.md - 世界杯球探 Pro 项目记忆

## 项目信息

**项目名称：** 世界杯全能助手・球探 Pro  
**GitHub：** https://github.com/wentChu/worldcup-scout-pro  
**本地路径：** `/root/projects/worldcup-scout-pro`  
**克隆时间：** 2026-03-13

## 技术栈

### 后端
- **语言：** Python 3.12
- **框架：** FastAPI
- **ORM：** SQLAlchemy 2.0 (异步)
- **数据库：** PostgreSQL 16
- **缓存：** Redis 7
- **任务队列：** Celery
- **迁移工具：** Alembic
- **依赖管理：** uv

### 前端 Web
- **框架：** Vue 3 (Composition API + `<script setup>`)
- **构建工具：** Vite 6
- **状态管理：** Pinia
- **路由：** Vue Router 4
- **样式：** TailwindCSS
- **HTTP 客户端：** Axios
- **工具库：** @vueuse/core

### 小程序
- **框架：** uni-app (Vue 3)

### 部署
- **容器化：** Docker + Docker Compose
- **实时通信：** WebSocket

### AI 集成
- **壁纸生成：** Stable Diffusion / DALL-E
- **赛事分析：** Claude API

## 项目结构

```
worldcup-scout-pro/
├── backend/              # Python FastAPI 后端
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── models/       # SQLAlchemy 模型
│   │   ├── schemas/      # Pydantic 模式
│   │   ├── services/     # 业务逻辑
│   │   ├── tasks/        # Celery 任务
│   │   └── utils/        # 工具函数
│   ├── alembic/          # 数据库迁移
│   ├── tests/            # 测试
│   └── pyproject.toml    # Python 依赖
│
├── frontend/             # Vue 3 前端
│   ├── src/
│   │   ├── api/          # API 封装
│   │   ├── components/   # 组件
│   │   ├── composables/  # 组合式函数
│   │   ├── router/       # 路由
│   │   ├── stores/       # Pinia 状态
│   │   ├── utils/        # 工具函数
│   │   └── views/        # 页面
│   └── package.json
│
├── miniprogram/          # uni-app 小程序
│   └── src/
│
├── notes/                # 项目笔记
├── scripts/              # 脚本
├── docker-compose.yml    # 开发环境
└── docker-compose.prod.yml  # 生产环境
```

## 核心功能模块

1. **赛程 + 提醒**
   - 完整赛程表
   - 实时比分 (WebSocket)
   - 赛前提醒

2. **基础数据**
   - 32 支球队资料
   - 球员数据库
   - 积分榜/射手榜

3. **球队圈子**
   - 专属讨论圈
   - 发帖评论点赞
   - 热门排序

4. **竞猜积分**
   - 虚拟积分竞猜
   - 排行榜
   - 连胜奖励

5. **壁纸生成**
   - AI 生成球队/球员壁纸
   - 多种风格模板

## 开发规范

### 代码风格
- **Python：** ruff 格式化 + 类型注解
- **TypeScript：** ESLint + Prettier
- **提交信息：** `feat/fix/docs/refactor: 描述`

### 语言规则
- **代码：** 英文（变量名、函数名、类型名）
- **注释：** 中文（业务逻辑、复杂算法）
- **文档：** 中文（分析报告、设计文档）

### 后端规范
- API 路由前缀：`/api/v1/`
- 所有模型继承 `Base`
- 使用 SQLAlchemy 2.0 异步风格
- Pydantic v2 做请求/响应校验
- JWT 认证，token 有效期 7 天
- 环境变量通过 `pydantic-settings` 管理

### 前端规范
- 组合式 API + `<script setup>`
- Pinia 状态管理
- API 请求统一封装在 `src/api/`
- TailwindCSS 样式
- 路由懒加载

### 数据库规范
- 迁移使用 Alembic
- JSONB 字段存储灵活数据
- 所有表包含 `created_at` 时间戳

## 启动命令

### 开发环境
```bash
# 启动所有服务（后端 + 前端 + 数据库 + Redis）
docker-compose up

# 后端 API 文档
http://localhost:8000/docs

# 前端开发服务器
http://localhost:5173
```

### 测试
```bash
cd backend && pytest
```

## 环境变量

参考 `.env.example` 配置：
- 数据库连接
- Redis 连接
- JWT 密钥
- AI API 密钥（Stable Diffusion / Claude）

## 待办事项

_待添加_

## 已知问题

_待添加_

## 重要决策

_待记录_

---

**最后更新：** 2026-03-13  
**当前状态：** 项目已克隆，准备继续开发
