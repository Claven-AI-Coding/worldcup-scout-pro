# 🚀 如何运行修复脚本

**脚本位置：** `/root/projects/worldcup-scout-pro/fix-deployment.sh`

---

## 📋 运行步骤

### 步骤 1：下载脚本到你的电脑

```bash
# 从 GitHub 下载
wget https://raw.githubusercontent.com/Claven-AI-Coding/worldcup-scout-pro/main/fix-deployment.sh

# 或者使用 curl
curl -O https://raw.githubusercontent.com/Claven-AI-Coding/worldcup-scout-pro/main/fix-deployment.sh
```

### 步骤 2：上传脚本到服务器

```bash
# 使用 scp 上传
scp fix-deployment.sh root@111.228.15.109:/root/

# 或者使用 sftp
sftp root@111.228.15.109
put fix-deployment.sh
```

### 步骤 3：SSH 连接到服务器

```bash
ssh root@111.228.15.109
# 密码：7wldMUR/
```

### 步骤 4：运行脚本

```bash
# 进入脚本所在目录
cd /root

# 给脚本执行权限
chmod +x fix-deployment.sh

# 运行脚本
./fix-deployment.sh
```

### 步骤 5：等待脚本完成

脚本会自动：
- ✅ 安装 Nginx
- ✅ 启动 Nginx
- ✅ 创建 Nginx 配置
- ✅ 启用配置
- ✅ 测试配置
- ✅ 重启 Nginx
- ✅ 启动 Docker 容器
- ✅ 验证服务

### 步骤 6：检查 DNS

在你的电脑上执行：
```bash
nslookup graysonwit.online
```

应该显示：`111.228.15.109`

### 步骤 7：访问网站

```
https://graysonwit.online
https://api.graysonwit.online
```

---

## 🎯 一行命令快速运行

如果你想一行命令完成所有操作：

```bash
ssh root@111.228.15.109 'bash -s' < fix-deployment.sh
```

或者：

```bash
ssh root@111.228.15.109 << 'EOF'
cd /opt/worldcup-scout-pro
bash fix-deployment.sh
EOF
```

---

## ✅ 脚本会做什么

1. **安装 Nginx** - 如果未安装
2. **启动 Nginx** - 并设置开机自启
3. **创建配置** - 为前端和后端配置反向代理
4. **启用配置** - 删除默认配置
5. **测试配置** - 确保配置正确
6. **重启 Nginx** - 应用配置
7. **启动 Docker** - 启动应用容器
8. **验证服务** - 显示所有服务状态

---

## 🔍 如果脚本失败

如果脚本在某个步骤失败，会显示错误信息。

**常见错误和解决方案：**

1. **权限不足**
   ```bash
   # 使用 sudo
   sudo ./fix-deployment.sh
   ```

2. **脚本没有执行权限**
   ```bash
   chmod +x fix-deployment.sh
   ```

3. **Nginx 配置错误**
   ```bash
   # 检查配置
   nginx -t
   
   # 查看错误
   cat /etc/nginx/sites-available/worldcup-scout
   ```

4. **Docker 容器启动失败**
   ```bash
   # 查看日志
   docker-compose logs
   
   # 重启容器
   docker-compose restart
   ```

---

## 📝 脚本内容

脚本位置：`fix-deployment.sh`

包含以下操作：
- Nginx 安装和配置
- SSL 证书配置
- 反向代理设置
- Docker 容器启动
- 服务验证

---

**现在你可以运行这个脚本来修复部署！** 🚀

**告诉我脚本运行的结果！** 📝

**我们会立即解决任何问题！** 💪
