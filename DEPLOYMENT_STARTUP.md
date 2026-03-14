# 🚀 世界杯球探 Pro 部署启动指南

**启动时间：** 2026-03-14 19:21 GMT+8  
**部署人：** GraySon  
**项目：** worldcup-scout-pro  
**状态：** 🟢 准备启动

---

## ✅ 已确认的部署信息

### 服务器信息
```
提供商：京东云
公网 IP：111.228.15.109
SSH 用户：root
SSH 密码：7wldMUR/
SSH 端口：22
配置：4 核 CPU、8 GB 内存、180 GB SSD
```

### 域名信息
```
主域名：graysonwit.online
前端：www.graysonwit.online
后端 API：api.graysonwit.online
```

### API 密钥
```
Anthropic API Token：sk-AZSyhTmmPy6vXqU2ssfE3Cc0b8tsebpODp5QvP4CGsp7bVBO
Anthropic Base URL：https://luckycodecc.cn/claude
```

### SSL 证书
```
方案：Let's Encrypt（免费自动续期）
```

### 对象存储
```
服务商：腾讯云 COS
账号：grayson
```

---

## ⏳ 待补充的信息

### 1. 腾讯云 COS 密钥

**需要：**
```
SecretId：_________________
SecretKey：_________________
```

**获取方式：**
1. 登录：https://cloud.tencent.com/login/subAccount/100006695197?type=subAccount&username=grayson
2. 进入 API 密钥管理
3. 复制 SecretId 和 SecretKey

### 2. 数据库选择

```
[ ] 本地 PostgreSQL（推荐快速部署）
    - 安装在 111.228.15.109 服务器上
    - 优点：快速、便宜、简单
    - 缺点：占用服务器资源

[ ] 京东云数据库（推荐生产环境）
    - 使用京东云的数据库服务
    - 优点：专业管理、自动备份
    - 缺点：需要额外费用
```

### 3. Redis 选择

```
[ ] 本地 Redis（推荐快速部署）
    - 安装在 111.228.15.109 服务器上
    - 优点：快速、便宜、简单
    - 缺点：占用服务器资源

[ ] 京东云 Redis（推荐生产环境）
    - 使用京东云的 Redis 服务
    - 优点：专业管理、自动备份
    - 缺点：需要额外费用
```

---

## 🎯 部署流程（6 个阶段）

### 第一阶段：环境准备（30 分钟）

```bash
# 1. SSH 连接到服务器
ssh root@111.228.15.109 -p 22

# 2. 更新系统
apt update && apt upgrade -y

# 3. 安装基础工具
apt install -y curl wget git vim htop

# 4. 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 5. 安装 Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 6. 配置防火墙
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

### 第二阶段：数据库和缓存（20 分钟）

**如果选择本地方案：**

```bash
# 安装 PostgreSQL
apt install -y postgresql postgresql-contrib

# 安装 Redis
apt install -y redis-server

# 启动服务
systemctl start postgresql
systemctl start redis-server

# 创建数据库
sudo -u postgres createdb worldcup_scout
sudo -u postgres createuser worldcup_user
sudo -u postgres psql -c "ALTER USER worldcup_user WITH PASSWORD 'password123';"
```

**如果选择云服务方案：**

```
1. 在京东云控制台创建 PostgreSQL 实例
2. 在京东云控制台创建 Redis 实例
3. 获取连接信息
4. 配置安全组允许访问
```

### 第三阶段：SSL 证书（10 分钟）

```bash
# 安装 Certbot
apt install -y certbot python3-certbot-nginx

# 生成证书
certbot certonly --standalone \
  -d graysonwit.online \
  -d www.graysonwit.online \
  -d api.graysonwit.online

# 配置自动续期
systemctl enable certbot.timer
systemctl start certbot.timer
```

### 第四阶段：部署应用（30 分钟）

```bash
# 克隆代码
git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
cd worldcup-scout-pro

