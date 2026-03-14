# 🔍 Nginx 和 SSL 证书状态检查指南

**时间：** 2026-03-15 00:29 GMT+8  
**用途：** 验证 Nginx 和 SSL 证书是否正常运行

---

## 🎯 Nginx 状态检查

### 1. 检查 Nginx 是否运行

```bash
ssh root@111.228.15.109 'systemctl status nginx'
```

**应该看到：**
```
● nginx.service - A high performance web server and a reverse proxy server
   Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
   Active: active (running) since ...
```

### 2. 检查 Nginx 配置是否正确

```bash
ssh root@111.228.15.109 'nginx -t'
```

**应该看到：**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 3. 查看 Nginx 监听的端口

```bash
ssh root@111.228.15.109 'netstat -tlnp | grep nginx'
```

**应该看到：**
```
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      1234/nginx: master
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      1234/nginx: master
```

### 4. 查看 Nginx 配置文件

```bash
ssh root@111.228.15.109 'cat /etc/nginx/sites-enabled/worldcup-scout'
```

### 5. 查看 Nginx 错误日志

```bash
ssh root@111.228.15.109 'tail -50 /var/log/nginx/error.log'
```

### 6. 查看 Nginx 访问日志

```bash
ssh root@111.228.15.109 'tail -50 /var/log/nginx/access.log'
```

---

## 🔐 SSL 证书状态检查

### 1. 检查证书文件是否存在

```bash
ssh root@111.228.15.109 'ls -la /etc/letsencrypt/live/graysonwit.online/'
```

**应该看到：**
```
total 12
drwxr-xr-x 2 root root 4096 Mar 15 00:15 .
drwxr-xr-x 3 root root 4096 Mar 15 00:15 ..
-rw-r--r-- 1 root root 1234 Mar 15 00:15 fullchain.pem
-rw------- 1 root root 5678 Mar 15 00:15 privkey.pem
```

### 2. 查看证书详细信息

```bash
ssh root@111.228.15.109 'openssl x509 -in /etc/letsencrypt/live/graysonwit.online/fullchain.pem -text -noout'
```

**关键信息：**
- Subject: CN=graysonwit.online
- Issuer: CN=TrustAsia TLS RSA CA
- Not Before: 日期
- Not After: 日期（证书过期时间）

### 3. 查看证书过期时间

```bash
ssh root@111.228.15.109 'openssl x509 -in /etc/letsencrypt/live/graysonwit.online/fullchain.pem -noout -dates'
```

**应该看到：**
```
notBefore=Mar 15 00:00:00 2026 GMT
notAfter=Mar 15 00:00:00 2027 GMT
```

### 4. 查看证书包含的域名

```bash
ssh root@111.228.15.109 'openssl x509 -in /etc/letsencrypt/live/graysonwit.online/fullchain.pem -noout -text | grep -A1 "Subject Alternative Name"'
```

**应该看到：**
```
X509v3 Subject Alternative Name:
    DNS:graysonwit.online, DNS:www.graysonwit.online, DNS:api.graysonwit.online
```

### 5. 验证证书和私钥是否匹配

```bash
# 获取证书的模数
ssh root@111.228.15.109 'openssl x509 -noout -modulus -in /etc/letsencrypt/live/graysonwit.online/fullchain.pem | openssl md5'

# 获取私钥的模数
ssh root@111.228.15.109 'openssl rsa -noout -modulus -in /etc/letsencrypt/live/graysonwit.online/privkey.pem | openssl md5'
```

**如果两个 MD5 值相同，说明证书和私钥匹配。**

---

## 🌐 HTTPS 连接测试

### 1. 测试 HTTPS 连接

```bash
# 测试前端
curl -I https://graysonwit.online

# 测试后端 API
curl -I https://api.graysonwit.online
```

**应该看到：**
```
HTTP/2 200
server: nginx/1.18.0
```

### 2. 查看 SSL 握手信息

