---
name: github-trending
description: 当需要采集 GitHub 热门开源项目时使用此技能。适用于知识库采集阶段。
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
---

# GitHub 热门项目采集技能

## 使用场景
在知识库采集阶段，从 GitHub 搜索并采集 AI 领域热门开源项目。

## 执行步骤

### 第 1 步：搜索热门仓库
**方法一（推荐）**: 使用 GitHub API 搜索近期热门仓库  
GET https://api.github.com/search/repositories?q=created:>{7天前日期}+stars:>100&sort=stars&order=desc&per_page=30

**方法二（备选）**: 如果 API 频率受限，可解析 GitHub Trending 页面  
采集多个时间段确保数量：`daily`、`weekly`、`monthly`，合并后去重

### 第 2 步：提取仓库信息
提取 name, full_name, html_url, description, stargazers_count, language, topics

### 第 3 步：过滤
纳入：AI/ML/LLM/Agent 相关、开发者工具、框架重大更新
排除：Awesome 列表、纯教程、Star 刷量、无 README

### 第 4 步：去重
按 full_name 去重，只保留一条

### 第 5 步：撰写中文摘要
公式：[项目名] + 做什么 + 为什么值得关注

### 第 6 步：排序取 Top 15
按 Star 数降序排列

### 第 7 步：输出 JSON
路径：knowledge/raw/github-trending-{YYYY-MM-DD}.json

## 注意事项
- GitHub API 未认证限频 10 次/分钟
- 摘要必须是中文
- 不编造不存在的仓库规范
- 确保最终 AI 相关项目数量 ≥ 15，可从多个时间段采集或调整 API 查询参数

## 输出格式

```json
{
  "source": "github_trending",
  "skill": "github-trending",
  "collected_at": "YYYY-MM-DD HH:MM:SS",
  "items": [
    {
      "name": "项目名称",
      "full_name": "所有者/仓库名",
      "url": "https://github.com/owner/repo",
      "description": "项目描述",
      "summary": "项目名做什么为什么值得关注",
      "stars": 1234,
      "language": "Python",
      "topics": ["llm", "agent", "framework"],
      "created_at": "仓库创建时间"
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
  - `full_name`：所有者/仓库名
  - `url`：完整的 GitHub 仓库 URL
  - `description`：项目描述（原始英文或中文翻译）
  - `summary`：生成的中文摘要（遵循公式：项目名+做什么+为什么值得关注）
  - `stars`：星标数（整数）
  - `language`：主要编程语言（字符串，可为空）
  - `topics`：仓库主题标签数组（字符串数组，可为空）
  - `created_at`：仓库创建时间（ISO 8601 格式）