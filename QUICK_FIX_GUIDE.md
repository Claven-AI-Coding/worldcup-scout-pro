# 🚨 快速修复指南 - "无法访问此网站"

**问题：** 显示"无法访问此网站"  
**时间：** 2026-03-14 22:33 GMT+8  
**状态：** 🔴 **立即修复**

---

## 🎯 最可能的原因排序

### 原因 1：DNS 未配置（最可能）

**症状：** 浏览器显示"无法访问此网站"或"找不到服务器"

**快速检查：**
```bash
# 在你的电脑上执行（不是服务器）
nslookup graysonwit.online
# 或
ping graysonwit.online
```

**如果显示 "Non-existent domain" 或无响应，说明 DNS 未配置**

**解决方案：**
1. 登录你的域名注册商（如阿里云、腾讯云等）
2. 找到 DNS 设置
3. 添加以下记录：

```
记录类型：A
主机名：graysonwit.online
值：111.228.15.109
TTL：600

记录类型：A
主机名：www
值：111.228.15.109
TTL：600

记录类型：A
主机名：api
值：111.228.15.109
TTL：600
```

4. 保存并等待 DNS 生效（通常 5-30 分钟）

---

### 原因 2：Nginx 未运行

**快速检查：**
```bash
ssh root@111.228.15.109
systemctl status nginx
```

**如果显示 "inactive"，执行：**
```bash
systemctl start nginx
systemctl enable nginx
```

---

### 原因 3：防火墙阻止

**快速检查：**
```bash
ssh root@111.228.15.109
ufw status
```

**如果 80 和 443 端口未开放，执行：**
```bash
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

---

### 原因 4：Docker 容器未运行

**快速检查：**
```bash
ssh root@111.228.15.109
cd /opt/worldcup-scout-pro
docker-compose ps
```

**如果容器显示 "Exit"，执行：**
```bash
docker-compose restart
# 或
docker-compose down
docker-compose up -d
```

---

## 🚀 完整的快速修复流程

**按照以下步骤逐一执行：**

### 步骤 1：SSH 连接到服务器

```bash
ssh root@111.228.15.109
# 密码：7wldMUR/
```

### 步骤 2：检查所有服务

```bash
# 检查 Nginx
systemctl status nginx

# 检查 Docker
docker-compose -f /opt/worldcup-scout-pro/docker-compose.yml ps

# 检查防火墙
ufw status
```

### 步骤 3：启动所有服务

```bash
# 启动 Nginx
systemctl start nginx
systemctl enable nginx

# 启动 Docker
cd /opt/worldcup-scout-pro
docker-compose up -d

# 启用防火墙
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

### 步骤 4：验证服务

```bash
# 测试 Nginx
curl -I http://localhost

# 测试后端
curl -I http://localhost:8000

# 测试前端
curl -I http://localhost:3000
```

### 步骤 5：检查 DNS

```bash
# 在你的电脑上执行（不是服务器）
nslookup graysonwit.online
# 应该显示：111.228.15.109
```

---

## 📋 最快的修复方案

**如果你只想快速修复，执行这个一键脚本：**

```bash
ssh root@111.228.15.109 << 'EOF'
# 启动 Nginx
systemctl start nginx
systemctl enable nginx

# 启动 Docker
cd /opt/worldcup-scout-pro
docker-compose up -d

# 配置防火墙
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# 验证
echo "=== Nginx 状态 ==="
systemctl status nginx

echo "=== Docker 容器 ==="
docker-compose ps

echo "=== 防火墙 ==="
ufw status
EOF
```

---

## 🎯 你现在需要做的

### 第一步：检查 DNS

在你的电脑上执行：
```bash
nslookup graysonwit.online
```

**告诉我结果：**
- 如果显示 `111.228.15.109` → DNS 已配置 ✅
- 如果显示 "Non-existent domain" → DNS 未配置 ❌

### 第二步：SSH 连接并执行修复

```bash
ssh root@111.228.15.109
# 密码：7wldMUR/

# 然后执行上面的一键脚本
```

### 第三步：等待 DNS 生效

如果 DNS 未配置，配置后需要等待 5-30 分钟生效

### 第四步：重新访问网站

```
https://graysonwit.online
https://api.graysonwit.online
```

---

## 💡 最可能的问题

**99% 的情况是 DNS 未配置！**

请立即检查你的域名注册商，确保 DNS 记录已添加。

---

**立即执行这些步骤！** 🚀

**告诉我 DNS 检查的结果！** 📝

**我们会立即解决！** 💪

---

**编制时间：** 2026-03-14 22:33 GMT+8  
**状态：** 🔴 **立即修复**
