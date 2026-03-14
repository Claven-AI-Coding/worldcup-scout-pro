# 🚀 完整的本地部署方案（无需 Docker 镜像下载）

**时间：** 2026-03-15 00:50 GMT+8  
**问题：** 服务器无法下载 Docker 镜像  
**解决方案：** 使用本地安装的 PostgreSQL 和 Redis  
**状态：** 🟢 **立即执行**

---

## 📋 部署架构

```
前端应用 (Node.js)
    ↓
Nginx (反向代理 + SSL)
    ↓
后端应用 (Node.js)
    ↓
PostgreSQL (本地安装)
Redis (本地安装)
COS (腾讯云对象存储)
```

---

## 🚀 一键完整部署脚本

**执行这个脚本完成所有部署：**

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=========================================="
echo "世界杯球探 Pro - 完整本地部署"
echo "=========================================="
echo ""

# ============ 第一步：安装系统依赖 ============
echo "[1/8] 安装系统依赖..."
apt update
apt install -y \
  curl wget git vim htop \
  postgresql postgresql-contrib \
  redis-server \
  nodejs npm \
  build-essential python3

echo "✅ 系统依赖已安装"
echo ""

# ============ 第二步：启动数据库服务 ============
echo "[2/8] 启动 PostgreSQL 和 Redis..."
systemctl start postgresql
systemctl start redis-server
systemctl enable postgresql
systemctl enable redis-server

echo "✅ 数据库服务已启动"
echo ""

# ============ 第三步：创建数据库 ============
echo "[3/8] 创建数据库..."
sudo -u postgres createdb worldcup_scout 2>/dev/null || true
sudo -u postgres createuser worldcup_user 2>/dev/null || true
sudo -u postgres psql -c "ALTER USER worldcup_user WITH PASSWORD 'worldcup123';" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE worldcup_scout TO worldcup_user;" 2>/dev/null || true

echo "✅ 数据库已创建"
echo ""

# ============ 第四步：克隆项目代码 ============
echo "[4/8] 克隆项目代码..."
cd /opt
if [ ! -d "worldcup-scout-pro" ]; then
    git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
fi
cd worldcup-scout-pro

echo "✅ 项目代码已克隆"
echo ""

# ============ 第五步：创建 .env 文件 ============
echo "[5/8] 创建 .env 文件..."
cat > .env << 'ENV'
# 数据库配置
DATABASE_URL=postgresql://worldcup_user:worldcup123@localhost:5432/worldcup_scout

# Redis 配置
REDIS_URL=redis://localhost:6379

# API 密钥（需要手动填入）
ANTHROPIC_AUTH_TOKEN=[从 DEPLOYMENT_SECRETS.md 获取]
ANTHROPIC_BASE_URL=https://luckycodecc.cn/claude

# COS 配置（需要手动填入）
COS_SECRET_ID=[从 DEPLOYMENT_SECRETS.md 获取]
COS_SECRET_KEY=[从 DEPLOYMENT_SECRETS.md 获取]
COS_BUCKET=worldcup-scout-pro
COS_REGION=ap-beijing

# 应用配置
FRONTEND_URL=https://graysonwit.online
API_URL=https://api.graysonwit.online
NODE_ENV=production
ENV

echo "✅ .env 文件已创建"
echo ""

# ============ 第六步：安装依赖 ============
echo "[6/8] 安装 Node.js 依赖..."
npm install

echo "✅ Node.js 依赖已安装"
echo ""

# ============ 第七步：构建应用 ============
echo "[7/8] 构建应用..."
npm run build

echo "✅ 应用已构建"
echo ""

# ============ 第八步：启动应用 ============
echo "[8/8] 启动应用..."
npm start &

sleep 3

echo "✅ 应用已启动"
echo ""

echo "=========================================="
echo "✅ 部署完成！"
echo "=========================================="
echo ""
echo "访问网站："
echo "  前端：https://graysonwit.online"
echo "  后端 API：https://api.graysonwit.online"
echo ""
echo "验证命令："
echo "  systemctl status postgresql"
echo "  systemctl status redis-server"
echo "  ps aux | grep node"
EOF
```

---

## 📝 如果上面的脚本太复杂，使用简化版本

**只安装数据库和启动应用：**

```bash
ssh root@111.228.15.109 << 'EOF'
# 1. 安装 PostgreSQL 和 Redis
apt update
apt install -y postgresql postgresql-contrib redis-server

# 2. 启动服务
systemctl start postgresql
systemctl start redis-server
systemctl enable postgresql
systemctl enable redis-server

# 3. 创建数据库
sudo -u postgres createdb worldcup_scout
sudo -u postgres createuser worldcup_user
sudo -u postgres psql -c "ALTER USER worldcup_user WITH PASSWORD 'worldcup123';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE worldcup_scout TO worldcup_user;"

# 4. 克隆项目
cd /opt
git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
cd worldcup-scout-pro

# 5. 创建 .env 文件
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

# 6. 安装依赖
npm install

# 7. 构建应用
npm run build

# 8. 启动应用
npm start &

echo "✅ 部署完成！"
EOF
```

---

## ✅ 验证部署

```bash
# 检查 PostgreSQL
ssh root@111.228.15.109 'systemctl status postgresql'

# 检查 Redis
ssh root@111.228.15.109 'systemctl status redis-server'

# 检查 Node.js 应用
ssh root@111.228.15.109 'ps aux | grep node'

# 测试数据库连接
ssh root@111.228.15.109 'sudo -u postgres psql -d worldcup_scout -c "SELECT 1;"'

# 测试 Redis 连接
ssh root@111.228.15.109 'redis-cli ping'

# 测试网站
curl -I https://graysonwit.online
curl -I https://api.graysonwit.online
```

---

## 🎯 如果应用启动失败

**查看应用日志：**

```bash
ssh root@111.228.15.109 'cd /opt/worldcup-scout-pro && npm start'
```

这样可以看到详细的错误信息。

---

## 📊 部署完成后的架构

```
用户访问
    ↓
https://graysonwit.online (Nginx + SSL)
    ↓
前端应用 (localhost:3000)
    ↓
后端 API (localhost:8000)
    ↓
PostgreSQL (localhost:5432)
Redis (localhost:6379)
COS (腾讯云)
```

---

**立即执行部署脚本！** 🚀

**告诉我部署的结果！** 📝

**成功后你的网站就完全上线了！** 🎉

---

**编制时间：** 2026-03-15 00:50 GMT+8  
**状态：** 🟢 **准备部署**
