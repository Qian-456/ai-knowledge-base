---
name: tech-summary
description: 当需要对采集的技术内容进行深度分析总结时使用此技能
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
---

# 技术内容深度分析技能

## 使用场景

当需要对采集的原始技术内容（如 GitHub 热门项目、Hacker News 文章等）进行深度分析、提取技术亮点、评分、标签建议，并发现行业趋势时使用此技能。

## 执行步骤（4步）

### 1. 读取最新采集文件
定位 `knowledge/raw/` 目录下最新的采集文件（按文件名日期排序），优先读取 GitHub Trending 和 Hacker News 的原始数据文件。

### 2. 逐条深度分析
对每个技术条目进行深度分析，生成以下结构化信息：
- **摘要**：中文摘要，≤50字，清晰概括核心价值
- **技术亮点**：2-3个具体技术亮点，用事实和数据说话（例如：采用xx架构、性能提升xx%、支持xx特性）
- **评分**：1-10分，附评分理由（遵循评分标准）
- **标签建议**：3-5个技术标签（如：llm、agent、framework、tool、python）

### 3. 趋势发现
分析全部项目，识别：
- **共同主题**：当前热门的技术方向、共同采用的技术栈
- **新概念**：新兴的技术概念、创新性的解决方案
- **技术趋势**：行业发展趋势预测

### 4. 输出分析结果 JSON
将分析结果保存为 JSON 文件到 `knowledge/articles/tech-analysis-YYYY-MM-DD.json`，文件名中的日期为分析当天日期（UTC 时间）。

## 评分标准

- **9-10分（改变格局）**：技术突破性、行业影响力大、可能改变技术格局的项目
- **7-8分（直接有帮助）**：实用性强、可直接应用于实际项目、解决具体问题的技术
- **5-6分（值得了解）**：有创新点、值得关注但应用场景有限的技术
- **1-4分（可略过）**：技术含量低、重复造轮子、应用价值有限的内容

## 约束条件

- 每批分析 15 个项目时，9-10 分项目不超过 2 个（避免评分膨胀）
- 评分必须附带具体理由，基于客观事实而非主观感受
- 技术亮点必须具体，避免模糊描述（如“性能优秀”应改为“性能提升30%”）

## 注意事项

1. **分析深度**：确保技术分析有深度，避免表面描述，挖掘技术实现的创新点
2. **客观公正**：评分和评价基于客观技术指标，避免个人偏好影响判断
3. **事实依据**：所有技术亮点必须有具体事实、数据或技术细节支持
4. **文件安全**：写入前检查目标目录，避免覆盖已有分析结果
5. **格式一致**：保持输出 JSON 格式的一致性，便于后续处理
6. **语言规范**：分析内容使用中文，技术术语保留英文原名

## 输出格式

```json
{
  "skill": "tech-summary",
  "analyzed_at": "YYYY-MM-DD HH:MM:SS",
  "source_file": "github-trending-YYYY-MM-DD.json",
  "items": [
    {
      "original_name": "原始项目/文章名称",
      "original_url": "原始链接",
      "source_type": "github_trending | hackernews",
      "summary": "≤50字中文摘要",
      "technical_highlights": ["具体亮点1", "具体亮点2", "具体亮点3"],
      "score": 8,
      "score_reason": "评分理由，基于客观事实",
      "suggested_tags": ["llm", "framework", "python"],
      "technical_level": "初级 | 中级 | 高级"
    }
  ],
  "trend_analysis": {
    "common_themes": ["共同主题1", "共同主题2"],
    "new_concepts": ["新概念1", "新概念2"],
    "technical_trends": "行业趋势分析文字描述"
  }
}
```

### 字段说明
- `skill`：固定为 `"tech-summary"`，标识使用的技能
- `analyzed_at`：分析时间，ISO 8601 格式（UTC）
- `source_file`：分析的原始数据文件名
- `items`：分析结果数组，每个元素包含：
  - `original_name`：原始项目/文章名称
  - `original_url`：原始链接
  - `source_type`：数据来源类型
  - `summary`：≤50字中文摘要
  - `technical_highlights`：具体技术亮点数组（2-3个）
  - `score`：评分（1-10）
  - `score_reason`：评分理由，需具体说明
  - `suggested_tags`：建议的技术标签数组（3-5个）
  - `technical_level`：技术难度等级
- `trend_analysis`：趋势分析结果
  - `common_themes`：共同主题数组
  - `new_concepts`：新概念数组
  - `technical_trends`：行业趋势文字描述
