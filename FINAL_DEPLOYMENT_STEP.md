# 🔧 部署完成 - 最后一步：启动 Docker 容器

**问题：** 项目代码目录不存在  
**原因：** 代码还未克隆到服务器  
**解决方案：** 克隆代码并启动容器

---

## 🚀 快速修复

### 步骤 1：克隆项目代码

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 克隆项目代码 ==="
cd /opt
git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
cd worldcup-scout-pro

echo "=== 创建 .env 文件 ==="
cat > .env << 'ENV'
# 数据库配置
DATABASE_URL=postgresql://worldcup_user:worldcup123@localhost:5432/worldcup_scout

# Redis 配置
REDIS_URL=redis://localhost:6379

# API 密钥（从 DEPLOYMENT_SECRETS.md 获取）
ANTHROPIC_AUTH_TOKEN=[从 DEPLOYMENT_SECRETS.md 获取]
ANTHROPIC_BASE_URL=https://luckycodecc.cn/claude

# COS 配置（从 DEPLOYMENT_SECRETS.md 获取）
COS_SECRET_ID=[从 DEPLOYMENT_SECRETS.md 获取]
COS_SECRET_KEY=[从 DEPLOYMENT_SECRETS.md 获取]
COS_BUCKET=worldcup-scout-pro
COS_REGION=ap-beijing

# 应用配置
FRONTEND_URL=https://graysonwit.online
API_URL=https://api.graysonwit.online
NODE_ENV=production
ENV

echo "=== 启动 Docker 容器 ==="
docker-compose up -d

echo "=== 验证容器 ==="
docker-compose ps

echo "✅ 所有容器已启动！"
EOF
```

### 步骤 2：验证部署

```bash
# 检查容器状态
ssh root@111.228.15.109 'cd /opt/worldcup-scout-pro && docker-compose ps'

# 查看容器日志
ssh root@111.228.15.109 'cd /opt/worldcup-scout-pro && docker-compose logs -f'

# 测试前端
curl -I https://graysonwit.online

# 测试后端 API
curl -I https://api.graysonwit.online
```

---

## 📋 完整的一键修复脚本

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 克隆项目代码 ==="
cd /opt
git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
cd worldcup-scout-pro

echo "=== 创建 .env 文件 ==="
cat > .env << 'ENV'
DATABASE_URL=postgresql://worldcup_user:worldcup123@localhost:5432/worldcup_scout
REDIS_URL=redis://localhost:6379
ANTHROPIC_AUTH_TOKEN=[从 DEPLOYMENT_SECRETS.md 获取]
ANTHROPIC_BASE_URL=https://luckycodecc.cn/claude
COS_SECRET_ID=[从 DEPLOYMENT_SECRETS.md 获取]
COS_SECRET_KEY=[从 DEPLOYMENT_SECRETS.md 获取]
COS_BUCKET=worldcup-scout-pro
COS_REGION=ap-beijing
FRONTEND_URL=https://graysonwit.online
API_URL=https://api.graysonwit.online
NODE_ENV=production
ENV

echo "=== 启动 Docker 容器 ==="
docker-compose up -d

echo "=== 验证容器 ==="
docker-compose ps

echo "✅ 部署完成！"
echo ""
echo "访问网站："
echo "  前端：https://graysonwit.online"
echo "  后端 API：https://api.graysonwit.online"
EOF
```

---

## ✅ 部署完成后应该看到

```
✅ 项目代码已克隆
✅ .env 文件已创建
✅ Docker 容器已启动
✅ 所有服务正常运行
```

---

## 🎯 验证部署

```bash
# 1. 检查 Nginx
ssh root@111.228.15.109 'systemctl status nginx'

# 2. 检查 Docker 容器
ssh root@111.228.15.109 'cd /opt/worldcup-scout-pro && docker-compose ps'

# 3. 测试 HTTPS
curl -I https://graysonwit.online

# 4. 查看容器日志
ssh root@111.228.15.109 'cd /opt/worldcup-scout-pro && docker-compose logs'
```

---

**立即执行这个修复脚本！** 🚀

**告诉我部署的最终结果！** 📝

**成功后你的网站就完全上线了！** 🎉
