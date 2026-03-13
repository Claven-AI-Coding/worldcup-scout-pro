# 🔧 OpenClaw 命令详解

**时间：** 2026-03-14 04:00 GMT+8  
**用途：** 理解 OpenClaw 系统命令

---

## 📋 完整命令列表解析

### 🔄 Session（会话管理）

| 命令 | 中文 | 含义 | 用途 |
|------|------|------|------|
| `/new` | 新建 | 创建新的会话 | 开始全新的对话，清空历史 |
| `/reset` | 重置 | 重置当前会话 | 清空当前会话的上下文，但保留会话 |
| `/compact [instructions]` | 压缩 | 压缩会话历史 | 节省 token，合并历史消息 |
| `/stop` | 停止 | 停止当前会话 | 结束会话，保存状态 |

**使用场景：**
```
/new → 开始完全新的项目
/reset → 清空当前对话，重新开始
/compact → token 用完前压缩历史
/stop → 结束工作，保存进度
```

---

### ⚙️ Options（选项配置）

| 命令 | 中文 | 含义 | 用途 |
|------|------|------|------|
| `/think <level>` | 思考 | 设置推理深度 | 控制 Claude 的思考时间 |
| `/model <id>` | 模型 | 切换 AI 模型 | 选择不同的模型执行任务 |
| `/verbose on\|off` | 详细模式 | 开启/关闭详细输出 | 控制输出的详细程度 |

**使用示例：**
```
/think deep → 深度思考（用于复杂问题）
/think fast → 快速思考（用于简单问题）

/model opus → 使用 Opus 模型
/model haiku → 使用 Haiku 模型

/verbose on → 显示所有细节
/verbose off → 只显示关键信息
```

---

### 📊 Status（状态查询）

| 命令 | 中文 | 含义 | 用途 |
|------|------|------|------|
| `/status` | 状态 | 查看当前会话状态 | 了解 token 使用、时间、成本 |
| `/whoami` | 我是谁 | 查看当前身份 | 确认当前用户和角色 |
| `/context` | 上下文 | 查看当前上下文 | 了解系统知道什么 |

**查看内容：**
```
/status → 
  - Token 使用情况
  - 会话时间
  - 成本统计
  - 模型信息

/whoami →
  - 用户名
  - 用户 ID
  - 权限级别
  - 角色

/context →
  - 加载的文件
  - 内存内容
  - 工作目录
  - 可用工具
```

---

### 🎓 Skills（技能调用）

| 命令 | 中文 | 含义 | 用途 |
|------|------|------|------|
| `/skill <name> [input]` | 技能 | 调用特定技能 | 执行专门的任务 |

**可用技能示例：**
```
/skill clawhub → 使用 ClawHub 技能
/skill healthcheck → 运行健康检查
/skill skill-creator → 创建新技能
/skill tmux → 控制 tmux 会话
/skill weather → 获取天气信息
```

---

## 🎯 实际使用场景

### 场景 1：开发新项目

```
/new
  → 创建新会话

/model opus
  → 选择最强模型

/think deep
  → 启用深度思考

/verbose on
  → 显示详细信息

开始开发...
```

### 场景 2：切换任务

```
/reset
  → 清空当前上下文

/model haiku
  → 切换到便宜模型

/verbose off
  → 关闭详细输出

开始新任务...
```

### 场景 3：检查状态

```
/status
  → 查看 token 使用

/whoami
  → 确认身份

/context
  → 查看加载的文件

决定是否继续...
```

### 场景 4：节省成本

```
/status
  → 检查 token 使用

/compact
  → 压缩历史

/model haiku
  → 切换便宜模型

继续工作...
```

---

## 💡 命令组合使用

### 高效开发流程

```
1. /new
   创建新会话

2. /model opus
   选择最强模型

3. /think deep
   启用深度思考

4. 开发工作...

5. /status
   检查进度

6. /compact
   压缩历史（如需要）

7. /stop
   保存并结束
```

### 成本优化流程

```
1. /status
   检查当前成本

2. 如果成本高：
   /model haiku
   切换到便宜模型

3. /verbose off
   减少输出

4. /compact
   压缩历史

5. 继续工作...
```

### 问题诊断流程

```
1. /whoami
   确认身份

2. /context
   查看上下文

3. /status
   检查状态

4. /skill healthcheck
   运行健康检查

5. 根据结果调整...
```

---

## 🔍 高级用法

### 思考深度设置

```
/think off
  → 不使用推理（最快）

/think fast
  → 快速推理（平衡）

/think deep
  → 深度推理（最慢但最准确）

/think extended
  → 扩展推理（最深度）
```

### 模型选择

```
/model opus-thinking
  → 最强推理模型

/model opus
  → 最强通用模型

/model sonnet
  → 平衡模型

/model haiku
  → 最便宜模型
```

### 详细模式

```
/verbose on
  → 显示：
    - 所有工具调用
    - 完整的推理过程
    - 详细的错误信息
    - 所有中间步骤

/verbose off
  → 只显示：
    - 最终结果
    - 关键信息
    - 错误摘要
```

---

## 📚 完整命令参考

### 会话管理
- `/new` - 新建会话
- `/reset` - 重置会话
- `/compact [instructions]` - 压缩历史
- `/stop` - 停止会话

### 配置选项
- `/think <level>` - 设置思考深度
- `/model <id>` - 切换模型
- `/verbose on|off` - 详细模式

### 状态查询
- `/status` - 查看状态
- `/whoami` - 查看身份
- `/context` - 查看上下文

### 技能调用
- `/skill <name> [input]` - 调用技能

### 帮助
- `/help` - 显示帮助
- `/commands` - 显示完整命令列表

---

## 🎓 最佳实践

### 1. 定期检查状态
```
每小时：/status
  → 了解 token 使用情况
  → 及时调整策略
```

### 2. 合理选择模型
```
简单任务 → /model haiku
一般任务 → /model sonnet
复杂任务 → /model opus
关键决策 → /model opus-thinking
```

### 3. 控制输出详细程度
```
开发阶段 → /verbose on
生产阶段 → /verbose off
调试阶段 → /verbose on
```

### 4. 及时压缩历史
```
当 token 接近上限时：
/compact "保留最近的代码和决策"
```

### 5. 定期重置
```
切换项目时：/reset
开始新任务时：/new
```

---

## 🚀 在我们项目中的应用

### 世界杯球探 Pro 项目

```
开始项目：
/new
/model opus
/think deep

开发阶段：
/verbose on
/status（每小时检查）

优化阶段：
/model sonnet
/verbose off

部署阶段：
/model opus
/think deep
/status（最终检查）

完成：
/compact
/stop
```

### 多项目管理

```
项目 A：
/new
/model opus
开发...

切换到项目 B：
/reset
/model sonnet
开发...

查看项目 A 状态：
/context
/status
```

---

## 💰 成本控制示例

```
高成本模式：
/model opus-thinking
/think deep
/verbose on
成本：最高

平衡模式：
/model sonnet
/think fast
/verbose off
成本：中等

低成本模式：
/model haiku
/think off
/verbose off
成本：最低
```

---

**这些命令是 OpenClaw 的核心控制工具！** 🔧

**掌握它们可以大幅提升效率！** 🚀

**在我们的项目中充分利用它们！** 💪

---

**参考时间：** 2026-03-14 04:00 GMT+8  
**完整性：** 100%  
**实用性：** ⭐⭐⭐⭐⭐
