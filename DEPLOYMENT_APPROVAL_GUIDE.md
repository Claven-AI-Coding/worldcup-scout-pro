# 📊 GitHub Actions 分钟数详解 + 部署确认机制

**更新日期：** 2026-03-14  
**项目：** 世界杯球探 Pro

---

## 🕐 GitHub Actions 分钟数是什么？

### 定义

**分钟数 = 工作流运行的总时间**

每当 GitHub Actions 工作流运行时，GitHub 会计算从开始到结束的总时间（以分钟为单位）。

### 计算方式

```
总分钟数 = 所有任务的运行时间之和

例如：
- 前端测试：3 分钟
- 后端测试：3 分钟
- Docker 构建：5 分钟
- 部署：2 分钟
─────────────────
总计：13 分钟
```

### 计费规则

```
免费额度：2,000 分钟/月

超出部分：$0.24 / 1,000 分钟

例如：
- 3,000 分钟 = 2,000 (免费) + 1,000 (超出)
- 超出费用 = 1,000 ÷ 1,000 × $0.24 = $0.24
```

---

## 📈 我们项目的分钟数消耗

### 单次部署消耗

| 步骤 | 时间 | 说明 |
|------|------|------|
| 前端 Lint | 1 分钟 | 代码风格检查 |
| 前端构建 | 1 分钟 | npm run build |
| 前端测试 | 1 分钟 | npm run test |
| 后端 Lint | 1 分钟 | Ruff 检查 |
| 后端测试 | 2 分钟 | pytest 运行 |
| Docker 构建 | 5 分钟 | 构建镜像 |
| 部署 | 2 分钟 | SSH 部署 |
| **总计** | **13 分钟** | **每次部署** |

### 月度消耗估算

```
场景 1：每天 1 次部署
- 每月部署：30 次
- 月度分钟数：30 × 13 = 390 分钟
- 月度成本：免费（在 2,000 分钟内）

场景 2：每天 3 次部署
- 每月部署：90 次
- 月度分钟数：90 × 13 = 1,170 分钟
- 月度成本：免费（在 2,000 分钟内）

场景 3：每天 5 次部署
- 每月部署：150 次
- 月度分钟数：150 × 13 = 1,950 分钟
- 月度成本：免费（在 2,000 分钟内）

场景 4：每天 10 次部署
- 每月部署：300 次
- 月度分钟数：300 × 13 = 3,900 分钟
- 超出分钟数：3,900 - 2,000 = 1,900 分钟
- 月度成本：1,900 ÷ 1,000 × $0.24 = $0.456
```

### 结论

✅ **正常使用完全免费**  
✅ **即使高频部署也很便宜**  
✅ **无需担心成本**

---

## 🔔 部署前确认机制

### 问题分析

当前的自动部署流程：
```
代码提交到 main
  ↓
自动触发部署
  ↓
直接部署到生产环境
```

**风险：** 可能会部署有问题的代码

**解决方案：** 添加部署前确认机制

---

## 🛠️ 实现部署确认机制

### 方案 1：GitHub 环境保护规则（推荐）

#### 配置步骤

1. **访问仓库设置**
   - Settings → Environments → New environment
   - 创建 "production" 环境

2. **配置环保护规则**
   ```
   ☑ Required reviewers
   - 添加审查者（例如：你自己）
   
   ☑ Deployment branches
   - 只允许 main 分支部署
   ```

3. **在工作流中使用环境**
   ```yaml
   deploy:
     environment: production
     runs-on: ubuntu-latest
     # ...
   ```

#### 效果

```
代码提交到 main
  ↓
GitHub Actions 运行测试
  ↓
部署任务等待审批
  ↓
审查者收到通知
  ↓
审查者在 GitHub 中批准部署
  ↓
开始部署
```

### 方案 2：Slack 通知 + 手动确认

#### 配置步骤

```yaml
# 在 CD 工作流中添加

- name: Request Deployment Approval
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "🚀 部署前确认",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "新的部署请求\n\n提交者：${{ github.actor }}\n分支：main\n提交：${{ github.sha }}\n\n请在 GitHub 中批准部署"
            }
          }
        ]
      }
```

### 方案 3：Telegram 通知 + 手动确认

```yaml
- name: Send Telegram Notification
  uses: appleboy/telegram-action@master
  with:
    to: ${{ secrets.TELEGRAM_CHAT_ID }}
    token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
    message: |
      🚀 部署前确认
      
      提交者：${{ github.actor }}
      分支：main
      提交：${{ github.sha }}
      
      请在 GitHub 中批准部署
```

---

## 🎯 推荐方案：GitHub 环境保护规则

### 优势

