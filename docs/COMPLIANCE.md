# 合规风控系统文档

## 概述

完整的内容审核和用户管理系统，包括违禁词过滤、举报审核、用户封禁等功能。

## 功能模块

### 1. 违禁词管理

**管理员 API：**
- `POST /api/v1/compliance/banned-words` - 添加违禁词
- `POST /api/v1/compliance/banned-words/batch` - 批量添加
- `GET /api/v1/compliance/banned-words` - 获取违禁词列表
- `DELETE /api/v1/compliance/banned-words/{id}` - 删除违禁词

**分类：**
- `profanity` - 脏话粗口
- `gambling` - 赌博相关
- `political` - 政治敏感
- `spam` - 垃圾广告
- `illegal` - 违法内容

### 2. 内容检查

**公开 API：**
- `POST /api/v1/compliance/check-content` - 检查文本内容

**返回：**
```json
{
  "is_clean": false,
  "matched_words": ["赌球", "下注"],
  "categories": ["gambling"],
  "filtered_text": "不要**，不要**"
}
```

**使用场景：**
- 发帖前实时检查
- 评论前实时检查
- 用户昵称检查

### 3. 举报系统

**用户 API：**
- `POST /api/v1/compliance/reports` - 创建举报

**管理员 API：**
- `GET /api/v1/compliance/reports/pending` - 获取待审核举报
- `POST /api/v1/compliance/reports/{id}/review` - 审核举报

**举报类型：**
- `post` - 帖子
- `comment` - 评论
- `user` - 用户

**处理动作：**
- `none` - 不处理
- `delete_content` - 删除内容
- `warn_user` - 警告用户
- `ban_user` - 封禁用户

### 4. 用户违规管理

**管理员 API：**
- `POST /api/v1/compliance/violations` - 创建违规记录
- `GET /api/v1/compliance/violations/user/{user_id}` - 获取用户违规记录

**公开 API：**
- `GET /api/v1/compliance/ban-status/{user_id}` - 检查封禁状态

**违规类型：**
- `spam` - 垃圾信息
- `profanity` - 脏话粗口
- `harassment` - 骚扰他人
- `illegal` - 违法内容

**严重程度：**
- `warning` - 警告
- `serious` - 严重
- `severe` - 极严重

**处理动作：**
- `warned` - 已警告
- `temp_ban` - 临时封禁
- `permanent_ban` - 永久封禁

## 使用流程

### 发帖流程（前端）

```javascript
// 1. 用户输入内容
const content = "这是帖子内容..."

// 2. 提交前检查
const checkResult = await api.post('/api/v1/compliance/check-content', {
  text: content
})

if (!checkResult.is_clean) {
  // 3. 提示用户包含违禁词
  alert(`内容包含违禁词：${checkResult.matched_words.join(', ')}`)
  // 可选：显示过滤后的文本
  console.log('过滤后：', checkResult.filtered_text)
  return
}

// 4. 内容合规，提交帖子
await api.post('/api/v1/community/posts', { content })
```

### 举报流程

```javascript
// 1. 用户点击举报按钮
const reportData = {
  target_type: 'post',
  target_id: 123,
  reason: '包含不当内容'
}

// 2. 提交举报
await api.post('/api/v1/compliance/reports', reportData)

// 3. 管理员审核（后台）
// GET /api/v1/compliance/reports/pending

// 4. 管理员处理
await api.post('/api/v1/compliance/reports/123/review', {
  status: 'reviewed',
  action: 'delete_content',
  notes: '确认违规，已删除'
})
```

### 封禁用户流程

```javascript
// 1. 管理员创建违规记录
await api.post('/api/v1/compliance/violations', {
  user_id: 456,
  violation_type: 'spam',
  severity: 'serious',
  action_taken: 'temp_ban',
  ban_days: 7,
  notes: '连续发送垃圾信息'
})

// 2. 用户被自动封禁 7 天
// 3. 用户尝试登录时检查封禁状态
const banStatus = await api.get('/api/v1/compliance/ban-status/456')
if (banStatus.is_banned) {
  alert(`您已被封禁至 ${banStatus.ban_until}`)
}
```

## 数据库表结构

### banned_words（违禁词）
```sql
CREATE TABLE banned_words (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### user_violations（用户违规记录）
```sql
CREATE TABLE user_violations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    violation_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) DEFAULT 'warning',
    content TEXT,
    action_taken VARCHAR(50),
    ban_until TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### users（新增字段）
```sql
ALTER TABLE users ADD COLUMN is_banned BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN ban_until TIMESTAMP WITH TIME ZONE;
```

## 初始化

### 1. 运行数据库迁移
```bash
cd backend
alembic upgrade head
```

### 2. 导入初始违禁词
```python
from app.utils.banned_words_seed import get_all_banned_words
from app.models.banned_word import BannedWord

# 在数据库中批量插入
words = get_all_banned_words()
for word, category in words:
    db.add(BannedWord(word=word, category=category))
db.commit()
```

## 配置建议

### 1. 违禁词库维护
- 定期更新违禁词库
- 根据实际情况调整分类
- 可以从外部导入通用违禁词库

### 2. 自动化规则
- 设置自动封禁阈值（如 3 次警告自动封禁）
- 配置不同严重程度的处理策略
- 实现申诉流程

### 3. 监控和统计
- 记录违规趋势
- 分析高频违禁词
- 监控举报处理效率

## 安全建议

1. **权限控制**
   - 管理员 API 必须验证 `is_admin` 权限
   - 用户只能查看自己的违规记录

2. **防止滥用**
   - 限制举报频率（如每天最多 10 次）
   - 检测恶意举报行为

3. **数据保护**
   - 违规内容脱敏存储
   - 定期清理过期数据

4. **合规性**
   - 遵守当地法律法规
   - 提供用户申诉渠道
   - 保留审核记录

## 未来扩展

- [ ] 图片内容审核（OCR + AI）
- [ ] 敏感图片检测
- [ ] 链接安全检测
- [ ] AI 自动审核
- [ ] 风险预警系统
- [ ] 合规报告生成

---

**版本：** v1.0  
**更新时间：** 2026-03-13
