# 世界杯全能助手・球探 Pro

## 项目概述

世界杯全能助手产品，核心定位：赛事工具 + 社区互动 + AI 创意生成。

## 技术栈

- **后端**: Python 3.12 + FastAPI + SQLAlchemy + Alembic
- **前端 Web**: Vue 3 + Vite + TailwindCSS + Pinia
- **小程序**: uni-app (Vue 3)
- **数据库**: PostgreSQL 16 (JSONB 存储灵活数据)
- **缓存**: Redis 7 (比分缓存、排行榜、消息队列)
- **实时推送**: WebSocket (FastAPI)
- **AI 壁纸**: Stable Diffusion API / DALL-E
- **AI 分析**: Claude API
- **任务队列**: Celery + Redis
- **部署**: Docker Compose

## 开发规范

### 后端
- 使用 `uv` 管理 Python 依赖
- API 路由统一前缀 `/api/v1/`
- 所有模型继承 `Base`，使用 SQLAlchemy 2.0 风格
- Pydantic v2 做请求/响应校验
- 异步优先：数据库操作使用 `async`
- JWT 认证，token 有效期 7 天
- 环境变量通过 `pydantic-settings` 管理

### 前端
- 组合式 API (Composition API) + `<script setup>` 语法
- Pinia 状态管理
- API 请求统一封装在 `src/api/` 目录
- TailwindCSS 样式，不使用 CSS 框架
- 路由懒加载

### 语言规则

| 类型 | 语言 | 说明                       |
|------|------|----------------------------|
| 代码 | 英文 | 变量名、函数名、类型名     |
| 注释 | 中文 | 业务逻辑注释、复杂算法解释 |
| 文档 | 中文 | 分析报告、设计文档、README |
| 回答 | 中文 | 所有对话、解释、分析       |

### 代码风格
- Python: ruff 格式化 + 类型注解
- TypeScript: ESLint + Prettier
- 提交信息格式: `feat/fix/docs/refactor: 描述`

### 数据库
- 迁移使用 Alembic，不手动修改数据库
- JSONB 字段用于存储灵活结构数据（球员统计、球队数据等）
- 所有表包含 `created_at` 时间戳

## 五大核心模块

1. **赛程 + 提醒**: 完整赛程表、实时比分 WebSocket、赛前提醒
2. **基础数据**: 32 支球队资料、球员数据库、积分榜/射手榜
3. **球队圈子**: 专属讨论圈、发帖评论点赞、热门排序
4. **竞猜积分**: 虚拟积分竞猜、排行榜、连胜奖励
5. **壁纸生成**: AI 生成球队/球员壁纸、多种风格模板

## 启动方式

```bash
# 开发环境
docker-compose up

# 后端 API 文档
http://localhost:8000/docs

# 前端开发
http://localhost:5173

# 运行测试
cd backend && pytest
```

## 环境变量

参考 `.env.example` 配置所有必要的环境变量。
