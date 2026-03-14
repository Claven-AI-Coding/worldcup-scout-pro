# 🚀 直接从 GitHub 运行修复脚本

**问题：** `zsh: no such file or directory: fix-deployment-with-ssl.sh`  
**原因：** 脚本文件在你的电脑上不存在  
**解决方案：** 直接从 GitHub 运行脚本

---

## 🎯 最简单的方式

**直接执行这一行命令：**

```bash
ssh root@111.228.15.109 'curl -s https://raw.githubusercontent.com/Claven-AI-Coding/worldcup-scout-pro/main/fix-deployment-with-ssl.sh | bash'
```

**或者使用 wget：**

```bash
ssh root@111.228.15.109 'wget -qO- https://raw.githubusercontent.com/Claven-AI-Coding/worldcup-scout-pro/main/fix-deployment-with-ssl.sh | bash'
```

---

## 📋 如果上面的命令不工作

**方式 1：分步执行**

```bash
# 1. SSH 连接到服务器
ssh root@111.228.15.109

# 2. 在服务器上执行以下命令
curl -s https://raw.githubusercontent.com/Claven-AI-Coding/worldcup-scout-pro/main/fix-deployment-with-ssl.sh | bash
```

**方式 2：下载后再运行**

```bash
# 1. 在你的电脑上下载脚本
curl -O https://raw.githubusercontent.com/Claven-AI-Coding/worldcup-scout-pro/main/fix-deployment-with-ssl.sh

# 2. 上传到服务器
scp fix-deployment-with-ssl.sh root@111.228.15.109:/root/

# 3. SSH 连接并运行
ssh root@111.228.15.109
chmod +x /root/fix-deployment-with-ssl.sh
/root/fix-deployment-with-ssl.sh
```

**方式 3：手动执行脚本内容**

如果上面的方式都不工作，你可以手动执行脚本中的命令：

```bash
ssh root@111.228.15.109 << 'EOF'
# 安装 Certbot
apt update
apt install -y certbot python3-certbot-nginx

# 生成 SSL 证书
certbot certonly --standalone \
  -d graysonwit.online \
  -d www.graysonwit.online \
  -d api.graysonwit.online \
  --agree-tos \
  --no-eff-email \
  -m admin@graysonwit.online \
  --non-interactive

# 安装 Nginx
apt install -y nginx

# 启动 Nginx
systemctl start nginx
systemctl enable nginx

# 创建 Nginx 配置
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

# 启用配置
ln -sf /etc/nginx/sites-available/worldcup-scout /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx

# 配置自动续期
systemctl enable certbot.timer
systemctl start certbot.timer

echo "✅ 修复完成！"
EOF
```

---

## 🎯 推荐方式

**最简单的一行命令：**

```bash
ssh root@111.228.15.109 'curl -s https://raw.githubusercontent.com/Claven-AI-Coding/worldcup-scout-pro/main/fix-deployment-with-ssl.sh | bash'
```

**密码：** `7wldMUR/`

---

## ✅ 修复后应该看到

```
✅ Certbot 已安装
✅ SSL 证书已生成
✅ Nginx 已安装并运行
✅ Nginx 配置测试通过
✅ SSL 证书自动续期已配置
✅ 修复完成！
```

---

**立即执行这个命令！** 🚀

**告诉我修复的结果！** 📝

**我们会立即解决！** 💪

---

**编制时间：** 2026-03-14 23:25 GMT+8  
**状态：** 🔴 **立即修复**
