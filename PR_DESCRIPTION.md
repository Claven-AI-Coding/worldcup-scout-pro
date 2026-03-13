# 🔧 配置代码质量工具链和 CI/CD

## 📝 变更说明

本 PR 为项目添加了完整的代码质量工具链和自动化 CI/CD 流程，确保代码质量和开发效率。

## ✨ 新增功能

### 1. 代码质量工具
- **ESLint**: Vue 3 + TypeScript 代码规范检查
- **Prettier**: 统一代码格式化（支持 Tailwind CSS）
- **Vitest**: 测试框架，覆盖率要求 ≥85%
- **commitlint**: 提交信息规范（Conventional Commits）
- **lint-staged**: 提交前自动检查和格式化

### 2. CI/CD 工作流
- **CI 流程** (`.github/workflows/ci.yml`)
  - 前端：Lint、格式检查、类型检查、测试、覆盖率
  - 后端：Ruff 检查、格式检查、测试、覆盖率
  - 自动上传覆盖率报告到 Codecov

- **部署流程** (`.github/workflows/deploy.yml`)
  - 合并到 `main` 自动部署
  - 构建前端
  - SSH 部署到服务器
  - 健康检查

### 3. 文档
- **SETUP.md**: 详细的项目配置和开发指南
- **MEMORY.md**: 项目记忆和技术决策记录
- **memory/2026-03-13.md**: 工作日志

## 📦 新增依赖

### 前端 (frontend/package.json)
```json
{
  "devDependencies": {
    "eslint": "^9.0.0",
    "eslint-plugin-vue": "^9.0.0",
    "@typescript-eslint/eslint-plugin": "^8.0.0",
    "@typescript-eslint/parser": "^8.0.0",
    "prettier": "^3.0.0",
    "prettier-plugin-tailwindcss": "^0.6.0",
    "husky": "^9.0.0",
    "lint-staged": "^15.0.0",
    "@commitlint/cli": "^19.0.0",
    "@commitlint/config-conventional": "^19.0.0",
    "vitest": "^2.0.0",
    "@vitest/ui": "^2.0.0",
    "@vue/test-utils": "^2.4.0",
    "happy-dom": "^15.0.0"
  }
}
```

## 🎯 提交规范

从现在开始，所有提交必须遵循 Conventional Commits 规范：

```
<type>: <subject>

[optional body]
```

**Type 类型：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链

**示例：**
```bash
feat: 添加用户登录功能
fix: 修复导航栏在移动端的显示问题
docs: 更新 API 文档
```

## 🧪 测试覆盖率

- **要求**: ≥85%
- **配置**: `frontend/vitest.config.ts`
- **运行**: `npm run test:coverage`

## 🔄 开发工作流

1. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **开发和提交**
   ```bash
   git add .
   git commit -m "feat: 添加新功能"
   # 自动触发 lint-staged 检查
   ```

3. **推送和创建 PR**
   ```bash
   git push origin feature/your-feature
   ```

4. **CI 自动检查**
   - ✅ Lint 通过
   - ✅ 测试通过
   - ✅ 覆盖率 ≥85%
   - ✅ 构建成功

5. **合并后自动部署**

## 📋 合并后需要做的事

1. **安装依赖**
   ```bash
   cd frontend
   npm install
   ```

2. **初始化 Husky**
   ```bash
   npm run prepare
   ```

3. **测试配置**
   ```bash
   npm run lint
   npm run format:check
   npm run test
   ```

## 🔗 相关文档

- [SETUP.md](./SETUP.md) - 详细配置指南
- [MEMORY.md](./MEMORY.md) - 项目记忆
- [CLAUDE.md](./CLAUDE.md) - 项目概述

## ✅ Checklist

- [x] 添加 ESLint 配置
- [x] 添加 Prettier 配置
- [x] 添加 Vitest 配置
- [x] 添加 commitlint 配置
- [x] 添加 lint-staged 配置
- [x] 添加 GitHub Actions CI
- [x] 添加 GitHub Actions 部署流程
- [x] 编写配置文档
- [x] 更新 package.json

## 🎉 影响

- ✅ 提升代码质量
- ✅ 统一代码风格
- ✅ 自动化测试
- ✅ 自动化部署
- ✅ 规范提交信息
- ✅ 提高开发效率

---

**合并后，所有开发者需要重新安装依赖并初始化 Husky。**
