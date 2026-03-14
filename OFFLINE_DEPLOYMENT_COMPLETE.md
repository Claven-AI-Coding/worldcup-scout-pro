# 🚀 完整的离线部署方案

**时间：** 2026-03-15 01:31 GMT+8  
**问题：** 服务器无法连接互联网  
**解决方案：** 在本地准备代码，上传到服务器  
**状态：** 🟢 **准备部署**

---

## 📋 部署步骤

### 步骤 1：在你的电脑上克隆项目

```bash
# 在你的 Mac 上执行
cd ~/Downloads  # 或任何你想放的目录

git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
cd worldcup-scout-pro
```

### 步骤 2：打包项目

```bash
# 在项目目录中执行
cd ~/Downloads
tar -czf worldcup-scout-pro.tar.gz worldcup-scout-pro/
```

### 步骤 3：上传到服务器

```bash
# 在你的 Mac 上执行
scp worldcup-scout-pro.tar.gz root@111.228.15.109:/opt/
```

### 步骤 4：在服务器上解压并部署

```bash
# 在你的 Mac 上执行
ssh root@111.228.15.109 << 'EOF'
cd /opt
rm -rf worldcup-scout-pro
tar -xzf worldcup-scout-pro.tar.gz
rm worldcup-scout-pro.tar.gz
cd worldcup-scout-pro

# 创建 .env 文件（需要手动填入密钥）
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

echo "✅ 项目已准备好"
EOF
```

### 步骤 5：安装依赖和启动应用

```bash
ssh root@111.228.15.109 << 'EOF'
cd /opt/worldcup-scout-pro

echo "=== 安装 Node.js 依赖 ==="
npm install

echo "=== 构建应用 ==="
npm run build

echo "=== 启动应用 ==="
npm start &

sleep 3

echo "✅ 应用已启动"
EOF
```

---

## 🎯 完整的一键部署命令

**在你的 Mac 上执行这个完整的脚本：**

```bash
# 1. 克隆项目
cd ~/Downloads
git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git

# 2. 打包
tar -czf worldcup-scout-pro.tar.gz worldcup-scout-pro/

# 3. 上传
scp worldcup-scout-pro.tar.gz root@111.228.15.109:/opt/

# 4. 解压并部署
ssh root@111.228.15.109 << 'DEPLOY'
cd /opt
rm -rf worldcup-scout-pro
tar -xzf worldcup-scout-pro.tar.gz
rm worldcup-scout-pro.tar.gz
cd worldcup-scout-pro

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

npm install
npm run build
npm start &

sleep 3

echo "✅ 部署完成！"
DEPLOY
```

---

## ✅ 验证部署

```bash
# 检查项目
ssh root@111.228.15.109 'ls -la /opt/worldcup-scout-pro/ | head -20'

# 检查应用是否运行
ssh root@111.228.15.109 'ps aux | grep node'

# 检查数据库
ssh root@111.228.15.109 'sudo -u postgres psql -d worldcup_scout -c "SELECT 1;"'

# 检查 Redis
ssh root@111.228.15.109 'redis-cli ping'

# 测试网站
curl -I https://graysonwit.online
curl -I https://api.graysonwit.online
```

---

## 📊 部署完成后的架构

```
你的 Mac
    ↓
Nginx (反向代理 + SSL) ✅ 已配置
    ↓
前端应用 (Node.js) ← 即将启动
    ↓
后端 API (Node.js) ← 即将启动
    ↓
PostgreSQL ✅ 已安装
Redis ✅ 已安装
COS ✅ 已配置
```

---

**现在就执行这个完整的脚本！** 🚀

**告诉我部署的结果！** 📝

**成功后你的网站就完全上线了！** 🎉
