# 🔒 Skill 安全检测和管理系统

**创建时间：** 2026-03-15 02:15 GMT+8  
**目的：** 安全地下载、检测和管理 OpenClaw skills

---

## 🛡️ Skill 安全检测清单

### 1. 源代码安全检测

```bash
#!/bin/bash

# skill_security_check.sh
# 检测 skill 的安全风险

SKILL_PATH=$1

if [ -z "$SKILL_PATH" ]; then
  echo "用法: $0 <skill_path>"
  exit 1
fi

echo "=== Skill 安全检测 ==="
echo "检测路径: $SKILL_PATH"
echo ""

# 1. 检查危险的系统调用
echo "[1/6] 检查危险的系统调用..."
grep -r "exec\|eval\|system\|subprocess\|os.system\|shell=True" "$SKILL_PATH" 2>/dev/null | grep -v "node_modules" && echo "⚠️ 发现危险的系统调用" || echo "✅ 无危险的系统调用"

# 2. 检查文件操作
echo ""
echo "[2/6] 检查文件操作..."
grep -r "open\|write\|delete\|remove\|unlink" "$SKILL_PATH" 2>/dev/null | grep -v "node_modules" && echo "⚠️ 发现文件操作" || echo "✅ 无危险的文件操作"

# 3. 检查网络操作
echo ""
echo "[3/6] 检查网络操作..."
grep -r "http\|socket\|request\|fetch\|curl" "$SKILL_PATH" 2>/dev/null | grep -v "node_modules" && echo "⚠️ 发现网络操作" || echo "✅ 无危险的网络操作"

# 4. 检查环境变量访问
echo ""
echo "[4/6] 检查环境变量访问..."
grep -r "process.env\|os.environ\|getenv" "$SKILL_PATH" 2>/dev/null | grep -v "node_modules" && echo "⚠️ 发现环境变量访问" || echo "✅ 无环境变量访问"

# 5. 检查依赖
echo ""
echo "[5/6] 检查依赖..."
if [ -f "$SKILL_PATH/package.json" ]; then
  echo "Node.js 依赖:"
  cat "$SKILL_PATH/package.json" | grep -A 20 "dependencies"
fi

if [ -f "$SKILL_PATH/requirements.txt" ]; then
  echo "Python 依赖:"
  cat "$SKILL_PATH/requirements.txt"
fi

# 6. 检查 SKILL.md
echo ""
echo "[6/6] 检查 SKILL.md..."
if [ -f "$SKILL_PATH/SKILL.md" ]; then
  echo "✅ SKILL.md 存在"
  echo "描述:"
  head -20 "$SKILL_PATH/SKILL.md"
else
  echo "❌ SKILL.md 不存在"
fi

echo ""
echo "=== 检测完成 ==="
```

### 2. 依赖安全检测

```bash
#!/bin/bash

# skill_dependency_check.sh
# 检测 skill 依赖的安全漏洞

SKILL_PATH=$1

echo "=== Skill 依赖安全检测 ==="

# 检查 Node.js 依赖
if [ -f "$SKILL_PATH/package.json" ]; then
  echo "检查 Node.js 依赖..."
  cd "$SKILL_PATH"
  npm audit 2>&1 | grep -E "vulnerabilities|moderate|high|critical"
  cd -
fi

# 检查 Python 依赖
if [ -f "$SKILL_PATH/requirements.txt" ]; then
  echo "检查 Python 依赖..."
  pip install safety 2>/dev/null
  safety check -r "$SKILL_PATH/requirements.txt" 2>&1 | grep -E "vulnerability|CRITICAL|HIGH"
fi

echo "=== 检测完成 ==="
```

### 3. 代码质量检测

