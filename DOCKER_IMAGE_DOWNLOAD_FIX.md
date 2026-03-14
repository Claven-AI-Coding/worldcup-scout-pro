# 🔧 Docker 镜像下载失败修复方案

**问题时间：** 2026-03-15 00:32 GMT+8  
**根本原因：** Docker 无法下载镜像（网络或镜像源问题）  
**错误信息：** `failed to resolve reference "docker.io/library/postgres:16-alpine"`  
**状态：** 🔴 **立即修复**

---

## 🚨 问题分析

**Docker 尝试从腾讯云镜像源下载，但失败了。**

可能的原因：
1. Docker 镜像源配置错误
2. 网络连接问题
3. 腾讯云镜像源不可用

---

## 🚀 快速修复方案

### 方案 A：使用官方 Docker 镜像源（推荐）

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 配置 Docker 镜像源 ==="

# 创建 Docker 配置目录
mkdir -p /etc/docker

# 创建 daemon.json 配置文件
cat > /etc/docker/daemon.json << 'DOCKER'
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://registry.docker-cn.com",
    "https://mirror.baidubce.com"
  ]
}
DOCKER

echo "=== 重启 Docker ==="
systemctl daemon-reload
systemctl restart docker

echo "=== 验证配置 ==="
docker info | grep -A 5 "Registry Mirrors"

echo "✅ Docker 镜像源已配置"
EOF
```

### 方案 B：使用阿里云镜像源

```bash
ssh root@111.228.15.109 << 'EOF'
mkdir -p /etc/docker

cat > /etc/docker/daemon.json << 'DOCKER'
{
  "registry-mirrors": [
    "https://registry.aliyuncs.com"
  ]
}
DOCKER

systemctl daemon-reload
systemctl restart docker

echo "✅ Docker 镜像源已配置为阿里云"
EOF
```

---

## 📋 完整的一键修复脚本

**执行这个脚本修复 Docker 镜像源并启动容器：**

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=========================================="
echo "Docker 镜像源修复和容器启动"
echo "=========================================="
echo ""

echo "=== 1. 配置 Docker 镜像源 ==="
mkdir -p /etc/docker

cat > /etc/docker/daemon.json << 'DOCKER'
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://registry.docker-cn.com",
    "https://mirror.baidubce.com"
  ]
}
DOCKER

echo "✅ Docker 配置文件已创建"
echo ""

echo "=== 2. 重启 Docker ==="
systemctl daemon-reload
systemctl restart docker
sleep 2

echo "✅ Docker 已重启"
echo ""

echo "=== 3. 验证 Docker 配置 ==="
docker info | grep -A 5 "Registry Mirrors"
echo ""

echo "=== 4. 克隆项目代码 ==="
cd /opt
if [ -d "worldcup-scout-pro" ]; then
    echo "项目已存在，跳过克隆"
else
    git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
fi
cd worldcup-scout-pro

echo "✅ 项目代码已准备"
echo ""

echo "=== 5. 创建 .env 文件 ==="
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
echo ""

echo "=== 6. 拉取 Docker 镜像 ==="
docker-compose pull

echo "✅ Docker 镜像已下载"
echo ""

echo "=== 7. 启动 Docker 容器 ==="
docker-compose up -d

echo "✅ Docker 容器已启动"
echo ""

echo "=== 8. 验证容器 ==="
docker-compose ps

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

## 🎯 如果上面的脚本还是失败

### 方案 C：手动指定镜像源

```bash
ssh root@111.228.15.109 << 'EOF'
# 直接使用国内镜像源拉取镜像
docker pull docker.mirrors.ustc.edu.cn/library/postgres:16-alpine
docker pull docker.mirrors.ustc.edu.cn/library/redis:7-alpine

# 重新标记镜像
docker tag docker.mirrors.ustc.edu.cn/library/postgres:16-alpine postgres:16-alpine
docker tag docker.mirrors.ustc.edu.cn/library/redis:7-alpine redis:7-alpine

# 启动容器
cd /opt/worldcup-scout-pro
docker-compose up -d
EOF
```

---

## 📝 验证修复

```bash
# 检查 Docker 镜像源配置
ssh root@111.228.15.109 'cat /etc/docker/daemon.json'

# 检查已下载的镜像
ssh root@111.228.15.109 'docker images'

# 检查容器状态
ssh root@111.228.15.109 'cd /opt/worldcup-scout-pro && docker-compose ps'

# 查看容器日志
ssh root@111.228.15.109 'cd /opt/worldcup-scout-pro && docker-compose logs'
```

---

## ✅ 修复后应该看到

```
CONTAINER ID   IMAGE                    COMMAND                  STATUS
abc123         postgres:16-alpine       "docker-entrypoint..."   Up 2 minutes
def456         redis:7-alpine           "redis-server"           Up 2 minutes
ghi789         worldcup-scout-pro:...   "npm start"              Up 2 minutes
```

---

## 🎯 立即行动

**执行这个命令修复 Docker 镜像源：**

```bash
ssh root@111.228.15.109 << 'EOF'
mkdir -p /etc/docker
cat > /etc/docker/daemon.json << 'DOCKER'
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://registry.docker-cn.com",
    "https://mirror.baidubce.com"
  ]
}
DOCKER
systemctl daemon-reload
systemctl restart docker
sleep 2
cd /opt/worldcup-scout-pro
docker-compose pull
docker-compose up -d
docker-compose ps
EOF
```

---

**立即执行这个修复脚本！** 🚀

**告诉我修复的结果！** 📝

**成功后你的网站就完全上线了！** 🎉

---

**编制时间：** 2026-03-15 00:32 GMT+8  
**状态：** 🔴 **立即修复**