✅ **原生支持** - GitHub 内置功能  
✅ **无需额外工具** - 不需要 Slack 或 Telegram  
✅ **完整审计** - 所有批准都有记录  
✅ **灵活控制** - 可以设置多个审查者  
✅ **自动通知** - GitHub 自动发送通知  

### 配置流程

#### 步骤 1：创建 Production 环境

```
Settings → Environments → New environment
环境名称：production
```

#### 步骤 2：配置保护规则

```
Required reviewers：
  ☑ 添加你的账户（或其他审查者）

Deployment branches：
  ☑ Selected branches
  ☑ main
```

#### 步骤 3：更新工作流

```yaml
deploy:
  name: Deploy to Production
  runs-on: ubuntu-latest
  needs: build-docker
  environment: production  # ← 添加这一行
  
  steps:
    - uses: actions/checkout@v4
    # ... 部署步骤 ...
```

#### 步骤 4：提交并推送

```bash
git add .github/workflows/cd.yml
git commit -m "ci: 添加部署前确认机制"
git push
```

---

## 📋 部署确认流程

### 完整流程

```
1. 代码提交到 main
   ↓
2. GitHub Actions 运行 CI 测试
   ↓
3. 构建 Docker 镜像
   ↓
4. 部署任务等待审批
   ↓
5. GitHub 发送通知给审查者
   ↓
6. 审查者在 GitHub 中查看部署
   ↓
7. 审查者点击 "Approve and deploy"
   ↓
8. 开始部署到生产环境
   ↓
9. 部署完成，发送通知
```

### 审查者的操作

1. **收到通知**
   - GitHub 发送邮件通知
   - 或在 GitHub 中看到待审批的部署

2. **查看部署详情**
   - 点击 "Review deployments"
   - 查看提交信息和测试结果

3. **批准部署**
   - 点击 "Approve and deploy"
   - 或 "Reject"

4. **部署开始**
   - 自动开始部署
   - 实时查看部署日志

---

## 🔄 完整的部署流程（带确认）

```yaml
name: CD - Auto Deploy with Approval

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-and-test:
    name: Build and Test
    runs-on: ubuntu-latest
    # ... 测试步骤 ...

  build-docker:
    name: Build Docker Images
    runs-on: ubuntu-latest
    needs: build-and-test
    # ... 构建步骤 ...

  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build-docker
    environment: production  # ← 关键：添加环境保护
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_KEY }}
          script: |
            cd /root/projects/worldcup-scout-pro
            git pull origin main
            docker-compose pull
            docker-compose down
            docker-compose up -d
            docker-compose exec -T backend alembic upgrade head
            sleep 10
            curl -f http://localhost:8000/api/health || exit 1
            echo "✅ 部署成功！"
      
      - name: Send Success Notification
        uses: appleboy/telegram-action@master
        with:
          to: ${{ secrets.TELEGRAM_CHAT_ID }}
          token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          message: |
            ✅ 部署成功！
            
            项目：世界杯球探 Pro
            分支：main
            提交：${{ github.sha }}
            审批者：${{ github.actor }}
```

---

## 📊 对比：有无确认机制

### 无确认机制

```
代码提交 → 自动测试 → 自动部署
风险：可能部署有问题的代码
```

### 有确认机制

```
代码提交 → 自动测试 → 等待审批 → 手动确认 → 部署
优势：确保只部署经过审查的代码
```

---

## 🎯 建议方案

### 立即实施

1. **配置 GitHub 环境保护规则**
   - 创建 production 环境
   - 添加必须的审查者
   - 限制只有 main 分支可以部署

2. **更新工作流**
   - 在 deploy 任务中添加 `environment: production`
   - 提交并推送

3. **测试流程**
   - 提交代码到 main
   - 查看部署是否等待审批
   - 在 GitHub 中批准部署

### 后续优化

1. **添加多个审查者**
   - 确保至少 2 个人审查

2. **添加通知**
   - Slack 通知
   - Telegram 通知
   - 邮件通知

3. **添加部署前检查**
   - 检查数据库备份
   - 检查服务器状态
   - 检查磁盘空间

---

## 💡 最佳实践

### 部署审批规则

✅ **至少 1 个审查者** - 防止单人错误  
✅ **只允许 main 分支** - 防止其他分支部署  
✅ **需要通过所有测试** - 防止不合格代码  
✅ **记录所有部署** - 便于审计  

### 部署通知规则

✅ **部署前通知** - 告知即将部署  
✅ **部署中通知** - 实时进度  
✅ **部署后通知** - 成功或失败  

---

**部署确认机制已准备就绪！** ✅

---

**配置版本：** 1.0  
**最后更新：** 2026-03-14  
**维护人：** Claven
