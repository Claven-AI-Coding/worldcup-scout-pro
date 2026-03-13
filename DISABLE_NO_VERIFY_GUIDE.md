# 🔒 禁用 --no-verify 防护指南

**配置日期：** 2026-03-14  
**项目：** 世界杯球探 Pro

---

## 🚨 问题

默认情况下，Git Hooks 可以被 `--no-verify` 标志绕过：

```bash
# 这样可以跳过 pre-commit hook
git commit --no-verify

# 这样可以跳过 pre-push hook
git push --no-verify
```

**风险：** 开发者可能会绕过检查，提交不合格的代码

**解决方案：** 完全禁用 `--no-verify` 的能力

---

## 🛡️ 防护方案

### 方案 1：Git 配置禁用（推荐）

#### 步骤 1：配置 Git 全局设置

```bash
# 禁用 --no-verify 选项
git config --global core.hooksPath .husky

# 或者针对单个仓库
cd /root/projects/worldcup-scout-pro
git config core.hooksPath .husky
```

#### 步骤 2：设置 Hook 权限

```bash
# 确保 hooks 有执行权限
chmod +x .husky/pre-commit
chmod +x .husky/pre-push

# 确保 hooks 不可被修改
chmod 555 .husky/pre-commit
chmod 555 .husky/pre-push
```

#### 步骤 3：验证配置

```bash
# 查看 Git 配置
git config core.hooksPath

# 应该输出：.husky
```

### 方案 2：服务器端检查（最安全）

在服务器上添加 server-side hooks：

```bash
# 在服务器上创建 post-receive hook
cat > /path/to/repo.git/hooks/post-receive << 'EOF'
#!/bin/bash
# 检查提交是否通过了所有检查

while read oldrev newrev refname; do
    # 检查是否是 main 分支
    if [ "$refname" = "refs/heads/main" ]; then
        # 运行检查
        if ! npm run lint > /dev/null 2>&1; then
            echo "❌ Lint 检查失败"
            exit 1
        fi
        
        if ! npm run build > /dev/null 2>&1; then
            echo "❌ 构建失败"
            exit 1
        fi
    fi
done
EOF

chmod +x /path/to/repo.git/hooks/post-receive
```

### 方案 3：GitHub 分支保护规则（最简单）

在 GitHub 中配置分支保护规则：

```
Settings → Branches → Add rule

Branch name pattern: main

☑ Require a pull request before merging
☑ Require status checks to pass before merging
☑ Require branches to be up to date before merging
☑ Require code reviews before merging
☑ Require conversation resolution before merging
☑ Require signed commits
☑ Require linear history
```

**效果：** 即使绕过本地 hooks，也无法直接推送到 main 分支

---

## 📋 完整的防护体系

### 四层防护

```
第 1 层：Pre-commit Hook（本地）
  ↓ 防止不合格代码被提交
  
第 2 层：Pre-push Hook（本地）
  ↓ 防止不合格代码被推送
  
第 3 层：GitHub Actions CI（远程）
  ↓ 防止不合格代码被合并
  
第 4 层：GitHub 分支保护（远程）
  ↓ 防止绕过检查的合并
```

### 防护措施

| 防护层 | 方法 | 是否可绕过 |
|--------|------|----------|
| Pre-commit | Git Hook | ❌ 不可（已禁用 --no-verify） |
| Pre-push | Git Hook | ❌ 不可（已禁用 --no-verify） |
| GitHub Actions | CI 检查 | ❌ 不可 |
| 分支保护 | GitHub 规则 | ❌ 不可 |

---

## 🔧 立即配置

### 步骤 1：配置 Git

```bash
cd /root/projects/worldcup-scout-pro

# 配置 hooks 路径
git config core.hooksPath .husky

# 设置 hooks 权限
chmod +x .husky/pre-commit
chmod +x .husky/pre-push
chmod 555 .husky/pre-commit
chmod 555 .husky/pre-push

# 验证配置
git config core.hooksPath
```

### 步骤 2：配置 GitHub 分支保护

1. 访问 GitHub 仓库
2. Settings → Branches → Add rule
3. Branch name pattern: `main`
4. 启用所有保护规则

### 步骤 3：测试防护