```bash
ssh root@111.228.15.109 'openssl s_client -connect graysonwit.online:443 -servername graysonwit.online'
```

**应该看到：**
```
subject=CN = graysonwit.online
issuer=C = CN, O = TrustAsia, CN = TrustAsia TLS RSA CA
```

### 3. 检查证书链

```bash
ssh root@111.228.15.109 'openssl s_client -connect graysonwit.online:443 -servername graysonwit.online -showcerts'
```

---

## 📋 完整的状态检查脚本

**一键检查所有状态：**

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=========================================="
echo "Nginx 和 SSL 证书状态检查"
echo "=========================================="
echo ""

echo "=== 1. Nginx 运行状态 ==="
systemctl status nginx
echo ""

echo "=== 2. Nginx 配置测试 ==="
nginx -t
echo ""

echo "=== 3. Nginx 监听端口 ==="
netstat -tlnp | grep nginx
echo ""

echo "=== 4. SSL 证书文件 ==="
ls -la /etc/letsencrypt/live/graysonwit.online/
echo ""

echo "=== 5. 证书过期时间 ==="
openssl x509 -in /etc/letsencrypt/live/graysonwit.online/fullchain.pem -noout -dates
echo ""

echo "=== 6. 证书包含的域名 ==="
openssl x509 -in /etc/letsencrypt/live/graysonwit.online/fullchain.pem -noout -text | grep -A1 "Subject Alternative Name"
echo ""

echo "=== 7. 证书和私钥匹配检查 ==="
echo "证书 MD5:"
openssl x509 -noout -modulus -in /etc/letsencrypt/live/graysonwit.online/fullchain.pem | openssl md5
echo "私钥 MD5:"
openssl rsa -noout -modulus -in /etc/letsencrypt/live/graysonwit.online/privkey.pem | openssl md5
echo ""

echo "=== 8. HTTPS 连接测试 ==="
echo "前端："
curl -I https://graysonwit.online
echo ""
echo "后端 API："
curl -I https://api.graysonwit.online
echo ""

echo "=========================================="
echo "✅ 状态检查完成！"
echo "=========================================="
EOF
```

---

## ✅ 正常状态应该看到

| 项目 | 正常状态 |
|------|---------|
| Nginx 状态 | Active: active (running) |
| Nginx 配置 | syntax is ok, test is successful |
| 端口监听 | 0.0.0.0:80 和 0.0.0.0:443 |
| 证书文件 | fullchain.pem 和 privkey.pem 存在 |
| 证书过期 | notAfter 日期在未来 |
| 域名覆盖 | 包含 graysonwit.online, www, api |
| 证书和私钥 | MD5 值相同 |
| HTTPS 连接 | HTTP/2 200 |

---

## 🔧 常见问题排查

### 问题 1：Nginx 未运行

```bash
# 启动 Nginx
ssh root@111.228.15.109 'systemctl start nginx'

# 启用开机自启
ssh root@111.228.15.109 'systemctl enable nginx'
```

### 问题 2：证书文件不存在

```bash
# 检查证书目录
ssh root@111.228.15.109 'ls -la /etc/letsencrypt/live/'

# 如果目录不存在，需要重新上传证书
```

### 问题 3：证书已过期

```bash
# 查看过期时间
ssh root@111.228.15.109 'openssl x509 -in /etc/letsencrypt/live/graysonwit.online/fullchain.pem -noout -dates'

# 如果已过期，需要申请新证书
```

### 问题 4：HTTPS 连接失败

```bash
# 查看 Nginx 错误日志
ssh root@111.228.15.109 'tail -100 /var/log/nginx/error.log'

# 测试 SSL 握手
openssl s_client -connect graysonwit.online:443 -servername graysonwit.online
```

---

**立即执行状态检查脚本！** 🔍

**告诉我检查的结果！** 📝

**一切正常后就可以启动 Docker 容器了！** 🚀
