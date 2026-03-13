# 测试覆盖率提升计划

## 当前状态

### ✅ 已添加测试
- `tests/components/EmptyState.spec.ts` - 空状态组件测试
- `tests/components/LoadingSpinner.spec.ts` - 加载动画测试
- `tests/utils/api.spec.ts` - API 工具测试
- `tests/setup.ts` - 测试环境配置

### 📊 测试覆盖率目标
- **目标：** ≥85%
- **当前：** 待运行测试

## 测试策略

### 1. 组件测试（优先）
- [x] 通用组件（EmptyState, LoadingSpinner）
- [ ] 赛程组件（MatchCard, LiveScore）
- [ ] 社区组件（PostCard, CommentItem）
- [ ] 竞猜组件（PredictionCard）

### 2. 工具函数测试
- [x] API 错误处理
- [ ] 日期格式化
- [ ] 数据转换

### 3. Store 测试
- [ ] Pinia stores 单元测试
- [ ] 状态管理逻辑

### 4. 集成测试
- [ ] 关键用户流程
- [ ] API 集成

## 下一步

1. 运行现有测试
2. 检查覆盖率
3. 补充缺失测试
4. 达到 85% 目标

---

**创建时间：** 2026-03-13 12:50  
**状态：** 进行中
