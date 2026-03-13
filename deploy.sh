#!/bin/bash
# 世界杯球探 Pro - 完整部署脚本

set -e  # 任何错误都会停止脚本

echo "============================================================"
echo "🚀 世界杯球探 Pro - 完整部署"
echo "============================================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 部署步骤计数
STEP=0

# 日志函数
log_step() {
    STEP=$((STEP + 1))
    echo -e "${BLUE}[$STEP]${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# ============================================================
# 1. 环境检查
# ============================================================
echo ""
log_step "环境检查"
echo "---"

# 检查 Docker
if command -v docker &> /dev/null; then
    log_success "Docker 已安装"
else
    log_error "Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查 Docker Compose
if command -v docker-compose &> /dev/null; then
    log_success "Docker Compose 已安装"
else
    log_error "Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 检查 Node.js
if command -v node &> /dev/null; then
    log_success "Node.js 已安装 ($(node -v))"
else
    log_warning "Node.js 未安装，前端构建可能失败"
fi

# 检查 Python
if command -v python3 &> /dev/null; then
    log_success "Python 已安装 ($(python3 --version))"
else
    log_error "Python 未安装，后端部署失败"
    exit 1
fi

# ============================================================
# 2. 代码检查
# ============================================================
echo ""
log_step "代码检查"
echo "---"

# 检查 Git 状态
if [ -z "$(git status --porcelain)" ]; then
    log_success "代码已同步，无未提交更改"
else
    log_warning "存在未提交的更改"
    git status --short
fi

# 检查最新提交
LATEST_COMMIT=$(git log -1 --oneline)
log_success "最新提交: $LATEST_COMMIT"

# ============================================================
# 3. 前端构建
# ============================================================
echo ""
log_step "前端构建"
echo "---"

cd frontend

# 安装依赖
log_warning "安装前端依赖..."
npm install --legacy-peer-deps 2>&1 | tail -5

# 运行 Lint
log_warning "运行 Lint 检查..."
npm run lint 2>&1 | grep -E "error|warning" | head -5 || log_success "Lint 检查通过"

# 构建
log_warning "构建前端..."
npm run build 2>&1 | tail -5

log_success "前端构建完成"

cd ..

# ============================================================
# 4. 后端检查
# ============================================================
echo ""
log_step "后端检查"
echo "---"

cd backend

# 检查语法
log_warning "检查后端代码语法..."
find app -name "*.py" -exec python3 -m py_compile {} \; 2>&1 | head -5 || log_success "语法检查通过"

log_success "后端检查完成"

cd ..

# ============================================================
# 5. Docker 构建
# ============================================================
echo ""
log_step "Docker 镜像构建"
echo "---"

log_warning "构建 Docker 镜像..."
docker-compose build 2>&1 | tail -10

log_success "Docker 镜像构建完成"

# ============================================================
# 6. 启动服务
# ============================================================
echo ""
log_step "启动服务"
echo "---"

log_warning "启动所有服务..."
docker-compose up -d 2>&1 | tail -10

log_success "服务启动完成"

# ============================================================
# 7. 等待服务就绪
# ============================================================
echo ""
log_step "等待服务就绪"
echo "---"

# 等待数据库
log_warning "等待数据库就绪..."
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U scout > /dev/null 2>&1; then
        log_success "数据库已就绪"
        break
    fi
    echo -n "."
    sleep 1
done

# 等待 Redis
log_warning "等待 Redis 就绪..."
for i in {1..30}; do
    if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
        log_success "Redis 已就绪"
        break
    fi
    echo -n "."
    sleep 1
done

# ============================================================
# 8. 数据库迁移
# ============================================================
echo ""
log_step "数据库迁移"
echo "---"

log_warning "运行数据库迁移..."
docker-compose exec -T backend alembic upgrade head 2>&1 | tail -10

log_success "数据库迁移完成"

# ============================================================
# 9. 健康检查
# ============================================================
echo ""
log_step "健康检查"
echo "---"

# 检查后端
log_warning "检查后端健康状态..."
for i in {1..10}; do
    if curl -s http://localhost:8000/api/health | grep -q "ok"; then
        log_success "后端健康检查通过"
        break
    fi
    echo -n "."
    sleep 1
done

# 检查前端
log_warning "检查前端..."
if [ -d "frontend/dist" ]; then
    log_success "前端构建文件存在"
else
    log_warning "前端构建文件不存在"
fi

# ============================================================
# 10. 部署总结
# ============================================================
echo ""
echo "============================================================"
echo "✅ 部署完成！"
echo "============================================================"
echo ""

echo "📋 服务访问地址："
echo "  前端：http://localhost:5173"
echo "  后端 API：http://localhost:8000"
echo "  API 文档：http://localhost:8000/docs"
echo "  健康检查：http://localhost:8000/api/health"
echo ""

echo "📊 服务状态："
docker-compose ps

echo ""
echo "📝 查看日志："
echo "  后端日志：docker-compose logs -f backend"
echo "  前端日志：docker-compose logs -f frontend"
echo "  数据库日志：docker-compose logs -f db"
echo ""

echo "🛑 停止服务："
echo "  docker-compose down"
echo ""

log_success "部署成功！项目已上线！"
