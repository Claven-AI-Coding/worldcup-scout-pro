# 🔧 端口 80 被占用修复方案

**问题时间：** 2026-03-14 23:28 GMT+8  
**根本原因：** 端口 80 已被占用  
**错误信息：** `Could not bind TCP port 80 because it is already in use by another process`  
**状态：** 🔴 **立即修复**

---

## 🚨 问题分析

**Certbot 需要使用端口 80 来验证域名所有权，但端口 80 已被其他进程占用。**

可能的原因：
1. Nginx 已经在运行
2. Apache 或其他 Web 服务器在运行
3. 其他应用占用了端口 80

---

## 🚀 完整修复方案

### 步骤 1：找出占用端口 80 的进程

```bash
ssh root@111.228.15.109

# 查看占用端口 80 的进程
lsof -i :80

# 或者
netstat -tlnp | grep :80
```

### 步骤 2：停止占用端口 80 的进程

**如果是 Nginx：**
```bash
systemctl stop nginx
```

**如果是 Apache：**
```bash
systemctl stop apache2
```

**如果是其他进程，使用 kill 命令：**
```bash
# 查看进程 ID
ps aux | grep nginx
# 或
ps aux | grep apache

# 杀死进程（替换 PID）
kill -9 <PID>
```

### 步骤 3：生成 SSL 证书

```bash
certbot certonly --standalone \
  -d graysonwit.online \
  -d www.graysonwit.online \
  -d api.graysonwit.online \
  --agree-tos \
  --no-eff-email \
  -m admin@graysonwit.online \
  --non-interactive
```

### 步骤 4：启动 Nginx

```bash
systemctl start nginx
systemctl enable nginx
```

### 步骤 5：验证

```bash
# 检查 SSL 证书
ls -la /etc/letsencrypt/live/graysonwit.online/

# 检查 Nginx 状态
systemctl status nginx

# 测试 HTTPS
curl -I https://graysonwit.online
```

---

## 📋 一键完整修复脚本

**复制并执行这个脚本：**

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 停止占用端口 80 的进程 ==="
systemctl stop nginx 2>/dev/null || true
systemctl stop apache2 2>/dev/null || true

echo "=== 等待端口释放 ==="
sleep 2

echo "=== 生成 Let's Encrypt SSL 证书 ==="
certbot certonly --standalone \
  -d graysonwit.online \
  -d www.graysonwit.online \
  -d api.graysonwit.online \
  --agree-tos \
  --no-eff-email \
  -m admin@graysonwit.online \
  --non-interactive

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

echo "=== 配置自动续期 ==="
systemctl enable certbot.timer
systemctl start certbot.timer

echo "✅ 修复完成！"
EOF
```

---

## 🎯 快速修复（最简单的方式）

**一行命令：**

```bash
ssh root@111.228.15.109 'systemctl stop nginx; sleep 2; certbot certonly --standalone -d graysonwit.online -d www.graysonwit.online -d api.graysonwit.online --agree-tos --no-eff-email -m admin@graysonwit.online --non-interactive; systemctl start nginx'
```

---

## ✅ 修复后应该看到

```
✅ Nginx 已停止
✅ SSL 证书已生成
✅ Nginx 已启动
✅ Nginx 配置测试通过
✅ SSL 证书自动续期已配置
✅ 修复完成！
```

---

## 🔍 诊断命令

如果还有问题，执行这些诊断命令：

```bash
# 查看占用端口 80 的进程
lsof -i :80

# 查看占用端口 443 的进程
lsof -i :443

# 查看 Nginx 状态
systemctl status nginx

# 查看 SSL 证书
ls -la /etc/letsencrypt/live/graysonwit.online/

# 查看 Certbot 日志
tail -50 /var/log/letsencrypt/letsencrypt.log

# 测试 HTTPS
curl -I https://graysonwit.online
```

---

**立即执行这个修复脚本！** 🚀

**告诉我修复的结果！** 📝

**我们会立即解决！** 💪

---

**编制时间：** 2026-03-14 23:28 GMT+8  
**状态：** 🔴 **立即修复**
