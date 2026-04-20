---
name: github-trending
description: 当需要采集 GitHub 热门开源项目时使用此技能
allowed-tools: Read, Grep, Glob, WebFetch
---

# GitHub Trending 采集技能

## 使用场景

当需要采集 GitHub 热门开源项目，特别是 AI/LLM/Agent 领域的趋势项目时，使用此技能自动抓取、过滤和分析 GitHub Trending 数据。

## 执行步骤（7步）

### 1. 搜索热门仓库
使用 GitHub API（或 GitHub Trending 页面）获取当日/本周热门仓库列表，优先使用 API 以避免频率限制问题。

### 2. 提取信息
从 API 响应或页面 HTML 中提取每个仓库的关键信息：项目名称、描述、URL、星标数、编程语言、主题标签（topics）。

### 3. 过滤
- **纳入范围**：优先选择与 AI/LLM/Agent 相关的项目（通过关键词匹配：AI、LLM、Agent、Machine Learning、Deep Learning、Transformer、GPT、LangChain 等）
- **排除范围**：过滤掉 Awesome 列表（标题包含 "awesome-" 或描述主要为列表性质的项目）、非技术项目、纯文档项目

### 4. 去重
对比本地已有记录（`knowledge/raw/` 中的历史数据），移除已收录过的项目，避免重复采集。

### 5. 撰写中文摘要
为每个项目生成简洁的中文摘要，遵循公式：**项目名** + **做什么** + **为什么值得关注**。示例：
- "LangChain：一个用于构建 LLM 应用程序的框架，值得关注因为它提供了统一的接口连接多种 LLM 并支持链式调用。"

### 6. 排序取 Top15
按星标数降序排列，取前 15 个项目作为最终输出。如果项目数不足 15，则输出全部符合条件的项目。

### 7. 输出 JSON
将结果保存为 JSON 文件到 `knowledge/raw/github-trending-YYYY-MM-DD.json`，文件名中的日期为采集当天日期（UTC 时间）。

## 注意事项

1. **频率限制**：GitHub API 有严格的频率限制，需合理规划请求间隔，或使用认证令牌提高限额。
2. **网络错误处理**：所有网络请求必须有适当的超时和重试机制。
3. **数据完整性**：确保提取的字段完整，缺失字段使用空字符串或 `null` 填充。
4. **语言偏好**：摘要和描述优先使用中文，除非项目本身无中文资料。
5. **文件安全**：写入文件前检查目标目录是否存在，避免覆盖已有数据。
6. **隐私合规**：不采集用户个人信息，仅关注公开仓库数据。

## 输出格式

```json
{
  "source": "github_trending",
  "skill": "github-trending",
  "collected_at": "YYYY-MM-DD HH:MM:SS",
  "items": [
    {
      "name": "项目名称",
      "url": "https://github.com/owner/repo",
      "summary": "项目名做什么为什么值得关注",
      "stars": 1234,
      "language": "Python",
      "topics": ["llm", "agent", "framework"]
    }
  ]
}
```

### 字段说明
- `source`：固定为 `"github_trending"`，标识数据来源
- `skill`：固定为 `"github-trending"`，标识使用的技能
- `collected_at`：采集时间，ISO 8601 格式（UTC）
- `items`：项目数组，每个元素包含：
  - `name`：仓库名称（不含所有者）
  - `url`：完整的 GitHub 仓库 URL
  - `summary`：AI 生成的中文摘要（200-300 字）
  - `stars`：星标数（整数）
  - `language`：主要编程语言（字符串，可为空）
  - `topics`：仓库主题标签数组（字符串数组，可为空）
