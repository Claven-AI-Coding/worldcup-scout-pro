# 🚀 自动部署配置指南

**项目名称：** 世界杯球探 Pro  
**配置日期：** 2026-03-14  
**自动化工具：** GitHub Actions

---

## 📋 自动部署流程

### 工作流程图

```
代码提交到 main
    ↓
GitHub Actions 触发
    ↓
1️⃣ 构建和测试
   - 前端 Lint + 构建 + 测试
   - 后端 Lint + 测试
    ↓
2️⃣ 构建 Docker 镜像
   - 后端镜像
   - 前端镜像
    ↓
3️⃣ 部署到生产环境
   - 拉取代码
   - 更新镜像
   - 启动服务
   - 数据库迁移
   - 健康检查
    ↓
4️⃣ 部署通知
   - Telegram 通知
   - GitHub 状态更新
    ↓
✅ 部署完成
```

---

## 🔧 配置步骤

### 步骤 1：配置 GitHub Secrets

在 GitHub 仓库设置中添加以下 Secrets：

#### 部署服务器信息
```
DEPLOY_HOST: 你的服务器 IP 或域名
DEPLOY_USER: SSH 用户名（通常是 root）
DEPLOY_KEY: SSH 私钥（用于无密码登录）
```

#### Telegram 通知（可选）
```
TELEGRAM_BOT_TOKEN: 你的 Telegram Bot Token
TELEGRAM_CHAT_ID: 你的 Telegram Chat ID
```

### 步骤 2：生成 SSH 密钥

```bash
# 在本地生成 SSH 密钥
ssh-keygen -t ed25519 -f deploy_key -N ""

# 查看私钥（用于 DEPLOY_KEY）
cat deploy_key

# 将公钥添加到服务器
ssh-copy-id -i deploy_key.pub root@your-server-ip
```

### 步骤 3：配置服务器

在部署服务器上执行：

```bash
# 1. 安装 Docker 和 Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. 克隆项目
cd /root/projects
git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
cd worldcup-scout-pro

# 3. 配置 .env 文件
cp .env.example .env
# 编辑 .env，配置真实的 API 密钥

# 4. 初始化数据库
docker-compose up -d db redis
docker-compose exec backend alembic upgrade head
```

### 步骤 4：配置 GitHub Actions

工作流文件已创建：`.github/workflows/cd.yml`

**工作流包含以下步骤：**

1. **构建和测试**
   - 前端：Lint + 构建 + 测试
   - 后端：Lint + 测试

2. **构建 Docker 镜像**
   - 推送到 GitHub Container Registry

3. **部署**
   - SSH 连接到服务器
   - 拉取最新代码
   - 更新 Docker 镜像
   - 启动服务
   - 运行数据库迁移
   - 健康检查

4. **通知**
   - Telegram 通知
   - GitHub 状态更新

---

## 📊 工作流详解

### 触发条件

```yaml
on:
  push:
    branches: [main]      # 只在 main 分支推送时触发
  workflow_dispatch:      # 允许手动触发
```

### 环境变量

```yaml
env:
  REGISTRY: ghcr.io                           # GitHub Container Registry
  IMAGE_NAME: ${{ github.repository }}        # 镜像名称
```

### 任务依赖

```
build-and-test (必须通过)
    ↓
build-docker (依赖 build-and-test)
    ↓
deploy (依赖 build-docker，仅在 main 分支)
    ↓
notify (总是执行，用于通知)
```

---

## 🔐 安全配置

### 最佳实践

1. **使用 SSH 密钥而不是密码**
   ```bash
   ssh-keygen -t ed25519 -f deploy_key -N ""
   ```

2. **限制 SSH 密钥权限**
   ```bash
   chmod 600 deploy_key
   ```

3. **使用 GitHub Secrets 存储敏感信息**
   - 不要在代码中硬编码密钥
   - 使用 `${{ secrets.SECRET_NAME }}`

4. **定期轮换密钥**
   - 每 3 个月更新一次 SSH 密钥
   - 更新 GitHub Secrets

5. **监控部署日志**
   - 检查 GitHub Actions 日志
   - 检查服务器日志

---

## 📈 监控和调试

### 查看部署日志

1. **GitHub Actions 日志**
   - 访问 GitHub 仓库
   - 点击 "Actions" 标签
   - 选择最新的工作流运行
   - 查看每个步骤的日志

2. **服务器日志**
   ```bash
   # SSH 连接到服务器
   ssh root@your-server-ip
   
   # 查看 Docker 日志
   docker-compose logs -f
   
   # 查看特定服务日志
   docker-compose logs -f backend
   ```

### 常见问题

**Q: 部署失败，显示 "SSH 连接失败"**  
A: 检查 DEPLOY_KEY 是否正确，确保公钥已添加到服务器

**Q: 部署成功但服务无法访问**  
A: 检查防火墙规则，确保端口 5173 和 8000 已开放

**Q: 数据库迁移失败**  
A: 检查数据库连接，查看 Docker 日志

---

## 🔄 手动触发部署

如果需要手动触发部署（不需要提交代码）：

1. 访问 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择 "CD - Auto Deploy" 工作流
4. 点击 "Run workflow"
5. 选择分支（main）
6. 点击 "Run workflow"

---

## 📝 部署检查清单

部署完成后，请检查以下项目：

- [ ] GitHub Actions 工作流成功完成
- [ ] 所有测试通过
- [ ] Docker 镜像构建成功
- [ ] SSH 部署成功
- [ ] 服务器上的服务正常运行
- [ ] 前端可以访问
- [ ] 后端 API 可以调用
- [ ] 数据库迁移成功
- [ ] 健康检查通过
- [ ] Telegram 通知已收到

---

## 🎯 自动部署优势

✅ **自动化流程** - 无需手动部署  
✅ **持续集成** - 每次提交都会测试  
✅ **快速反馈** - 立即知道部署是否成功  
✅ **减少人工错误** - 流程标准化  
✅ **可追溯性** - 每次部署都有记录  
✅ **回滚能力** - 可以快速回滚到上一个版本  

---

## 🚀 下一步

### 立即可以做的
1. 配置 GitHub Secrets
2. 生成 SSH 密钥
3. 配置服务器
4. 测试自动部署

### 后续改进
1. 添加自动回滚机制
2. 添加性能监控
3. 添加自动备份
4. 添加灾难恢复计划

---

## 📞 故障排查

### 部署失败排查步骤

1. **检查 GitHub Actions 日志**
   ```
   Actions → 最新工作流 → 查看日志
   ```

2. **检查测试是否通过**
   ```
   查看 "Build and Test" 步骤的输出
   ```

3. **检查 Docker 镜像构建**
   ```
   查看 "Build Docker Images" 步骤的输出
   ```

4. **检查 SSH 连接**
   ```
   查看 "Deploy via SSH" 步骤的输出
   ```

5. **检查服务器日志**
   ```bash
   ssh root@your-server-ip
   docker-compose logs -f
   ```

---

**自动部署配置版本：** 1.0  
**最后更新：** 2026-03-14  
**维护人：** Claven

---

## 💡 自动部署最佳实践

### 代码提交规范
- 使用 Conventional Commits
- 每个提交都应该是可部署的
- 避免在 main 分支上直接提交

### 分支策略
- `main` - 生产环境
- `develop` - 开发环境
- `feature/*` - 功能分支

### 部署策略
- 自动部署到生产环境
- 部署前运行完整测试
- 部署后进行健康检查
- 失败时自动通知

### 监控策略
- 监控部署日志
- 监控应用性能
- 监控错误率
- 定期备份数据

---

**项目已配置完整的自动部署流程！** 🚀
