# 🔧 项目结构修复和部署指南

**时间：** 2026-03-15 00:59 GMT+8  
**问题：** package.json 找不到  
**原因：** 项目代码结构不完整或目录错误  
**状态：** 🔴 **立即修复**

---

## 🚨 问题分析

**错误信息：** `Could not read package.json: Error: ENOENT: no such file or directory`

这说明：
1. `/opt/worldcup-scout-pro` 目录存在但是空的
2. 或者项目代码没有正确克隆
3. 或者 package.json 在子目录中

---

## 🚀 快速修复方案

### 步骤 1：检查项目结构

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 检查项目目录 ==="
ls -la /opt/worldcup-scout-pro/

echo ""
echo "=== 查找 package.json ==="
find /opt -name "package.json" 2>/dev/null

echo ""
echo "=== 查看目录大小 ==="
du -sh /opt/worldcup-scout-pro/
EOF
```

### 步骤 2：清理并重新克隆

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 备份旧目录 ==="
mv /opt/worldcup-scout-pro /opt/worldcup-scout-pro.bak

echo "=== 重新克隆项目 ==="
cd /opt
git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
cd worldcup-scout-pro

echo "=== 验证项目结构 ==="
ls -la

echo ""
echo "=== 检查 package.json ==="
cat package.json | head -20

echo "✅ 项目已重新克隆"
EOF
```

### 步骤 3：创建 .env 文件

```bash
ssh root@111.228.15.109 << 'EOF'
cd /opt/worldcup-scout-pro

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

echo "✅ .env 文件已创建"
EOF
```

### 步骤 4：安装依赖

```bash
ssh root@111.228.15.109 << 'EOF'
cd /opt/worldcup-scout-pro

echo "=== 安装 Node.js 依赖 ==="
npm install

echo "✅ 依赖已安装"
EOF
```

### 步骤 5：构建应用

```bash
ssh root@111.228.15.109 << 'EOF'
cd /opt/worldcup-scout-pro

echo "=== 构建应用 ==="
npm run build

echo "✅ 应用已构建"
EOF
```

### 步骤 6：启动应用

```bash
ssh root@111.228.15.109 << 'EOF'
cd /opt/worldcup-scout-pro

echo "=== 启动应用 ==="
npm start &

sleep 3

echo "✅ 应用已启动"
EOF
```

---

## 📋 完整的一键修复脚本

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=========================================="
echo "项目结构修复和部署"
echo "=========================================="
echo ""

echo "[1/6] 备份旧目录..."
mv /opt/worldcup-scout-pro /opt/worldcup-scout-pro.bak 2>/dev/null || true

echo "[2/6] 重新克隆项目..."
cd /opt
git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
cd worldcup-scout-pro

echo "[3/6] 创建 .env 文件..."
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

echo "[4/6] 安装依赖..."
npm install

echo "[5/6] 构建应用..."
npm run build

echo "[6/6] 启动应用..."
npm start &

sleep 3

echo ""
echo "=========================================="
echo "✅ 部署完成！"
echo "=========================================="
echo ""
echo "访问网站："
echo "  前端：https://graysonwit.online"
echo "  后端 API：https://api.graysonwit.online"
EOF
```

---

## ✅ 验证部署

```bash
# 检查项目结构
ssh root@111.228.15.109 'ls -la /opt/worldcup-scout-pro/'

# 检查 package.json
ssh root@111.228.15.109 'cat /opt/worldcup-scout-pro/package.json | head -20'

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

## 🎯 如果还是有问题

**查看应用日志：**

```bash
ssh root@111.228.15.109 'cd /opt/worldcup-scout-pro && npm start'
```

这样可以看到详细的错误信息。

---

**立即执行修复脚本！** 🚀

**告诉我修复的结果！** 📝

**成功后你的网站就完全上线了！** 🎉

---

**编制时间：** 2026-03-15 00:59 GMT+8  
**状态：** 🔴 **立即修复**