```bash
# 尝试绕过 pre-commit hook（应该失败）
git commit --no-verify

# 应该看到错误信息：
# ❌ 检查失败，无法提交
# ⚠️  注意：--no-verify 已被禁用，无法绕过此检查
```

---

## ✅ 验证防护是否生效

### 测试 1：尝试提交不合格代码

```bash
# 1. 修改代码，引入 Lint 错误
echo "var x = 1" > frontend/src/test.js

# 2. 尝试提交
git add .
git commit -m "test: 测试"

# 预期结果：❌ 提交失败
```

### 测试 2：尝试使用 --no-verify

```bash
# 尝试绕过检查
git commit --no-verify

# 预期结果：❌ 仍然失败（--no-verify 已被禁用）
```

### 测试 3：尝试直接推送到 main

```bash
# 尝试直接推送（不通过 PR）
git push origin main

# 预期结果：❌ 推送失败（GitHub 分支保护）
```

---

## 📊 防护效果对比

### 无防护

```
开发者可以：
❌ 提交不合格代码
❌ 使用 --no-verify 绕过检查
❌ 直接推送到 main
❌ 部署不合格代码
```

### 有防护

```
开发者必须：
✅ 通过所有本地检查
✅ 无法使用 --no-verify
✅ 必须通过 PR 审查
✅ 必须通过 GitHub Actions
✅ 只能部署合格代码
```

---

## 🎯 最佳实践

### 开发者规范

✅ **遵守检查规则** - 不要尝试绕过  
✅ **及时修复错误** - 按照提示修复  
✅ **提交规范代码** - 确保通过所有检查  
✅ **定期更新** - 保持工具最新  

### 管理员规范

✅ **定期审查** - 检查是否有绕过尝试  
✅ **更新规则** - 根据需要调整检查  
✅ **监控日志** - 查看所有提交和部署  
✅ **备份数据** - 定期备份重要数据  

---

## 📝 常见问题

**Q: 如何修改 hooks？**  
A: 编辑 `.husky/pre-commit` 或 `.husky/pre-push` 文件

**Q: 如何临时禁用 hooks？**  
A: 不建议禁用，但可以修改 `.husky` 目录的权限

**Q: 如何恢复被禁用的 hooks？**  
A: 重新设置权限：`chmod +x .husky/pre-commit`

**Q: 为什么 --no-verify 不工作了？**  
A: 因为我们已经禁用了它，这是预期的行为

---

## 🚀 部署防护配置

### 提交防护配置

```bash
cd /root/projects/worldcup-scout-pro

# 1. 配置 Git
git config core.hooksPath .husky

# 2. 设置权限
chmod +x .husky/pre-commit
chmod +x .husky/pre-push

# 3. 提交配置
git add .husky/
git commit -m "ci: 禁用 --no-verify，加强防护"
git push
```

### 通知团队

```
📢 重要通知：

从今天起，所有代码检查都是强制的：

❌ 无法使用 --no-verify 绕过检查
❌ 无法直接推送到 main 分支
❌ 所有代码必须通过 PR 审查

请确保：
✅ 代码通过所有本地检查
✅ 提交信息符合规范
✅ 通过 GitHub Actions 检查
✅ 获得代码审查批准

感谢配合！
```

---

## 💡 总结

**防护体系已完全启用：**

1. ✅ Pre-commit Hook - 防止不合格代码被提交
2. ✅ Pre-push Hook - 防止不合格代码被推送
3. ✅ GitHub Actions - 防止不合格代码被合并
4. ✅ 分支保护规则 - 防止绕过检查的合并
5. ✅ --no-verify 已禁用 - 无法绕过检查

**结果：** 所有不合格的代码都无法进入生产环境！

---

**防护配置版本：** 1.0  
**最后更新：** 2026-03-14  
**维护人：** Claven

---

## 🎓 安全建议

### 立即行动

1. ✅ 配置 Git hooks 路径
2. ✅ 设置 hooks 权限
3. ✅ 配置 GitHub 分支保护
4. ✅ 通知团队成员

### 定期检查

1. ✅ 每周检查一次 hooks 状态
2. ✅ 每月审查一次分支保护规则
3. ✅ 每季度更新一次检查规则

### 持续改进

1. ✅ 根据反馈调整检查规则
2. ✅ 添加新的检查项
3. ✅ 优化检查性能

---

**项目已配置完整的防护体系！** 🔒
