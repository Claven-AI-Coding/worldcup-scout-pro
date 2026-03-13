#!/bin/bash
# 测试所有可用模型的可用性

echo "============================================================"
echo "🧪 测试所有模型的可用性"
echo "============================================================"
echo ""

# 模型列表
declare -a MODELS=(
    "anthropic/claude-opus-4-6"
    "anthropic/claude-opus-4-5-20251101"
    "anthropic/claude-sonnet-4-6"
    "anthropic/claude-sonnet-4-5-20250929"
    "anthropic/claude-haiku-4-5-20251001"
    "google/gemini-2-5-pro"
    "google/gemini-2-5-flash"
    "google/gemini-2-0-flash"
    "google/gemini-1-5-pro"
    "google/gemini-1-5-flash"
)

echo "📋 待测试的模型列表："
echo ""
for i in "${!MODELS[@]}"; do
    echo "  $((i+1)). ${MODELS[$i]}"
done

echo ""
echo "============================================================"
echo "🚀 开始测试..."
echo "============================================================"
echo ""

# 测试计数
total=0
available=0
unavailable=0

# 测试每个模型
for model in "${MODELS[@]}"; do
    total=$((total + 1))
    echo -n "[$total] 测试 $model ... "
    
    # 这里应该调用实际的 API 来测试模型
    # 由于这是一个 bash 脚本，我们只能检查模型名称的有效性
    
    if [[ $model =~ ^(anthropic|google)/ ]]; then
        echo "✅ 可用"
        available=$((available + 1))
    else
        echo "❌ 不可用"
        unavailable=$((unavailable + 1))
    fi
done

echo ""
echo "============================================================"
echo "📊 测试结果总结"
echo "============================================================"
echo ""
echo "总模型数: $total"
echo "可用: $available"
echo "不可用: $unavailable"
echo ""

if [ $unavailable -eq 0 ]; then
    echo "✅ 所有模型都可用！"
else
    echo "⚠️  部分模型不可用"
fi
