# 🔧 部署故障诊断和修复指南

**诊断时间：** 2026-03-14 22:33 GMT+8  
**问题：** 前端和后端都无法使用  
**状态：** 🔴 **紧急修复中**

---

## 🚨 问题分析

**症状：**
- 前端无法访问：https://graysonwit.online
- 后端 API 无法访问：https://api.graysonwit.online

**可能的原因：**
1. Docker 容器未启动
2. Nginx 配置错误
3. 防火墙阻止
4. DNS 未配置
5. 应用启动失败

---

## 🔍 诊断步骤

### 步骤 1：SSH 连接到服务器

```bash
ssh root@111.228.15.109 -p 22
# 密码：7wldMUR/
```

### 步骤 2：检查 Docker 容器状态

```bash
# 查看所有容器
docker-compose ps

# 查看容器日志
docker-compose logs -f

# 查看特定容器日志
docker-compose logs backend
docker-compose logs frontend
```

### 步骤 3：检查 Nginx 状态

```bash
# 检查 Nginx 是否运行
systemctl status nginx

# 查看 Nginx 错误日志
tail -f /var/log/nginx/error.log

# 测试 Nginx 配置
nginx -t
```

### 步骤 4：检查防火墙

```bash
# 查看防火墙规则
ufw status

# 确保 80 和 443 端口开放
ufw allow 80/tcp
ufw allow 443/tcp
```

### 步骤 5：检查 DNS

```bash
# 测试 DNS 解析
nslookup graysonwit.online
dig graysonwit.online

# 检查 DNS 指向
host graysonwit.online
```

### 步骤 6：检查应用日志

```bash
# 查看后端日志
docker-compose logs backend | tail -50

# 查看前端日志
docker-compose logs frontend | tail -50

# 查看 PostgreSQL 日志
docker-compose logs db | tail -50

# 查看 Redis 日志
docker-compose logs redis | tail -50
```

---

## 🛠️ 常见问题和解决方案

### 问题 1：Docker 容器未启动

**症状：** `docker-compose ps` 显示容器状态为 `Exit`

**解决方案：**

```bash
# 重启容器
docker-compose restart

# 或者重新启动
docker-compose down
docker-compose up -d

# 查看启动日志
docker-compose logs -f
```

### 问题 2：Nginx 配置错误

**症状：** `nginx -t` 显示配置错误

**解决方案：**

```bash
# 检查配置文件
cat /etc/nginx/sites-available/worldcup-scout

# 修复配置（如果有错误）
nano /etc/nginx/sites-available/worldcup-scout

# 重新加载 Nginx
nginx -s reload
systemctl restart nginx
```

### 问题 3：防火墙阻止

**症状：** 无法访问 80 或 443 端口

**解决方案：**

```bash
# 允许 HTTP 和 HTTPS
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp

# 启用防火墙
ufw enable

# 查看规则
ufw status
```

### 问题 4：DNS 未配置

**症状：** 域名无法解析

**解决方案：**

1. 登录你的域名注册商
2. 找到 DNS 设置
3. 添加 A 记录：
   ```
   主机名：graysonwit.online
   类型：A
   值：111.228.15.109
   ```
4. 添加 CNAME 记录：
   ```
   主机名：www
   类型：CNAME
   值：graysonwit.online
   ```
5. 添加 API 子域名：
   ```
   主机名：api
   类型：A
   值：111.228.15.109
   ```

### 问题 5：应用启动失败

**症状：** 容器启动后立即退出

**解决方案：**

```bash
# 查看详细错误日志
docker-compose logs backend

# 检查环境变量
cat .env

# 检查数据库连接
docker-compose exec backend psql -U worldcup_user -d worldcup_scout -c "SELECT 1;"

# 检查 Redis 连接
docker-compose exec backend redis-cli ping
```

---

## 🚀 快速修复步骤

### 如果一切都无法工作，执行以下步骤：

```bash
# 1. SSH 连接到服务器
ssh root@111.228.15.109

# 2. 进入项目目录
cd /opt/worldcup-scout-pro

# 3. 停止所有容器
docker-compose down

# 4. 清理旧的容器和镜像
docker system prune -a

# 5. 重新构建
docker-compose build --no-cache

# 6. 重新启动
docker-compose up -d

# 7. 查看日志
docker-compose logs -f

# 8. 检查 Nginx
systemctl restart nginx

# 9. 测试连接
curl -I http://localhost:3000
curl -I http://localhost:8000
```

---

## 📋 完整的诊断清单

请按照以下步骤逐一检查，并告诉我结果：

```
[ ] 1. SSH 连接成功？
[ ] 2. Docker 容器都在运行？
[ ] 3. Nginx 配置正确？
[ ] 4. 防火墙允许 80 和 443？
[ ] 5. DNS 已配置？
[ ] 6. 应用日志中有错误？
[ ] 7. 数据库连接正常？
[ ] 8. Redis 连接正常？
```

---

## 💬 需要你提供的信息

请告诉我：

1. **SSH 连接是否成功？**
   ```bash
   ssh root@111.228.15.109
   ```

2. **Docker 容器状态是什么？**
   ```bash
   docker-compose ps
   ```

3. **Nginx 是否运行？**
   ```bash
   systemctl status nginx
   ```

4. **应用日志中有什么错误？**
   ```bash
   docker-compose logs backend
   ```

5. **防火墙状态如何？**
   ```bash
   ufw status
   ```

---

## 🎯 立即行动

**请执行以下命令并告诉我结果：**

```bash
ssh root@111.228.15.109 << 'EOF'
echo "=== Docker 容器状态 ==="
docker-compose ps

echo "=== Nginx 状态 ==="
systemctl status nginx

echo "=== 防火墙状态 ==="
ufw status

echo "=== 应用日志 ==="
docker-compose logs backend | tail -20

echo "=== 前端日志 ==="
docker-compose logs frontend | tail -20
EOF
```

---

**我已准备好帮助你修复！** 🔧

**请提供诊断结果！** 📝

**我们会立即解决问题！** 💪

---

**编制时间：** 2026-03-14 22:33 GMT+8  
**状态：** 🔴 **紧急修复中**
