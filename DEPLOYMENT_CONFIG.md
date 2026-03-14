# 🚀 世界杯球探 Pro 部署配置

**部署日期：** 2026-03-14  
**部署人：** GraySon  
**项目：** worldcup-scout-pro

---

## 📋 已收集的部署信息

### 1. 服务器信息 ✅

```
服务器提供商：京东云
服务器类型：通用型 SSD
CPU：4 核
内存：8 GB
磁盘：180 GB
流量包：500 GB/月
带宽上限：5 Mbps

SSH 访问信息：
  - 用户名：root
  - 密码：7wldMUR/
  - 端口：22
  - IP：[待确认]
```

### 2. 域名信息 ✅

```
主域名：graysonwit.online
前端域名：www.graysonwit.online（或 graysonwit.online）
后端 API 域名：api.graysonwit.online
```

### 3. 对象存储 ✅

```
服务商：腾讯云 COS
已购买资源包
控制台：https://console.cloud.tencent.com
```

---

## 📝 需要你补充的信息

### 1. 服务器 IP 地址

```
公网 IP：_________________ （必需）
内网 IP：_________________ （可选）
```

### 2. SSL 证书

```
选择方案：
  [ ] Let's Encrypt（免费，自动续期）- 推荐
  [ ] 付费证书
  [ ] 自签名证书

如已有证书：
  - 证书文件路径：_________________
  - 私钥文件路径：_________________
```

### 3. 数据库

```
选择方案：
  [ ] 在服务器上安装 PostgreSQL
  [ ] 使用京东云数据库服务
  [ ] 使用其他云数据库

如选择云数据库：
  - 数据库主机：_________________
  - 数据库端口：_________________
  - 数据库名：_________________
  - 用户名：_________________
  - 密码：_________________
```

### 4. Redis 缓存

```
选择方案：
  [ ] 在服务器上安装 Redis
  [ ] 使用京东云 Redis 服务
  [ ] 使用其他云 Redis

如选择云 Redis：
  - Redis 主机：_________________
  - Redis 端口：_________________
  - Redis 密码：_________________
```

### 5. API 密钥

```
Anthropic API Key：_________________
Google API Key（可选）：_________________
腾讯云 COS 密钥：
  - SecretId：_________________
  - SecretKey：_________________
```

### 6. 邮件服务（可选）

```
是否需要邮件功能：[ ] 是  [ ] 否

如需要：
  - SMTP 服务器：_________________
  - SMTP 端口：_________________
  - 邮箱账号：_________________
  - 邮箱密码：_________________
```

---

## 🎯 部署计划

### 第一阶段：环境准备（今天）

**Claven 的行动：**

1. ✅ 连接到服务器
   ```bash
   ssh root@[IP] -p 22
   密码：7wldMUR/
   ```

2. ✅ 更新系统
   ```bash
   apt update && apt upgrade -y
   ```

3. ✅ 安装基础工具
   ```bash
   apt install -y curl wget git vim htop
   ```

4. ✅ 安装 Docker
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

5. ✅ 安装 Docker Compose
   ```bash
   curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   chmod +x /usr/local/bin/docker-compose
   ```

6. ✅ 配置防火墙
   ```bash
   ufw allow 22/tcp
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw enable
   ```

### 第二阶段：数据库和缓存（今天）

**根据你的选择：**

**选项 A：本地安装（推荐用于小规模）**
```bash
# 安装 PostgreSQL
apt install -y postgresql postgresql-contrib

# 安装 Redis
apt install -y redis-server
```

**选项 B：云服务（推荐用于生产）**
- 在京东云控制台创建 PostgreSQL 实例
- 在京东云控制台创建 Redis 实例
- 获取连接信息

### 第三阶段：SSL 证书（今天）

**推荐方案：Let's Encrypt**
```bash
apt install -y certbot python3-certbot-nginx

certbot certonly --standalone \
  -d graysonwit.online \
  -d www.graysonwit.online \
  -d api.graysonwit.online
```