```bash
#!/bin/bash

# skill_quality_check.sh
# 检测 skill 的代码质量

SKILL_PATH=$1

echo "=== Skill 代码质量检测 ==="

# 检查 JavaScript/TypeScript
if [ -f "$SKILL_PATH/package.json" ]; then
  echo "检查 JavaScript 代码质量..."
  cd "$SKILL_PATH"
  npm run lint 2>&1 | head -50
  cd -
fi

# 检查 Python
if [ -f "$SKILL_PATH/requirements.txt" ]; then
  echo "检查 Python 代码质量..."
  pip install pylint 2>/dev/null
  pylint "$SKILL_PATH" 2>&1 | grep -E "error|warning" | head -20
fi

echo "=== 检测完成 ==="
```

---

## 📋 Skill 下载和检测流程

### 步骤 1：下载 Skill

```bash
#!/bin/bash

# download_skill.sh
# 安全地下载 skill

SKILL_NAME=$1
SKILL_URL=$2

if [ -z "$SKILL_NAME" ] || [ -z "$SKILL_URL" ]; then
  echo "用法: $0 <skill_name> <skill_url>"
  exit 1
fi

# 创建临时目录
TEMP_DIR="/tmp/skill_check_$SKILL_NAME"
mkdir -p "$TEMP_DIR"

echo "=== 下载 Skill ==="
echo "名称: $SKILL_NAME"
echo "URL: $SKILL_URL"
echo "临时目录: $TEMP_DIR"
echo ""

# 下载
cd "$TEMP_DIR"
git clone "$SKILL_URL" . 2>&1 | head -20

echo ""
echo "✅ 下载完成"
```

### 步骤 2：运行安全检测

```bash
#!/bin/bash

# check_skill_safety.sh
# 完整的 skill 安全检测

SKILL_PATH=$1

if [ -z "$SKILL_PATH" ]; then
  echo "用法: $0 <skill_path>"
  exit 1
fi

echo "=========================================="
echo "Skill 安全检测"
echo "=========================================="
echo ""

# 1. 源代码安全
echo "📋 [1/4] 源代码安全检测..."
bash skill_security_check.sh "$SKILL_PATH"

# 2. 依赖安全
echo ""
echo "📋 [2/4] 依赖安全检测..."
bash skill_dependency_check.sh "$SKILL_PATH"

# 3. 代码质量
echo ""
echo "📋 [3/4] 代码质量检测..."
bash skill_quality_check.sh "$SKILL_PATH"

# 4. 生成报告
echo ""
echo "📋 [4/4] 生成安全报告..."
cat > "$SKILL_PATH/SECURITY_REPORT.md" << 'EOF'
# Skill 安全检测报告

**检测时间：** $(date)
**Skill 路径：** $SKILL_PATH

## 检测结果

### 源代码安全
- [ ] 无危险的系统调用
- [ ] 无危险的文件操作
- [ ] 无危险的网络操作
- [ ] 无环境变量访问

### 依赖安全
- [ ] 无已知漏洞
- [ ] 依赖版本合理

### 代码质量
- [ ] 代码风格一致
- [ ] 无 lint 错误
- [ ] 文档完整

## 建议

1. 定期更新依赖
2. 运行自动化测试
3. 进行代码审查
4. 监控安全公告

EOF

echo "✅ 报告已生成: $SKILL_PATH/SECURITY_REPORT.md"

echo ""
echo "=========================================="
echo "✅ 安全检测完成"
echo "=========================================="
```

### 步骤 3：安装 Skill

