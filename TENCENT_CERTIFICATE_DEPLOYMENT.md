# 🚀 腾讯云证书部署指南（bundle.crt 版本）

**证书文件：** graysonwit.online_bundle.crt  
**私钥文件：** graysonwit.online.key  
**时间：** 2026-03-15 00:15 GMT+8

---

## 📋 文件说明

- **graysonwit.online_bundle.crt** - 完整的证书链（包含根证书和中间证书）
- **graysonwit.online.key** - 私钥文件

这个组合完全可以用于 Nginx！

---

## 🚀 快速部署步骤

### 步骤 1：创建证书目录

```bash
ssh root@111.228.15.109 'mkdir -p /etc/letsencrypt/live/graysonwit.online'
```

### 步骤 2：上传证书文件

```bash
# 上传证书链
scp graysonwit.online_bundle.crt root@111.228.15.109:/etc/letsencrypt/live/graysonwit.online/fullchain.pem

# 上传私钥
scp graysonwit.online.key root@111.228.15.109:/etc/letsencrypt/live/graysonwit.online/privkey.pem
```

### 步骤 3：设置权限

```bash
ssh root@111.228.15.109 << 'EOF'
chmod 644 /etc/letsencrypt/live/graysonwit.online/fullchain.pem
chmod 600 /etc/letsencrypt/live/graysonwit.online/privkey.pem
EOF
```

### 步骤 4：一键部署（Nginx + Docker）

```bash
ssh root@111.228.15.109 << 'EOF'
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

echo "=== 启用 Nginx 配置 ==="
ln -sf /etc/nginx/sites-available/worldcup-scout /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

echo "=== 测试 Nginx 配置 ==="
nginx -t

echo "=== 启动 Nginx ==="
systemctl start nginx
systemctl enable nginx

echo "=== 启动 Docker 容器 ==="
cd /opt/worldcup-scout-pro
docker-compose up -d

echo "=== 验证服务 ==="
echo "Nginx 状态："
systemctl status nginx

echo ""
echo "Docker 容器："
docker-compose ps

echo ""
echo "✅ 部署完成！"
echo ""
echo "访问网站："
echo "  前端：https://graysonwit.online"
echo "  后端 API：https://api.graysonwit.online"
EOF
```

---

## ✅ 验证部署

```bash
# 测试 HTTPS
curl -I https://graysonwit.online

# 查看证书信息
openssl s_client -connect graysonwit.online:443 -servername graysonwit.online
```

---

## 🎯 完整的一行命令

如果你想快速执行所有步骤：

```bash
ssh root@111.228.15.109 'mkdir -p /etc/letsencrypt/live/graysonwit.online' && \
scp graysonwit.online_bundle.crt root@111.228.15.109:/etc/letsencrypt/live/graysonwit.online/fullchain.pem && \
scp graysonwit.online.key root@111.228.15.109:/etc/letsencrypt/live/graysonwit.online/privkey.pem && \
ssh root@111.228.15.109 << 'DEPLOY'
chmod 644 /etc/letsencrypt/live/graysonwit.online/fullchain.pem
chmod 600 /etc/letsencrypt/live/graysonwit.online/privkey.pem

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

ln -sf /etc/nginx/sites-available/worldcup-scout /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl start nginx
systemctl enable nginx

cd /opt/worldcup-scout-pro
docker-compose up -d

echo "✅ 部署完成！"
DEPLOY
```

---

## 📝 部署后检查

```bash
# 1. 检查证书文件
ssh root@111.228.15.109 'ls -la /etc/letsencrypt/live/graysonwit.online/'

# 2. 检查 Nginx 状态
ssh root@111.228.15.109 'systemctl status nginx'

# 3. 检查 Docker 容器
ssh root@111.228.15.109 'cd /opt/worldcup-scout-pro && docker-compose ps'

# 4. 测试 HTTPS
curl -I https://graysonwit.online
```

---

**现在就执行部署！** 🚀

**告诉我部署的结果！** 📝

**成功后你的网站就上线了！** 🎉
