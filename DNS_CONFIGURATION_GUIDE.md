# 🌐 DNS 配置完整指南

**问题时间：** 2026-03-14 23:33 GMT+8  
**根本原因：** DNS 记录未配置  
**错误信息：** `DNS problem: NXDOMAIN looking up A for graysonwit.online`  
**状态：** 🔴 **立即配置 DNS**

---

## 🚨 问题分析

**Certbot 无法验证域名所有权，因为 DNS 记录未指向你的服务器。**

错误详情：
- `graysonwit.online` - 无有效 A 记录
- `www.graysonwit.online` - DNS 问题
- `api.graysonwit.online` - DNS 问题

---

## 🎯 DNS 配置步骤

### 步骤 1：登录你的域名注册商

你的域名是 `graysonwit.online`，需要找到域名注册商的 DNS 管理界面。

**常见的域名注册商：**
- 阿里云（aliyun.com）
- 腾讯云（cloud.tencent.com）
- 西部数码（west.cn）
- GoDaddy（godaddy.com）
- Namecheap（namecheap.com）

### 步骤 2：找到 DNS 管理界面

1. 登录你的域名注册商账户
2. 找到"域名管理"或"DNS 管理"
3. 选择 `graysonwit.online` 域名
4. 点击"DNS 设置"或"解析设置"

### 步骤 3：添加 DNS 记录

**需要添加以下 3 条 A 记录：**

| 主机名 | 记录类型 | 记录值 | TTL |
|--------|---------|--------|-----|
| graysonwit.online | A | 111.228.15.109 | 600 |
| www | A | 111.228.15.109 | 600 |
| api | A | 111.228.15.109 | 600 |

**或者用另一种表示方式：**

```
记录 1：
  主机名：@ 或 graysonwit.online
  类型：A
  值：111.228.15.109
  TTL：600

记录 2：
  主机名：www
  类型：A
  值：111.228.15.109
  TTL：600

记录 3：
  主机名：api
  类型：A
  值：111.228.15.109
  TTL：600
```

### 步骤 4：保存并等待 DNS 生效

1. 点击"保存"或"确认"
2. 等待 DNS 生效（通常 5-30 分钟，有时需要 24 小时）

### 步骤 5：验证 DNS 配置

在你的电脑上执行以下命令验证：

```bash
# 检查 graysonwit.online
nslookup graysonwit.online
# 应该显示：111.228.15.109

# 检查 www.graysonwit.online
nslookup www.graysonwit.online
# 应该显示：111.228.15.109

# 检查 api.graysonwit.online
nslookup api.graysonwit.online
# 应该显示：111.228.15.109

# 或使用 dig
dig graysonwit.online
dig www.graysonwit.online
dig api.graysonwit.online
```

---

## 📝 DNS 配置示例

### 示例 1：阿里云

1. 登录阿里云控制台
2. 进入"域名"
3. 选择 `graysonwit.online`
4. 点击"解析"
5. 添加记录：
   - 记录类型：A
   - 主机记录：@ 或 graysonwit.online
   - 记录值：111.228.15.109
   - TTL：600
6. 重复添加 www 和 api 的记录

### 示例 2：腾讯云

1. 登录腾讯云控制台
2. 进入"域名注册"
3. 选择 `graysonwit.online`
4. 点击"DNS 解析"
5. 添加记录（同上）

### 示例 3：GoDaddy

1. 登录 GoDaddy
2. 进入"My Products"
3. 选择 `graysonwit.online`
4. 点击"DNS"
5. 添加 A 记录（同上）

---

## 🔍 DNS 配置检查清单

```
[ ] 1. 登录域名注册商
[ ] 2. 找到 DNS 管理界面
[ ] 3. 添加 graysonwit.online A 记录 → 111.228.15.109
[ ] 4. 添加 www A 记录 → 111.228.15.109
[ ] 5. 添加 api A 记录 → 111.228.15.109
[ ] 6. 保存所有记录
[ ] 7. 等待 DNS 生效（5-30 分钟）
[ ] 8. 验证 DNS 配置（nslookup）
```

---

## ✅ DNS 配置完成后

**DNS 生效后，执行以下命令重新生成 SSL 证书：**

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 生成 Let's Encrypt SSL 证书 ==="
certbot certonly --standalone \
  -d graysonwit.online \
  -d www.graysonwit.online \
  -d api.graysonwit.online \
  --agree-tos \
  --no-eff-email \
  -m admin@graysonwit.online \
  --non-interactive

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

echo "=== 启动 Nginx ==="
systemctl start nginx
systemctl enable nginx

echo "=== 配置自动续期 ==="
systemctl enable certbot.timer
systemctl start certbot.timer

echo "✅ 修复完成！"
EOF
```

---

## 🎯 立即行动

**你现在需要做的：**

1. **登录你的域名注册商**
   - 找到 DNS 管理界面

2. **添加 3 条 A 记录**
   - graysonwit.online → 111.228.15.109
   - www → 111.228.15.109
   - api → 111.228.15.109

3. **保存并等待 DNS 生效**
   - 通常 5-30 分钟

4. **验证 DNS 配置**
   ```bash
   nslookup graysonwit.online
   ```

5. **DNS 生效后，告诉我**
   - 我会帮你生成 SSL 证书

---

**立即配置 DNS！** 🌐

**告诉我 DNS 配置完成！** 📝

**我们会立即生成 SSL 证书！** 💪

---

**编制时间：** 2026-03-14 23:33 GMT+8  
**状态：** 🔴 **等待 DNS 配置**
