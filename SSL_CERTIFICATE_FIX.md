# 🔧 SSL 证书缺失修复方案

**问题时间：** 2026-03-14 22:57 GMT+8  
**根本原因：** Let's Encrypt SSL 证书未生成  
**错误信息：** `No such file or directory: /etc/letsencrypt/live/graysonwit.online/fullchain.pem`  
**状态：** 🔴 **立即修复**

---

## 🚨 问题分析

**Nginx 配置中引用了 SSL 证书，但证书文件不存在。**

原因：
1. Certbot 未安装
2. 或者 Certbot 安装了但证书生成失败
3. 或者证书生成过程被跳过了

---

## 🚀 完整修复方案

### 方案 A：生成 Let's Encrypt 证书（推荐）

**步骤 1：安装 Certbot**

```bash
ssh root@111.228.15.109
apt update
apt install -y certbot python3-certbot-nginx
```

**步骤 2：生成证书**

```bash
# 使用 standalone 模式生成证书
certbot certonly --standalone \
  -d graysonwit.online \
  -d www.graysonwit.online \
  -d api.graysonwit.online \
  --agree-tos \
  --no-eff-email \
  -m admin@graysonwit.online
```

**步骤 3：配置自动续期**

```bash
systemctl enable certbot.timer
systemctl start certbot.timer
```

**步骤 4：重新测试 Nginx 配置**

```bash
nginx -t
systemctl restart nginx
```

---

### 方案 B：临时使用自签名证书（快速测试）

如果你想快速测试，可以先用自签名证书：

**步骤 1：生成自签名证书**

```bash
mkdir -p /etc/letsencrypt/live/graysonwit.online

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/letsencrypt/live/graysonwit.online/privkey.pem \
  -out /etc/letsencrypt/live/graysonwit.online/fullchain.pem \
  -subj "/C=CN/ST=Shanghai/L=Shanghai/O=WorldCup/CN=graysonwit.online"
```

**步骤 2：测试 Nginx 配置**

```bash
nginx -t
systemctl restart nginx
```

**步骤 3：稍后替换为真实证书**

```bash
# 生成真实的 Let's Encrypt 证书
certbot certonly --standalone \
  -d graysonwit.online \
  -d www.graysonwit.online \
  -d api.graysonwit.online
```

---

## 📋 一键完整修复脚本

**复制并执行这个脚本：**

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== 安装 Certbot ==="
apt update
apt install -y certbot python3-certbot-nginx

echo "=== 生成 Let's Encrypt 证书 ==="
certbot certonly --standalone \
  -d graysonwit.online \
  -d www.graysonwit.online \
  -d api.graysonwit.online \
  --agree-tos \
  --no-eff-email \
  -m admin@graysonwit.online

echo "=== 配置自动续期 ==="
systemctl enable certbot.timer
systemctl start certbot.timer

echo "=== 测试 Nginx 配置 ==="
nginx -t

echo "=== 重启 Nginx ==="
systemctl restart nginx

echo "=== 验证证书 ==="
ls -la /etc/letsencrypt/live/graysonwit.online/

echo "=== 修复完成 ==="
EOF
```

---

## 🎯 快速修复（最简单的方式）

**一行命令：**

```bash
ssh root@111.228.15.109 'apt update && apt install -y certbot python3-certbot-nginx && certbot certonly --standalone -d graysonwit.online -d www.graysonwit.online -d api.graysonwit.online --agree-tos --no-eff-email -m admin@graysonwit.online && nginx -t && systemctl restart nginx'
```

---

## ✅ 修复后应该看到

```
✅ Certbot 已安装
✅ SSL 证书已生成
✅ 证书文件存在：/etc/letsencrypt/live/graysonwit.online/fullchain.pem
✅ Nginx 配置测试通过
✅ Nginx 已重启
```

---

## 🔍 验证证书

修复后，执行以下命令验证：

```bash
# 查看证书文件
ls -la /etc/letsencrypt/live/graysonwit.online/

# 查看证书信息
openssl x509 -in /etc/letsencrypt/live/graysonwit.online/fullchain.pem -text -noout

# 查看证书过期时间
openssl x509 -in /etc/letsencrypt/live/graysonwit.online/fullchain.pem -noout -dates

# 测试 HTTPS 连接
curl -I https://graysonwit.online
```

---

## 📝 修复步骤总结

1. **安装 Certbot**
   ```bash
   apt install -y certbot python3-certbot-nginx
   ```

2. **生成证书**
   ```bash
   certbot certonly --standalone -d graysonwit.online -d www.graysonwit.online -d api.graysonwit.online
   ```

3. **配置自动续期**
   ```bash
   systemctl enable certbot.timer
   systemctl start certbot.timer
   ```

4. **重启 Nginx**
   ```bash
   nginx -t
   systemctl restart nginx
   ```

5. **验证**
   ```bash
   curl -I https://graysonwit.online
   ```

---

## 💡 为什么会这样

部署脚本中的 SSL 证书生成步骤可能：
1. 未被执行
2. 执行失败但没有报错
3. 被跳过了

现在我们直接手动生成证书，确保 SSL 证书被正确创建。

---

**立即执行这个修复脚本！** 🚀

**告诉我修复的结果！** 📝

**我们会立即解决！** 💪

---

**编制时间：** 2026-03-14 22:57 GMT+8  
**状态：** 🔴 **立即修复**
