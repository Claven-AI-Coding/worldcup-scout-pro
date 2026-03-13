# 🚀 部署指南

**项目名称：** 世界杯球探 Pro  
**部署日期：** 2026-03-14  
**部署环境：** Docker + Docker Compose

---

## 📋 部署前检查清单

### 系统要求
- [ ] Docker 已安装（版本 20.10+）
- [ ] Docker Compose 已安装（版本 2.0+）
- [ ] Node.js 已安装（版本 18+）
- [ ] Python 已安装（版本 3.12+）
- [ ] 至少 4GB 可用内存
- [ ] 至少 10GB 可用磁盘空间

### 环境配置
- [ ] `.env` 文件已创建
- [ ] `ANTHROPIC_API_KEY` 已配置
- [ ] `DATABASE_URL` 已配置
- [ ] `REDIS_URL` 已配置
- [ ] `JWT_SECRET_KEY` 已配置

### 代码检查
- [ ] 所有代码已提交
- [ ] 所有测试已通过
- [ ] 所有文档已更新

---

## 🚀 快速部署（一键部署）

### 方式 1：使用部署脚本（推荐）

```bash
cd /root/projects/worldcup-scout-pro
chmod +x deploy.sh
./deploy.sh
```

脚本会自动完成以下步骤：
1. 环境检查
2. 代码检查
3. 前端构建
4. 后端检查
5. Docker 镜像构建
6. 启动服务
7. 数据库迁移
8. 健康检查

### 方式 2：手动部署

#### 步骤 1：启动基础服务

```bash
cd /root/projects/worldcup-scout-pro
docker-compose up -d db redis
```

#### 步骤 2：等待服务就绪

```bash
# 检查数据库
docker-compose exec db pg_isready -U scout

# 检查 Redis
docker-compose exec redis redis-cli ping
```

#### 步骤 3：构建前端

```bash
cd frontend
npm install
npm run build
cd ..
```

#### 步骤 4：启动后端

```bash
docker-compose up -d backend
```

#### 步骤 5：运行数据库迁移

```bash
docker-compose exec backend alembic upgrade head
```

#### 步骤 6：启动前端开发服务器（开发环境）

```bash
cd frontend
npm run dev
```

或启动前端生产服务器：

```bash
docker-compose up -d frontend
```

---

## 📊 部署验证

### 检查服务状态

```bash
# 查看所有服务
docker-compose ps

# 查看服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### 健康检查

```bash
# 后端健康检查
curl http://localhost:8000/api/health

# 前端访问
curl http://localhost:5173

# API 文档
curl http://localhost:8000/docs
```

### 数据库检查

```bash
# 连接数据库
docker-compose exec db psql -U scout -d worldcup_scout

# 查看表
\dt

# 查看迁移状态
SELECT * FROM alembic_version;
```

---

## 🌐 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端 | http://localhost:5173 | Vue 3 应用 |
| 后端 API | http://localhost:8000 | FastAPI 服务 |
| API 文档 | http://localhost:8000/docs | Swagger UI |
| 数据库 | localhost:5432 | PostgreSQL |
| Redis | localhost:6379 | Redis 缓存 |

---

## 🔧 常见问题

### 问题 1：Docker 镜像构建失败

**原因：** 网络问题或依赖下载失败

**解决方案：**
```bash
# 清除缓存重新构建
docker-compose build --no-cache

# 或使用代理
docker build --build-arg HTTP_PROXY=http://proxy:port .
```

### 问题 2：数据库连接失败

**原因：** 数据库未就绪或配置错误

**解决方案：**
```bash
# 检查数据库状态
docker-compose logs db

# 重启数据库
docker-compose restart db

# 检查 .env 配置
cat .env | grep DATABASE_URL
```

### 问题 3：前端无法访问

**原因：** 前端服务未启动或端口被占用

**解决方案：**
```bash
# 检查前端服务
docker-compose logs frontend

# 检查端口占用
lsof -i :5173

# 更改端口
# 修改 docker-compose.yml 中的端口配置
```

### 问题 4：API 调用失败

**原因：** 后端服务未就绪或 API 密钥未配置

**解决方案：**
```bash
# 检查后端服务
docker-compose logs backend

# 检查 API 密钥
cat .env | grep API_KEY

# 重启后端
docker-compose restart backend
```

---

## 📈 性能优化

### 数据库优化

```sql
-- 创建索引
CREATE INDEX idx_match_start_time ON matches(start_time);
CREATE INDEX idx_team_id ON matches(team1_id, team2_id);
CREATE INDEX idx_user_id ON predictions(user_id);

-- 分析表
ANALYZE matches;
ANALYZE teams;
ANALYZE users;
```

### Redis 优化

```bash
# 设置最大内存
redis-cli CONFIG SET maxmemory 512mb

# 设置淘汰策略
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### 应用优化

```bash
# 增加 Uvicorn 工作进程
uvicorn app.main:app --workers 4

# 启用 Gzip 压缩
# 在 main.py 中添加 GZipMiddleware
```

---

## 🔒 安全配置

### 生产环境检查清单

- [ ] 更改默认密码
- [ ] 配置 HTTPS/SSL
- [ ] 启用防火墙
- [ ] 配置 CORS
- [ ] 启用速率限制
- [ ] 配置日志监控
- [ ] 定期备份数据库
- [ ] 启用 API 认证

### 安全命令

```bash
# 生成强密钥
openssl rand -hex 32

# 配置 HTTPS
# 使用 Nginx 反向代理配置 SSL

# 启用防火墙
sudo ufw enable
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
```

---

## 📊 监控和日志

### 查看日志

```bash
# 实时日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend --tail 100

# 导出日志
docker-compose logs > deployment.log
```

### 性能监控

```bash
# 查看容器资源使用
docker stats

# 查看数据库连接
docker-compose exec db psql -U scout -d worldcup_scout -c "SELECT count(*) FROM pg_stat_activity;"

# 查看 Redis 内存使用
docker-compose exec redis redis-cli INFO memory
```

---

## 🛑 停止和清理

### 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据
docker-compose down -v

# 停止特定服务
docker-compose stop backend
```

### 清理资源

```bash
# 删除未使用的镜像
docker image prune

# 删除未使用的容器
docker container prune

# 删除未使用的卷
docker volume prune

# 完全清理
docker system prune -a
```

---

## 📝 部署检查清单

部署完成后，请检查以下项目：

- [ ] 所有服务都在运行
- [ ] 前端可以访问
- [ ] 后端 API 可以调用
- [ ] 数据库迁移成功
- [ ] 日志中没有错误
- [ ] 健康检查通过
- [ ] API 文档可以访问
- [ ] 数据库备份已创建

---

## 🎉 部署完成

恭喜！项目已成功部署！

**下一步：**
1. 访问前端应用
2. 创建测试账户
3. 进行功能测试
4. 收集用户反馈
5. 持续优化和改进

---

**部署指南版本：** 1.0  
**最后更新：** 2026-03-14  
**维护人：** Claven
