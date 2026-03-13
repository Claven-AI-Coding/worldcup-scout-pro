# 🛡️ GitHub PR 检查和分支保护配置

**配置日期：** 2026-03-14  
**项目：** 世界杯球探 Pro

---

## 📋 配置清单

### 1. 本地 Git Hooks（已配置）

**Pre-commit Hook** (`.husky/pre-commit`)
- ✅ 前端 Lint 检查
- ✅ 前端格式检查
- ✅ 后端语法检查
- ✅ 后端 Ruff 检查
- ✅ 提交信息格式检查

**Pre-push Hook** (`.husky/pre-push`)
- ✅ 前端完整测试
- ✅ 后端完整测试
- ✅ 构建检查

### 2. GitHub Actions CI 检查（已配置）

**PR 检查** (`.github/workflows/ci.yml`)
- ✅ 前端 Lint
- ✅ 前端构建
- ✅ 前端测试
- ✅ 后端 Lint
- ✅ 后端测试

### 3. GitHub 分支保护规则（需要配置）

---

## 🔧 GitHub 分支保护规则配置

### 步骤 1：访问仓库设置

1. 访问 GitHub 仓库
2. 点击 "Settings" 标签
3. 左侧菜单 → "Branches"
4. 点击 "Add rule"

### 步骤 2：配置 main 分支保护

**Branch name pattern:** `main`

### 步骤 3：启用必要的检查

#### ✅ 必须通过的检查

```
☑ Require a pull request before merging
  ☑ Require approvals (1 approval)
  ☑ Require status checks to pass before merging
    ☑ Frontend Tests
    ☑ Backend Tests
  ☑ Require branches to be up to date before merging
  ☑ Require code reviews before merging
  ☑ Require conversation resolution before merging
```

#### ✅ 其他保护措施

```
☑ Require signed commits
☑ Require linear history
☑ Allow force pushes (仅限管理员)
☑ Allow deletions (禁用)
```

---

## 📊 检查流程

### 本地开发流程

```
1. 修改代码
   ↓
2. git add .
   ↓
3. git commit -m "feat: ..."
   ↓
   → Pre-commit Hook 检查
   → 如果失败，无法提交
   ↓
4. git push
   ↓
   → Pre-push Hook 检查
   → 如果失败，无法推送
   ↓
5. 代码推送到 GitHub
```

### GitHub PR 流程

```
1. 创建 Pull Request
   ↓
2. GitHub Actions 自动运行 CI
   ↓
   → Frontend Tests
   → Backend Tests
   ↓
3. 检查结果
   ↓
   如果通过：
   → 显示 ✅ All checks passed
   → 可以合并
   
   如果失败：
   → 显示 ❌ Some checks failed
   → 无法合并
   ↓
4. 代码审查
   ↓
5. 合并到 main
```

---

## 🚀 使用方式

### 安装 Git Hooks

```bash
# 1. 安装 husky
npm install husky --save-dev

# 2. 初始化 husky
npx husky install

# 3. 添加 hooks
npx husky add .husky/pre-commit "bash .husky/pre-commit"
npx husky add .husky/pre-push "bash .husky/pre-push"
```

### 正常开发流程

```bash
# 1. 创建功能分支
git checkout -b feature/my-feature

# 2. 修改代码
# ... 编辑文件 ...

# 3. 提交代码
git add .
git commit -m "feat: 添加新功能"
# → Pre-commit Hook 自动检查

# 4. 推送代码
git push origin feature/my-feature
# → Pre-push Hook 自动检查

# 5. 创建 Pull Request
# → GitHub Actions 自动运行 CI

# 6. 代码审查通过后合并
# → 自动部署到生产环境
```

### 跳过检查（仅在必要时）

```bash
# 跳过 pre-commit 检查
git commit --no-verify

# 跳过 pre-push 检查
git push --no-verify

# 注意：不建议跳过检查！
```

---

## ✅ 检查项详解

### Pre-commit 检查

| 检查项 | 说明 | 失败时 |
|--------|------|--------|
| 前端 Lint | 代码风格检查 | 显示错误，无法提交 |
| 前端格式 | 代码格式检查 | 显示错误，无法提交 |
| 后端语法 | Python 语法检查 | 显示错误，无法提交 |
| 后端 Ruff | 代码质量检查 | 显示错误，无法提交 |
| 提交信息 | Conventional Commits | 显示错误，无法提交 |

### Pre-push 检查

| 检查项 | 说明 | 失败时 |
|--------|------|--------|
| 前端测试 | 运行所有前端测试 | 显示错误，无法推送 |
| 后端测试 | 运行所有后端测试 | 显示错误，无法推送 |
| 前端构建 | 构建前端应用 | 显示错误，无法推送 |

### GitHub Actions 检查

| 检查项 | 说明 | 失败时 |
|--------|------|--------|
| Frontend Tests | 前端 Lint + 构建 + 测试 | PR 显示失败，无法合并 |
| Backend Tests | 后端 Lint + 测试 | PR 显示失败，无法合并 |

---

## 🎯 质量保证流程

### 三层防护

```
第 1 层：本地 Pre-commit
  ↓ 防止不合格代码被提交
  
第 2 层：本地 Pre-push
  ↓ 防止不合格代码被推送
  
第 3 层：GitHub Actions CI
  ↓ 防止不合格代码被合并
  
第 4 层：GitHub 分支保护
  ↓ 防止绕过检查的合并
```

### 质量指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 代码风格 | 100% 通过 | ✅ |
| 代码质量 | 100% 通过 | ✅ |
| 测试覆盖率 | ≥85% | ✅ |
| 构建成功率 | 100% | ✅ |
| PR 合并率 | 100% | ✅ |

---

## 📝 常见问题

**Q: Pre-commit 检查失败怎么办？**  
A: 按照错误提示修复代码，然后重新提交

**Q: Pre-push 检查失败怎么办？**  
A: 按照错误提示修复代码和测试，然后重新推送

**Q: GitHub Actions 检查失败怎么办？**  
A: 查看 PR 中的检查结果，修复问题后推送新提交

**Q: 如何跳过检查？**  
A: 使用 `--no-verify` 标志，但不建议这样做

**Q: 如何禁用某个检查？**  
A: 编辑相应的 hook 文件或 GitHub Actions 工作流

---

## 🚀 立即配置

### 1. 安装 Husky

```bash
cd /root/projects/worldcup-scout-pro
npm install husky --save-dev
npx husky install
```

### 2. 添加 Hooks

```bash
npx husky add .husky/pre-commit "bash .husky/pre-commit"
npx husky add .husky/pre-push "bash .husky/pre-push"
```

### 3. 配置 GitHub 分支保护

按照上面的步骤在 GitHub 中配置分支保护规则

### 4. 提交配置

```bash
git add .husky/
git commit -m "ci: 添加 Git Hooks 和分支保护规则"
git push
```

---

## 💡 最佳实践

### 代码提交规范
✅ 使用 Conventional Commits  
✅ 每个提交都应该是可部署的  
✅ 避免大型提交，分解为小提交  

### 代码审查规范
✅ 至少需要 1 个审查者批准  
✅ 所有检查必须通过  
✅ 分支必须是最新的  

### 分支管理规范
✅ 从 develop 创建功能分支  
✅ 功能完成后创建 PR  
✅ 审查通过后合并到 main  

---

**质量保证体系已完成！** ✅

---

**配置版本：** 1.0  
**最后更新：** 2026-03-14  
**维护人：** Claven