# 创建 .env 文件
cat > .env << EOF
# 数据库配置
DATABASE_URL=postgresql://worldcup_user:password123@localhost:5432/worldcup_scout

# Redis 配置
REDIS_URL=redis://localhost:6379

# API 密钥
ANTHROPIC_AUTH_TOKEN=sk-AZSyhTmmPy6vXqU2ssfE3Cc0b8tsebpODp5QvP4CGsp7bVBO
ANTHROPIC_BASE_URL=https://luckycodecc.cn/claude

# COS 配置
COS_SECRET_ID=your_secret_id
COS_SECRET_KEY=your_secret_key
COS_BUCKET=worldcup-scout-pro
COS_REGION=ap-beijing

# 应用配置
FRONTEND_URL=https://graysonwit.online
API_URL=https://api.graysonwit.online
EOF

# 构建 Docker 镜像
docker-compose build

# 启动应用
docker-compose up -d

# 验证部署
docker-compose ps
curl http://localhost:8000/health
```

### 第五阶段：配置 Nginx（15 分钟）

```bash
# 安装 Nginx
apt install -y nginx

# 创建配置文件
cat > /etc/nginx/sites-available/worldcup-scout << 'EOF'
# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name graysonwit.online www.graysonwit.online api.graysonwit.online;
    return 301 https://$server_name$request_uri;
}

# HTTPS 配置
server {
    listen 443 ssl http2;
    server_name graysonwit.online www.graysonwit.online;

    ssl_certificate /etc/letsencrypt/live/graysonwit.online/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/graysonwit.online/privkey.pem;

    # SSL 配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 前端
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# API 服务器
server {
    listen 443 ssl http2;
    server_name api.graysonwit.online;

    ssl_certificate /etc/letsencrypt/live/graysonwit.online/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/graysonwit.online/privkey.pem;

    # SSL 配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 后端 API
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/worldcup-scout /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# 测试配置
nginx -t

# 启动 Nginx
systemctl start nginx
systemctl enable nginx
```

### 第六阶段：配置 COS（15 分钟）

```bash
# 在应用中配置 COS 密钥
# 编辑 .env 文件
COS_SECRET_ID=your_secret_id
COS_SECRET_KEY=your_secret_key
COS_BUCKET=worldcup-scout-pro
COS_REGION=ap-beijing

# 重启应用
docker-compose restart
```

---

## ✅ 部署检查清单

**部署前：**
- [ ] 服务器 SSH 连接正常
- [ ] 域名 DNS 已配置
- [ ] 数据库方案已确认
- [ ] Redis 方案已确认
- [ ] API 密钥已获取
- [ ] COS 密钥已获取

**部署中：**
- [ ] 环境准备完成
- [ ] 数据库和缓存启动
- [ ] SSL 证书生成
- [ ] 应用启动成功
- [ ] Nginx 配置完成
- [ ] COS 连接正常

**部署后：**
- [ ] 前端可以访问（https://graysonwit.online）
- [ ] 后端 API 可以访问（https://api.graysonwit.online）
- [ ] 数据库连接正常
- [ ] Redis 缓存正常
- [ ] 文件上传到 COS 正常
- [ ] 监控告警已配置

---

## 🎯 立即行动

**请提供最后的信息：**

```
1. 腾讯云 COS 密钥：
   - SecretId：_________________
   - SecretKey：_________________

2. 数据库选择：
   [ ] 本地 PostgreSQL
   [ ] 京东云数据库

3. Redis 选择：
   [ ] 本地 Redis
   [ ] 京东云 Redis
```

**或者直接说：**
```
"按照本地方案部署，COS 密钥是 [SecretId] 和 [SecretKey]"
```

---

**所有信息已确认！** ✅

**等待最后的确认！** 📝

**准备立即开始部署！** 🚀

---

**编制时间：** 2026-03-14 19:21 GMT+8  
**状态：** 🟢 准备启动
