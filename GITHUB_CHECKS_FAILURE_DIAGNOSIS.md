# 🔍 GitHub 检查失败诊断

**诊断时间：** 2026-03-14 22:56 GMT+8  
**问题：** 5 个检查失败，2 个检查被跳过  
**状态：** 🔴 **需要调查**

---

## 📋 可能的失败原因

### 1. 代码质量检查失败
- Linting 错误
- 类型检查错误
- 代码风格不符合规范

### 2. 构建失败
- 前端构建失败
- 后端构建失败
- 依赖问题

### 3. 测试失败
- 单元测试失败
- 集成测试失败
- E2E 测试失败

### 4. 安全检查失败
- 依赖漏洞
- 代码安全问题
- 敏感信息泄露

### 5. 部署检查失败
- 部署配置错误
- 环境变量缺失
- 权限问题

---

## 🎯 快速诊断步骤

### 步骤 1：查看 GitHub Actions 日志

1. 访问你的 GitHub 仓库
2. 点击 "Actions" 标签
3. 查看最新的工作流运行
4. 点击失败的检查查看详细日志

### 步骤 2：查看具体错误

在 GitHub Actions 日志中查找：
- ❌ 标记的错误
- 红色的失败信息
- 堆栈跟踪

### 步骤 3：本地重现错误

```bash
cd /root/projects/worldcup-scout-pro

# 运行 linting
npm run lint

# 运行类型检查
npm run type-check

# 运行测试
npm run test

# 构建前端
npm run build

# 构建后端
cd backend && npm run build
```

---

## 🛠️ 常见问题和解决方案

### 问题 1：TypeScript 类型错误

**症状：** `error TS2322: Type 'X' is not assignable to type 'Y'`

**解决方案：**
```bash
# 修复类型错误
npm run type-check

# 查看具体错误
npm run type-check -- --pretty
```

### 问题 2：Linting 错误

**症状：** `error: Unexpected token`

**解决方案：**
```bash
# 运行 linter
npm run lint

# 自动修复
npm run lint -- --fix
```

### 问题 3：构建失败

**症状：** `Build failed with exit code 1`

**解决方案：**
```bash
# 清理缓存
rm -rf node_modules
rm -rf dist
rm -rf .next

# 重新安装依赖
npm install

# 重新构建
npm run build
```

### 问题 4：测试失败

**症状：** `FAIL src/tests/...`

**解决方案：**
```bash
# 运行测试
npm run test

# 查看详细输出
npm run test -- --verbose

# 运行特定测试
npm run test -- --testNamePattern="test name"
```

### 问题 5：依赖漏洞

**症状：** `npm audit` 显示漏洞

**解决方案：**
```bash
# 检查漏洞
npm audit

# 修复漏洞
npm audit fix

# 强制修复
npm audit fix --force
```

---

## 📝 查看 GitHub Actions 日志

### 方式 1：通过 GitHub 网页

1. 访问：https://github.com/Claven-AI-Coding/worldcup-scout-pro
2. 点击 "Actions" 标签
3. 选择最新的工作流运行
4. 查看失败的步骤

### 方式 2：通过 GitHub CLI

```bash
# 安装 GitHub CLI
brew install gh  # macOS
# 或
sudo apt install gh  # Linux

# 登录
gh auth login

# 查看工作流运行
gh run list --repo Claven-AI-Coding/worldcup-scout-pro

# 查看特定运行的日志
gh run view <run-id> --repo Claven-AI-Coding/worldcup-scout-pro

# 查看详细日志
gh run view <run-id> --log --repo Claven-AI-Coding/worldcup-scout-pro
```

---

## 🎯 立即行动

**请告诉我：**

1. **GitHub Actions 中显示的具体错误是什么？**
   - 复制错误信息

2. **哪 5 个检查失败了？**
   - 列出失败的检查名称

3. **哪 2 个检查被跳过了？**
   - 列出被跳过的检查名称

4. **你想我做什么？**
   - 修复代码错误？
   - 修复构建问题？
   - 修复测试失败？

---

## 📊 常见的 CI/CD 检查

| 检查名称 | 用途 | 失败原因 |
|---------|------|---------|
| Linting | 代码风格检查 | 代码不符合规范 |
| Type Check | TypeScript 类型检查 | 类型错误 |
| Build | 构建检查 | 构建失败 |
| Test | 测试检查 | 测试失败 |
| Security | 安全检查 | 依赖漏洞或敏感信息 |

---

**我已准备好帮助你修复这些检查！** 🔧

**请提供具体的错误信息！** 📝

**我们会立即解决！** 💪

---

**编制时间：** 2026-03-14 22:56 GMT+8  
**状态：** 🔴 **需要调查**
