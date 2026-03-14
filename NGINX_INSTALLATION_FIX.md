# 🔧 部署失败根本原因 + 完整修复方案

**诊断时间：** 2026-03-14 22:38 GMT+8  
**根本原因：** Nginx 未被安装  
**状态：** 🔴 **立即修复**

---

## 🚨 根本原因分析

**错误信息：** `Unit nginx.service could not be found`

**含义：** Nginx 根本没有被安装到服务器上

**为什么会这样：**
- 部署脚本中的 Nginx 安装步骤未执行
- 或者安装失败但没有报错
- 导致 Web 服务器完全不存在

---

## 🚀 完整的修复方案

### 步骤 1：SSH 连接到服务器

```bash
ssh root@111.228.15.109
# 密码：7wldMUR/
```

### 步骤 2：安装 Nginx

```bash
# 更新包管理器
apt update

# 安装 Nginx
apt install -y nginx

# 启动 Nginx
systemctl start nginx

# 启用开机自启
systemctl enable nginx

# 验证安装
systemctl status nginx
```

### 步骤 3：创建 Nginx 配置文件

```bash
# 创建配置文件
cat > /etc/nginx/sites-available/worldcup-scout << 'EOF'
# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name graysonwit.online www.graysonwit.online api.graysonwit.online;
    return 301 https://$server_name$request_uri;
}

# 前端服务器
server {
    listen 443 ssl http2;
    server_name graysonwit.online www.graysonwit.online;

    ssl_certificate /etc/letsencrypt/live/graysonwit.online/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/graysonwit.online/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

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

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

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

# 删除默认配置
rm /etc/nginx/sites-enabled/default

# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx
```

### 步骤 4：验证 Docker 容器

```bash
# 进入项目目录
cd /opt/worldcup-scout-pro

# 检查容器状态
docker-compose ps

# 如果容器未运行，启动它们
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 步骤 5：验证所有服务

```bash
# 检查 Nginx
systemctl status nginx

# 检查 Docker
docker-compose ps

# 测试前端
curl -I http://localhost:3000

# 测试后端
curl -I http://localhost:8000

# 测试 Nginx
curl -I http://localhost
```

### 步骤 6：检查 DNS

```bash
# 在你的电脑上执行（不是服务器）
nslookup graysonwit.online
# 应该显示：111.228.15.109
```

---

## 📋 一键完整修复脚本

**复制并执行这个脚本：**

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 安装 Nginx ==="
apt update
apt install -y nginx

echo "=== 启动 Nginx ==="
systemctl start nginx
systemctl enable nginx

echo "=== 创建 Nginx 配置 ==="
cat > /etc/nginx/sites-available/worldcup-scout << 'NGINX'
server {
    listen 80;
    server_name graysonwit.online www.graysonwit.online api.graysonwit.online;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name graysonwit.online www.graysonwit.online;
    ssl_certificate /etc/letsencrypt/live/graysonwit.online/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/graysonwit.online/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 443 ssl http2;
    server_name api.graysonwit.online;
    ssl_certificate /etc/letsencrypt/live/graysonwit.online/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/graysonwit.online/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX

echo "=== 启用配置 ==="
ln -sf /etc/nginx/sites-available/worldcup-scout /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

echo "=== 测试 Nginx 配置 ==="
nginx -t

echo "=== 重启 Nginx ==="
systemctl restart nginx

echo "=== 启动 Docker 容器 ==="
cd /opt/worldcup-scout-pro
docker-compose up -d

echo "=== 验证服务 ==="
echo "Nginx 状态："
systemctl status nginx

echo "Docker 容器："
docker-compose ps

echo "=== 修复完成 ==="
EOF
```

---

## 🎯 你现在需要做的

### 立即执行：

1. **SSH 连接到服务器**
   ```bash
   ssh root@111.228.15.109
   ```

2. **复制并执行一键修复脚本**
   ```bash
   # 复制上面的脚本并执行
   ```

3. **等待脚本完成**
   - 应该看到 "修复完成" 的消息

4. **检查 DNS 配置**
   ```bash
   # 在你的电脑上执行
   nslookup graysonwit.online
   ```

5. **重新访问网站**
   ```
   https://graysonwit.online
   https://api.graysonwit.online
   ```

---

## ✅ 修复后应该看到的

**如果修复成功：**
- ✅ Nginx 已安装并运行
- ✅ Docker 容器已启动
- ✅ 前端可以访问
- ✅ 后端 API 可以访问
- ✅ SSL 证书有效

---

## 💡 为什么会这样

部署脚本中的 Nginx 安装步骤可能：
1. 未被执行
2. 执行失败但没有报错
3. 被跳过了

现在我们直接手动安装，确保 Nginx 被正确安装。

---

**立即执行这个修复脚本！** 🚀

**告诉我修复的结果！** 📝

**我们会立即解决！** 💪

---

**编制时间：** 2026-03-14 22:38 GMT+8  
**状态：** 🔴 **立即修复**
