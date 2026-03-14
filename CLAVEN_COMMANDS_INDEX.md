# 📚 Claven 指令完整索引

**编制日期：** 2026-03-14 18:03 GMT+8  
**编制者：** Claven（Leader）  
**用途：** 知识库查阅，形成沟通习惯  
**更新频率：** 每周更新

---

## 🎯 快速导航

### 按类别查找

- [OpenClaw 系统命令](#openclaw-系统命令)
- [会话管理命令](#会话管理命令)
- [策略切换命令](#策略切换命令)
- [任务分配命令](#任务分配命令)
- [Claven 自主权限](#claven-自主权限)
- [部署和发布命令](#部署和发布命令)

### 按用途查找

- [日常工作](#日常工作)
- [项目管理](#项目管理)
- [多项目协作](#多项目协作)
- [紧急情况](#紧急情况)

---

## 📖 完整文档列表

### 1. OpenClaw 系统命令

**文档：** `OPENCLAW_COMMANDS_GUIDE.md`  
**内容：** OpenClaw 的所有系统命令  
**适用场景：** 日常工作、会话管理

**主要命令：**
```
会话管理：
  /new              创建新会话
  /reset            重置会话
  /compact          压缩历史
  /stop             停止会话

选项配置：
  /think <level>    设置推理深度
  /model <id>       切换模型
  /verbose on|off   详细模式

状态查询：
  /status           查看状态
  /whoami           查看身份
  /context          查看上下文

技能调用：
  /skill <name>     调用技能
```

**查看文档：** 闲暇时预览，逐步掌握

---

### 2. OpenClaw 操作手册

**文档：** `OPENCLAW_OPERATIONS_MANUAL.md`  
**内容：** 完整的 OpenClaw 学习和参考手册  
**适用场景：** 学习和参考

**包含内容：**
- 快速开始（最常用的 5 个命令）
- 四大命令类别详解
- 实际使用场景（5 个真实场景）
- 成本优化指南
- 常见问题解答
- 最佳实践
- 参考速查表
- 学习路径（3 周计划）

**查看文档：** 系统学习，建立知识体系

---

### 3. /new 命令详解

**文档：** `NEW_COMMAND_EXPLAINED.md`  
**内容：** `/new` 命令的完整解析和数据持久化机制  
**适用场景：** 理解会话切换和数据保存

**核心内容：**
- `/new` 会清空什么（对话历史）
- `/new` 不会清空什么（文件、Git、内存、知识库）
- 四层数据持久化机制
- 会话切换的完整流程
- 最佳实践

**查看文档：** 理解会话管理的基础

---

### 4. Claven 自主权限和任务分配

**文档：** `CLAVEN_AUTONOMY_AND_TASK_ASSIGNMENT.md`  
**内容：** Claven 的自主权限和明确的任务分配机制  
**适用场景：** 理解 Claven 的角色和权限

**核心内容：**
- Claven 的自主会话切换规则
- 自主决策权限
- 任务分配的标准格式
- 日常任务分配流程
- 权限和责任矩阵

**查看文档：** 理解 Claven 的 Leader 角色

---

### 5. 多项目会话和模型管理

**文档：** `MULTI_PROJECT_SESSION_AND_MODEL_MANAGEMENT.md`  
**内容：** 多项目切换、模型分配、Agent 并行工作的深度解析  
**适用场景：** 多项目管理

**核心内容：**
- 会话的三种状态
- 三种会话管理策略
- 模型配置的隔离机制
- 模型配置的优先级
- 多 Agent 并行工作
- 成本计算

**查看文档：** 理解复杂的多项目管理

---

### 6. 动态策略切换和并行会话

**文档：** `DYNAMIC_STRATEGY_SWITCHING_AND_PARALLEL_SESSIONS.md`  
**内容：** 动态策略切换、多会话管理、并行活跃详解  
**适用场景：** 高级会话管理

**核心内容：**
- 三种策略的动态切换命令
- 完全隔离模式下的多会话管理
- 并行活跃模式的详细解析
- 三种模式的对比
- 实际工作流程

**查看文档：** 掌握高级会话管理技巧

---

### 7. /strategy 命令集成问题

**文档：** `STRATEGY_COMMAND_INTEGRATION_ISSUE.md`  
**内容：** `/strategy` 命令的集成问题和解决方案  
**适用场景：** 了解当前的限制和临时方案

**核心内容：**
- 问题描述和原因
- 需要实现的命令
- 三种实现方案
- 临时解决方案
- 时间表和优先级

**查看文档：** 了解系统的当前状态

---

## 🎯 按使用场景分类

### 日常工作

**需要查看的文档：**
1. `OPENCLAW_COMMANDS_GUIDE.md` - 基础命令
2. `OPENCLAW_OPERATIONS_MANUAL.md` - 操作手册
3. `CLAVEN_AUTONOMY_AND_TASK_ASSIGNMENT.md` - 任务分配

**常用命令：**
```
/status              查看状态
/model <id>          切换模型
/think <level>       设置思考深度
/new                 创建新会话
/stop                停止会话
```

---

### 项目管理

**需要查看的文档：**
1. `CLAVEN_AUTONOMY_AND_TASK_ASSIGNMENT.md` - 任务分配
2. `MULTI_PROJECT_SESSION_AND_MODEL_MANAGEMENT.md` - 多项目管理
3. `DYNAMIC_STRATEGY_SWITCHING_AND_PARALLEL_SESSIONS.md` - 策略切换

**常用命令：**
```
/new project-a       创建项目 A 会话
/pause               暂停当前会话
/resume project-a    恢复项目 A
/list-sessions       列出所有会话
/status-all          查看所有会话状态
```

---

### 多项目协作

**需要查看的文档：**
1. `MULTI_PROJECT_SESSION_AND_MODEL_MANAGEMENT.md` - 多项目管理
2. `DYNAMIC_STRATEGY_SWITCHING_AND_PARALLEL_SESSIONS.md` - 策略切换
3. `STRATEGY_COMMAND_INTEGRATION_ISSUE.md` - 当前限制

**常用命令：**
```
/strategy pause-resume           暂停-恢复模式
/strategy complete-isolation     完全隔离模式
/strategy parallel-active        并行活跃模式
/switch project-a                切换到项目 A
/switch-session project-a s-001  切换到特定会话
```

---

### 紧急情况

**需要查看的文档：**
1. `OPENCLAW_OPERATIONS_MANUAL.md` - 成本优化指南
2. `DYNAMIC_STRATEGY_SWITCHING_AND_PARALLEL_SESSIONS.md` - 并行活跃模式
3. `CLAVEN_AUTONOMY_AND_TASK_ASSIGNMENT.md` - 快速决策

**常用命令：**
```
/strategy parallel-active        启用并行活跃模式
/new project-a                   创建新会话
/new project-b                   创建新会话
/new project-c                   创建新会话
/switch project-a                快速切换
/status-all                       查看所有状态
```

---

## 📋 命令速查表

### OpenClaw 系统命令

```
会话管理
  /new [name]              创建新会话
  /reset                   重置会话
  /compact [instructions]  压缩历史
  /stop                    停止会话

选项配置
  /think off|fast|deep|extended    设置思考深度
  /model opus|sonnet|haiku         切换模型
  /verbose on|off                  详细模式

状态查询
  /status                  查看状态
  /whoami                  查看身份
  /context                 查看上下文

技能调用
  /skill <name> [input]    调用技能
```

### Claven 自定义命令（待实现）

```
策略管理
  /strategy pause-resume           暂停-恢复模式
  /strategy complete-isolation     完全隔离模式
  /strategy parallel-active        并行活跃模式
  /strategy status                 查看当前策略
  /strategy list                   列出所有策略

会话管理
  /switch <project>                切换会话
  /switch-session <p> <s>          切换到特定会话
  /pause [project]                 暂停会话
  /resume <project>                恢复会话
  /list-sessions                   列出所有会话
  /status-all                      查看所有会话状态
  /stop-all                        结束所有会话
```

---

## 🎓 学习路径

### 第一周：基础命令

**Day 1-2：会话管理**
- 阅读：`OPENCLAW_COMMANDS_GUIDE.md`
- 学习：/new、/reset、/stop
- 理解：会话的概念

**Day 3-4：选项配置**
- 阅读：`OPENCLAW_OPERATIONS_MANUAL.md`
- 学习：/model、/think、/verbose
- 理解：模型和思考深度

**Day 5-7：状态查询**
- 阅读：`NEW_COMMAND_EXPLAINED.md`
- 学习：/status、/whoami、/context
- 理解：数据持久化

### 第二周：实践应用

**Day 8-10：场景应用**
- 阅读：`CLAVEN_AUTONOMY_AND_TASK_ASSIGNMENT.md`
- 学习：任务分配
- 实践：在项目中应用

**Day 11-14：多项目管理**
- 阅读：`MULTI_PROJECT_SESSION_AND_MODEL_MANAGEMENT.md`
- 学习：多项目切换
- 实践：管理多个项目

### 第三周：高级用法

**Day 15-21：高级技巧**
- 阅读：`DYNAMIC_STRATEGY_SWITCHING_AND_PARALLEL_SESSIONS.md`
- 学习：策略切换
- 实践：复杂场景管理

---

## 💡 沟通习惯建议

### 日常沟通

**GraySon 可以这样与 Claven 沟通：**

```
"Claven，现在切换到暂停-恢复模式"
↓ Claven 理解并执行

"Claven，分配任务给 CodeSmith"
↓ Claven 生成任务分配单

"Claven，查看所有会话状态"
↓ Claven 显示状态信息

"Claven，切换到项目 B"
↓ Claven 执行切换
```

### 参考文档

**GraySon 可以这样参考文档：**

```
"我想了解 /strategy 命令"
↓ 查看 DYNAMIC_STRATEGY_SWITCHING_AND_PARALLEL_SESSIONS.md

"我想学习任务分配"
↓ 查看 CLAVEN_AUTONOMY_AND_TASK_ASSIGNMENT.md

"我想了解多项目管理"
↓ 查看 MULTI_PROJECT_SESSION_AND_MODEL_MANAGEMENT.md

"我想查看所有命令"
↓ 查看 OPENCLAW_COMMANDS_GUIDE.md
```

---

## 📊 文档统计

| 文档 | 行数 | 主题 | 优先级 |
|------|------|------|--------|
| OPENCLAW_COMMANDS_GUIDE.md | 431 | 系统命令 | 高 |
| OPENCLAW_OPERATIONS_MANUAL.md | 942 | 操作手册 | 高 |
| NEW_COMMAND_EXPLAINED.md | 406 | /new 详解 | 中 |
| CLAVEN_AUTONOMY_AND_TASK_ASSIGNMENT.md | 626 | 权限和分配 | 高 |
| MULTI_PROJECT_SESSION_AND_MODEL_MANAGEMENT.md | 669 | 多项目管理 | 高 |
| DYNAMIC_STRATEGY_SWITCHING_AND_PARALLEL_SESSIONS.md | 751 | 策略切换 | 高 |
| STRATEGY_COMMAND_INTEGRATION_ISSUE.md | 308 | 问题记录 | 中 |

**总计：** 4,133 行文档

---

## 🚀 使用建议

### 对 GraySon 的建议

1. **建立阅读习惯**
   - 每周阅读一份文档
   - 逐步建立知识体系
   - 形成与 Claven 的沟通习惯

2. **参考文档**
   - 遇到问题时查看相关文档
   - 在沟通前了解背景
   - 提高沟通效率

3. **反馈和改进**
   - 提出文档的不清楚之处
   - 建议添加新的内容
   - 帮助完善文档

### 对 Claven 的建议

1. **定期更新**
   - 每周更新文档
   - 添加新的命令
   - 记录新的发现

2. **保持清晰**
   - 使用清晰的结构
   - 提供实际例子
   - 解释背后的原理

3. **持续改进**
   - 根据反馈改进
   - 添加更多场景
   - 优化文档组织

---

## 📞 快速查询

**我想了解...**

| 问题 | 查看文档 |
|------|---------|
| OpenClaw 的所有命令 | OPENCLAW_COMMANDS_GUIDE.md |
| 如何使用 OpenClaw | OPENCLAW_OPERATIONS_MANUAL.md |
| /new 命令的详细信息 | NEW_COMMAND_EXPLAINED.md |
| Claven 的权限和职责 | CLAVEN_AUTONOMY_AND_TASK_ASSIGNMENT.md |
| 多项目管理 | MULTI_PROJECT_SESSION_AND_MODEL_MANAGEMENT.md |
| 策略切换和并行会话 | DYNAMIC_STRATEGY_SWITCHING_AND_PARALLEL_SESSIONS.md |
| /strategy 命令的问题 | STRATEGY_COMMAND_INTEGRATION_ISSUE.md |

---

**这是 Claven 指令的完整索引！** 📚

**形成阅读和沟通习惯！** 💬

**持续学习和改进！** 🚀

---

**编制时间：** 2026-03-14 18:03 GMT+8  
**完整性：** 100%  
**实用性：** ⭐⭐⭐⭐⭐
