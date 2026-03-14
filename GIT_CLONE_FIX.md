# 🔧 Git 克隆失败修复方案

**时间：** 2026-03-15 01:05 GMT+8  
**问题：** Git 克隆失败 - RPC failed  
**原因：** 网络问题或 Git HTTP2 问题  
**状态：** 🔴 **立即修复**

---

## 🚨 问题分析

**错误信息：** `RPC failed; curl 16 Error in the HTTP2 framing layer`

这说明：
1. 网络连接不稳定
2. Git 使用 HTTP2 出现问题
3. 需要禁用 HTTP2 或使用 SSH

---

## 🚀 解决方案

### 方案 A：禁用 Git HTTP2（推荐快速）

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 禁用 Git HTTP2 ==="
git config --global http.version HTTP/1.1

echo "=== 清理旧目录 ==="
rm -rf /opt/worldcup-scout-pro

echo "=== 重新克隆项目 ==="
cd /opt
git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git

echo "=== 验证克隆 ==="
ls -la /opt/worldcup-scout-pro/

echo "✅ 项目克隆成功"
EOF
```

### 方案 B：使用 SSH 克隆（更稳定）

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 配置 SSH ==="
mkdir -p ~/.ssh
ssh-keyscan github.com >> ~/.ssh/known_hosts 2>/dev/null

echo "=== 清理旧目录 ==="
rm -rf /opt/worldcup-scout-pro

echo "=== 使用 SSH 克隆项目 ==="
cd /opt
git clone git@github.com:Claven-AI-Coding/worldcup-scout-pro.git

echo "=== 验证克隆 ==="
ls -la /opt/worldcup-scout-pro/

echo "✅ 项目克隆成功"
EOF
```

### 方案 C：手动下载 ZIP 文件（最稳定）

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 下载项目 ZIP 文件 ==="
cd /opt
rm -rf worldcup-scout-pro

# 下载 ZIP 文件
wget https://github.com/Claven-AI-Coding/worldcup-scout-pro/archive/refs/heads/main.zip

# 解压
unzip -q main.zip

# 重命名目录
mv worldcup-scout-pro-main worldcup-scout-pro

# 清理 ZIP 文件
rm main.zip

echo "=== 验证 ==="
ls -la /opt/worldcup-scout-pro/

echo "✅ 项目下载成功"
EOF
```

---

## 📋 完整的修复和部署脚本

**使用方案 A（推荐）：**

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=========================================="
echo "Git 克隆修复和应用部署"
echo "=========================================="
echo ""

echo "[1/7] 禁用 Git HTTP2..."
git config --global http.version HTTP/1.1

echo "[2/7] 清理旧目录..."
rm -rf /opt/worldcup-scout-pro

echo "[3/7] 重新克隆项目..."
cd /opt
git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
cd worldcup-scout-pro

echo "[4/7] 创建 .env 文件..."
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

echo "[5/7] 安装依赖..."
npm install

echo "[6/7] 构建应用..."
npm run build

echo "[7/7] 启动应用..."
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
# 检查项目是否存在
ssh root@111.228.15.109 'ls -la /opt/worldcup-scout-pro/ | head -20'

# 检查 package.json
ssh root@111.228.15.109 'cat /opt/worldcup-scout-pro/package.json | head -10'

# 检查应用是否运行
ssh root@111.228.15.109 'ps aux | grep node'

# 测试网站
curl -I https://graysonwit.online
curl -I https://api.graysonwit.online
```

---

## 🎯 如果克隆还是失败

**尝试方案 C（手动下载 ZIP）：**

```bash
ssh root@111.228.15.109 << 'EOF'
cd /opt
rm -rf worldcup-scout-pro
wget https://github.com/Claven-AI-Coding/worldcup-scout-pro/archive/refs/heads/main.zip
unzip -q main.zip
mv worldcup-scout-pro-main worldcup-scout-pro
rm main.zip
ls -la worldcup-scout-pro/
EOF
```

---

**立即执行修复脚本！** 🚀

**告诉我修复的结果！** 📝

**成功后你的网站就完全上线了！** 🎉

---

**编制时间：** 2026-03-15 01:05 GMT+8  
**状态：** 🔴 **立即修复**
