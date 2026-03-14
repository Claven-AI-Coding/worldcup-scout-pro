#!/bin/bash

# 世界杯球探 Pro - 完整修复脚本
# 执行时间：2026-03-14 22:42 GMT+8
# 用途：修复 Nginx 未安装问题

set -e  # 任何错误都会停止脚本

echo "=========================================="
echo "世界杯球探 Pro - 完整修复脚本"
echo "=========================================="
echo ""

# 第一步：安装 Nginx
echo "[1/8] 安装 Nginx..."
apt update
apt install -y nginx
echo "✅ Nginx 安装完成"
echo ""

# 第二步：启动 Nginx
echo "[2/8] 启动 Nginx..."
systemctl start nginx
systemctl enable nginx
echo "✅ Nginx 已启动并设置开机自启"
echo ""

# 第三步：创建 Nginx 配置
echo "[3/8] 创建 Nginx 配置文件..."
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

# 第四步：启用配置
echo "[4/8] 启用 Nginx 配置..."
ln -sf /etc/nginx/sites-available/worldcup-scout /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
echo "✅ Nginx 配置已启用"
echo ""

# 第五步：测试 Nginx 配置
echo "[5/8] 测试 Nginx 配置..."
if nginx -t; then
    echo "✅ Nginx 配置测试通过"
else
    echo "❌ Nginx 配置测试失败"
    exit 1
fi
echo ""

# 第六步：重启 Nginx
echo "[6/8] 重启 Nginx..."
systemctl restart nginx
echo "✅ Nginx 已重启"
echo ""

# 第七步：启动 Docker 容器
echo "[7/8] 启动 Docker 容器..."
cd /opt/worldcup-scout-pro
docker-compose up -d
echo "✅ Docker 容器已启动"
echo ""

# 第八步：验证服务
echo "[8/8] 验证服务状态..."
echo ""
echo "--- Nginx 状态 ---"
systemctl status nginx
echo ""
echo "--- Docker 容器 ---"
docker-compose ps
echo ""

echo "=========================================="
echo "✅ 修复完成！"
echo "=========================================="
echo ""
echo "接下来的步骤："
echo "1. 检查 DNS 配置（在你的电脑上执行）："
echo "   nslookup graysonwit.online"
echo ""
echo "2. 等待 DNS 生效（5-30 分钟）"
echo ""
echo "3. 访问网站："
echo "   https://graysonwit.online"
echo "   https://api.graysonwit.online"
echo ""
echo "=========================================="
