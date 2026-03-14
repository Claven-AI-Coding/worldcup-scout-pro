#!/bin/bash

# 世界杯球探 Pro - 完整修复脚本（包含 SSL 证书）
# 执行时间：2026-03-14 22:57 GMT+8
# 用途：修复 Nginx 和 SSL 证书问题

set -e  # 任何错误都会停止脚本

echo "=========================================="
echo "世界杯球探 Pro - 完整修复脚本（含 SSL）"
echo "=========================================="
echo ""

# 第一步：安装 Certbot
echo "[1/9] 安装 Certbot..."
apt update
apt install -y certbot python3-certbot-nginx
echo "✅ Certbot 安装完成"
echo ""

# 第二步：生成 SSL 证书
echo "[2/9] 生成 Let's Encrypt SSL 证书..."
certbot certonly --standalone \
  -d graysonwit.online \
  -d www.graysonwit.online \
  -d api.graysonwit.online \
  --agree-tos \
  --no-eff-email \
  -m admin@graysonwit.online \
  --non-interactive
echo "✅ SSL 证书已生成"
echo ""

# 第三步：安装 Nginx
echo "[3/9] 安装 Nginx..."
apt install -y nginx
echo "✅ Nginx 安装完成"
echo ""

# 第四步：启动 Nginx
echo "[4/9] 启动 Nginx..."
systemctl start nginx
systemctl enable nginx
echo "✅ Nginx 已启动并设置开机自启"
echo ""

# 第五步：创建 Nginx 配置
echo "[5/9] 创建 Nginx 配置文件..."
cat > /etc/nginx/sites-available/worldcup-scout << 'NGINX_CONFIG'
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
NGINX_CONFIG
echo "✅ Nginx 配置文件已创建"
echo ""

# 第六步：启用配置
echo "[6/9] 启用 Nginx 配置..."
ln -sf /etc/nginx/sites-available/worldcup-scout /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
echo "✅ Nginx 配置已启用"
echo ""

# 第七步：测试 Nginx 配置
echo "[7/9] 测试 Nginx 配置..."
if nginx -t; then
    echo "✅ Nginx 配置测试通过"
else
    echo "❌ Nginx 配置测试失败"
    exit 1
fi
echo ""

# 第八步：重启 Nginx
echo "[8/9] 重启 Nginx..."
systemctl restart nginx
echo "✅ Nginx 已重启"
echo ""

# 第九步：配置自动续期
echo "[9/9] 配置 SSL 证书自动续期..."
systemctl enable certbot.timer
systemctl start certbot.timer
echo "✅ SSL 证书自动续期已配置"
echo ""

echo "=========================================="
echo "✅ 修复完成！"
echo "=========================================="
echo ""
echo "验证步骤："
echo "1. 检查 SSL 证书："
echo "   ls -la /etc/letsencrypt/live/graysonwit.online/"
echo ""
echo "2. 检查 Nginx 状态："
echo "   systemctl status nginx"
echo ""
echo "3. 测试 HTTPS 连接："
echo "   curl -I https://graysonwit.online"
echo ""
echo "4. 访问网站："
echo "   https://graysonwit.online"
echo "   https://api.graysonwit.online"
echo ""
echo "=========================================="