### 第四阶段：部署应用（明天）

1. 克隆代码
   ```bash
   git clone https://github.com/Claven-AI-Coding/worldcup-scout-pro.git
   cd worldcup-scout-pro
   ```

2. 配置环境变量
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入数据库、Redis、API 密钥等信息
   ```

3. 构建 Docker 镜像
   ```bash
   docker-compose build
   ```

4. 启动应用
   ```bash
   docker-compose up -d
   ```

5. 验证部署
   ```bash
   docker-compose ps
   curl http://localhost:8000/health
   ```

### 第五阶段：配置 Nginx（明天）

```nginx
server {
    listen 443 ssl http2;
    server_name graysonwit.online www.graysonwit.online;

    ssl_certificate /etc/letsencrypt/live/graysonwit.online/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/graysonwit.online/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;
    server_name graysonwit.online www.graysonwit.online;
    return 301 https://$server_name$request_uri;
}
```

### 第六阶段：配置 COS（明天）

**腾讯云 COS 配置：**

1. 在 COS 控制台创建 Bucket
   ```
   Bucket 名称：worldcup-scout-pro
   地域：选择离用户最近的地域
   ```

2. 获取 SecretId 和 SecretKey
   ```
   在 https://console.cloud.tencent.com 获取
   ```

3. 配置应用
   ```
   在 .env 中配置：
   COS_SECRET_ID=your_secret_id
   COS_SECRET_KEY=your_secret_key
   COS_BUCKET=worldcup-scout-pro
   COS_REGION=ap-beijing（或其他地域）
   ```

---

## 📊 部署时间表

| 阶段 | 任务 | 预计时间 | 状态 |
|------|------|---------|------|
| 1 | 环境准备 | 30 分钟 | ⏳ 待开始 |
| 2 | 数据库和缓存 | 20 分钟 | ⏳ 待开始 |
| 3 | SSL 证书 | 10 分钟 | ⏳ 待开始 |
| 4 | 部署应用 | 30 分钟 | ⏳ 待开始 |
| 5 | 配置 Nginx | 15 分钟 | ⏳ 待开始 |
| 6 | 配置 COS | 15 分钟 | ⏳ 待开始 |

**总计：约 2 小时**

---

## 🎯 立即需要你做的

### 第一步：提供缺失的信息

请回复以下信息：

```
1. 服务器公网 IP：_________________

2. 数据库选择：
   [ ] 本地 PostgreSQL
   [ ] 京东云数据库
   [ ] 其他

3. Redis 选择：
   [ ] 本地 Redis
   [ ] 京东云 Redis
   [ ] 其他

4. SSL 证书：
   [ ] Let's Encrypt（推荐）
   [ ] 已有证书

5. Anthropic API Key：_________________

6. 腾讯云 COS 密钥：
   - SecretId：_________________
   - SecretKey：_________________
```

### 第二步：确认部署时间

```
何时开始部署：
  [ ] 立即开始
  [ ] 明天开始
  [ ] 其他时间：_________________
```

---

## ✅ 部署检查清单

**部署前检查：**
- [ ] 服务器 SSH 连接正常
- [ ] 域名 DNS 已配置
- [ ] 数据库已创建
- [ ] Redis 已启动
- [ ] API 密钥已获取
- [ ] SSL 证书已准备

**部署后检查：**
- [ ] 前端可以访问
- [ ] 后端 API 可以访问
- [ ] 数据库连接正常
- [ ] Redis 缓存正常
- [ ] 文件上传到 COS 正常
- [ ] 监控告警已配置

---

**准备好开始部署了！** 🚀

**请提供缺失的信息！** 📝

**我会立即执行部署！** 💪

---

**编制时间：** 2026-03-14 18:24 GMT+8  
**状态：** 🟡 等待信息补充
