# 🚀 项目配置指南

## 📦 安装依赖

### 前端
```bash
cd frontend
npm install
```

### 后端
```bash
cd backend
pip install uv
uv pip install -r requirements.txt
```

## 🔧 Git Hooks 配置

项目使用 Husky 管理 Git hooks，确保代码质量。

### 初始化 Husky
```bash
cd frontend
npm run prepare
```

这会创建以下 hooks：
- **pre-commit**: 运行 lint-staged（自动格式化和检查）
- **commit-msg**: 检查提交信息格式

## ✅ 提交规范

使用 Conventional Commits 规范：

```
<type>: <subject>

[optional body]

[optional footer]
```

### Type 类型
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链

### 示例
```bash
git commit -m "feat: 添加用户登录功能"
git commit -m "fix: 修复导航栏在移动端的显示问题"
git commit -m "docs: 更新 API 文档"
```

## 🧪 测试

### 前端测试
```bash
cd frontend

# 运行测试
npm run test

# 测试覆盖率
npm run test:coverage

# 测试 UI
npm run test:ui
```

**覆盖率要求：≥85%**

### 后端测试
```bash
cd backend
pytest --cov=app --cov-report=term
```

## 🎨 代码格式化

### 前端
```bash
cd frontend

# 检查格式
npm run format:check

# 自动格式化
npm run format

# Lint 检查
npm run lint

# 自动修复
npm run lint:fix
```

### 后端
```bash
cd backend

# 检查
ruff check .

# 自动修复
ruff check --fix .

# 格式化
ruff format .
```

## 🔄 CI/CD

### GitHub Actions

项目配置了自动化 CI/CD：

**CI（持续集成）**
- 代码 Lint 检查
- 格式检查
- 类型检查
- 运行测试
- 检查覆盖率

**CD（持续部署）**
- 合并到 `main` 分支自动部署
- 构建 Docker 镜像
- 部署到生产服务器
- 健康检查

### 需要配置的 Secrets

在 GitHub Settings → Secrets 中添加：
- `SERVER_HOST`: 服务器地址
- `SERVER_USER`: SSH 用户名
- `SERVER_SSH_KEY`: SSH 私钥
- `APP_URL`: 应用 URL

## 📋 开发工作流

### 1. 创建功能分支
```bash
git checkout -b feature/your-feature-name
```

### 2. 开发和提交
```bash
# 开发代码...

# 提交（会自动触发 lint 和 format）
git add .
git commit -m "feat: 添加新功能"
```

### 3. 推送和创建 PR
```bash
git push origin feature/your-feature-name
```

然后在 GitHub 创建 Pull Request。

### 4. CI 检查
PR 会自动触发 CI 检查：
- ✅ Lint 通过
- ✅ 测试通过
- ✅ 覆盖率 ≥85%
- ✅ 构建成功

### 5. 合并和部署
合并到 `main` 后自动部署到生产环境。

## 🛠️ 常用命令

### 前端开发
```bash
cd frontend
npm run dev          # 启动开发服务器
npm run build        # 构建生产版本
npm run preview      # 预览生产构建
```

### 后端开发
```bash
cd backend
uvicorn app.main:app --reload  # 启动开发服务器
```

### Docker
```bash
# 开发环境
docker-compose up

# 生产环境
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 更多文档

- [CLAUDE.md](./CLAUDE.md) - 项目概述和技术栈
- [MEMORY.md](./MEMORY.md) - 项目记忆和决策记录
- [frontend/README.md](./frontend/README.md) - 前端详细文档
- [backend/README.md](./backend/README.md) - 后端详细文档

## 🆘 遇到问题？

1. 检查 Node.js 版本（需要 ≥20）
2. 检查 Python 版本（需要 ≥3.12）
3. 清理依赖重新安装：
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```
4. 查看 CI 日志了解具体错误

---

**Happy Coding! 🦅**