```bash
#!/bin/bash

# install_skill.sh
# 安全地安装 skill

SKILL_PATH=$1
SKILL_NAME=$(basename "$SKILL_PATH")

if [ -z "$SKILL_PATH" ]; then
  echo "用法: $0 <skill_path>"
  exit 1
fi

echo "=== 安装 Skill ==="
echo "名称: $SKILL_NAME"
echo "路径: $SKILL_PATH"
echo ""

# 检查 SKILL.md
if [ ! -f "$SKILL_PATH/SKILL.md" ]; then
  echo "❌ 错误: SKILL.md 不存在"
  exit 1
fi

# 检查安全报告
if [ ! -f "$SKILL_PATH/SECURITY_REPORT.md" ]; then
  echo "⚠️ 警告: 未进行安全检测"
  echo "请先运行: bash check_skill_safety.sh $SKILL_PATH"
  exit 1
fi

# 复制到 skills 目录
SKILLS_DIR="/usr/lib/node_modules/openclaw/skills"
mkdir -p "$SKILLS_DIR/$SKILL_NAME"
cp -r "$SKILL_PATH"/* "$SKILLS_DIR/$SKILL_NAME/"

echo "✅ Skill 已安装到: $SKILLS_DIR/$SKILL_NAME"

# 验证安装
if [ -f "$SKILLS_DIR/$SKILL_NAME/SKILL.md" ]; then
  echo "✅ 验证成功"
else
  echo "❌ 验证失败"
  exit 1
fi
```

---

## 🎯 完整的 Skill 管理工作流

```bash
#!/bin/bash

# manage_skills.sh
# 完整的 skill 管理工作流

SKILL_NAME=$1
SKILL_URL=$2

if [ -z "$SKILL_NAME" ] || [ -z "$SKILL_URL" ]; then
  echo "用法: $0 <skill_name> <skill_url>"
  echo ""
  echo "示例:"
  echo "  $0 weather https://github.com/openclaw/skill-weather.git"
  exit 1
fi

echo "=========================================="
echo "Skill 管理工作流"
echo "=========================================="
echo ""

# 步骤 1: 下载
echo "📥 步骤 1: 下载 Skill..."
TEMP_DIR="/tmp/skill_check_$SKILL_NAME"
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"
git clone "$SKILL_URL" . 2>&1 | tail -5
echo "✅ 下载完成"
echo ""

# 步骤 2: 安全检测
echo "🔒 步骤 2: 安全检测..."
bash check_skill_safety.sh "$TEMP_DIR"
echo ""

# 步骤 3: 用户确认
echo "❓ 步骤 3: 确认安装?"
echo "请查看上面的安全检测结果"
read -p "是否继续安装? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "❌ 已取消"
  exit 1
fi
echo ""

# 步骤 4: 安装
echo "📦 步骤 4: 安装 Skill..."
bash install_skill.sh "$TEMP_DIR"
echo ""

# 步骤 5: 清理
echo "🧹 步骤 5: 清理临时文件..."
rm -rf "$TEMP_DIR"
echo "✅ 清理完成"
echo ""

echo "=========================================="
echo "✅ Skill 管理完成"
echo "=========================================="
```

---

## 📋 Skill 安全检测清单

### 下载前
- [ ] 验证源 URL 的合法性
- [ ] 检查项目的 GitHub stars 和 fork 数
- [ ] 查看项目的最后更新时间
- [ ] 阅读项目的 README 和文档

### 下载后
- [ ] 运行源代码安全检测
- [ ] 运行依赖安全检测
- [ ] 运行代码质量检测
- [ ] 查看安全报告

### 安装前
- [ ] 确认所有检测都通过
- [ ] 手动审查关键代码
- [ ] 确认依赖版本合理
- [ ] 获得用户确认

### 安装后
- [ ] 验证 skill 正常工作
- [ ] 监控 skill 的行为
- [ ] 定期更新依赖
- [ ] 监控安全公告

---

## 🚀 快速开始

```bash
# 1. 下载脚本
curl -O https://raw.githubusercontent.com/openclaw/openclaw/main/skills/security/check_skill_safety.sh
curl -O https://raw.githubusercontent.com/openclaw/openclaw/main/skills/security/manage_skills.sh

# 2. 给脚本执行权限
chmod +x check_skill_safety.sh manage_skills.sh

# 3. 使用脚本
./manage_skills.sh weather https://github.com/openclaw/skill-weather.git
```

---

## ✅ 安全最佳实践

1. **只从官方或信任的源下载 skill**
2. **总是运行安全检测**
3. **定期更新依赖**
4. **监控 skill 的行为**
5. **保持 OpenClaw 更新**

