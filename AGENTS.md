# AI 知识库助手 Agent 系统设计

## 项目概述
AI 知识库助手是一个自动化系统，用于从 GitHub Trending 和 Hacker News 采集 AI/LLM/Agent 领域的技术动态，通过 AI 分析提取结构化信息并存储为 JSON，最后支持通过 Telegram、飞书等多渠道进行分发。

## 技术栈
- **Python**: 3.12+
- **AI 框架**: OpenCode + 国产大模型 (如 DeepSeek、Qwen 等)
- **工作流引擎**: LangGraph
- **采集工具**: OpenClaw (网页抓取)
- **数据存储**: JSON 文件 (后期可扩展至数据库)
- **消息推送**: Telegram Bot API、飞书机器人 API

## 编码规范
1. **代码风格**: 遵循 PEP 8，使用 snake_case 命名
2. **文档字符串**: 使用 Google 风格 docstring，所有函数、类、模块需包含完整的文档说明
3. **日志输出**: 禁止使用裸 `print()`，统一使用 `loguru` 模块
4. **错误处理**: 使用明确的异常类型，避免裸露的 `except`
5. **类型注解**: 推荐使用 Python 类型注解提高代码可读性
6. **导入顺序**: 标准库 → 第三方库 → 本地模块，每组之间空一行

## 项目结构
```
.ai-knowledge-base/
├── .opencode/
│   ├── agents/                # Agent 角色定义文件
│   │   ├── collector.md
│   │   ├── analyzer.md
│   │   └── curator.md
│   └── skills/                # 可复用技能包
│       ├── github_trending/
│       │   └── SKILL.md
│       ├── hackernews/
│       │   └── SKILL.md
│       ├── llm_analysis/
│       │   └── SKILL.md
│       └── notification/
│           └── SKILL.md
├── knowledge/
│   ├── raw/             # 原始采集数据 (JSON 格式)
│   │   ├── github/
│   │   └── hackernews/
│   └── articles/        # 分析后的结构化知识条目
├── config/              # 配置文件
├── logs/                # 日志文件
├── tests/               # 单元测试
└── AGENTS.md            # 本文档
```

## 知识条目 JSON 格式
```json
{
  "id": "uuid4 或基于时间戳的唯一标识",
  "title": "文章/项目标题",
  "source_url": "原始链接",
  "source_type": "github_trending | hackernews",
  "summary": "AI 生成的摘要 (200-300 字)",
  "key_points": ["要点1", "要点2", "要点3"],
  "tags": ["llm", "agent", "framework", "tool"],
  "technical_level": "beginner | intermediate | advanced",
  "language": "zh | en",
  "published_at": "YYYY-MM-DD HH:MM:SS",
  "collected_at": "YYYY-MM-DD HH:MM:SS",
  "analyzed_at": "YYYY-MM-DD HH:MM:SS",
  "status": "collected | analyzed | curated | published",
  "metadata": {
    "github_stars": 1234,
    "hackernews_score": 42,
    "comment_count": 10
  }
}
```

## Agent 角色概览

| 角色 | 职责 | 主要工具 | 输出 |
|------|------|----------|------|
| **采集器 (Collector)** | 定期从 GitHub Trending 和 Hacker News 抓取内容 | OpenClaw、Requests、BeautifulSoup | 原始 JSON 数据，保存至 `knowledge/raw/` |
| **分析器 (Analyzer)** | 使用 LLM 对原始内容进行摘要、标签分类、技术难度评估 | OpenCode、国产大模型、LangChain | 结构化知识条目，保存至 `knowledge/articles/` |
| **整理器 (Curator)** | 审核分析结果，去重，补充元数据，触发分发 | 相似度计算、规则引擎 | 更新条目状态，生成分发消息 |

### 工作流示意
```
采集器 → (原始数据) → 分析器 → (结构化条目) → 整理器 → (分发消息) → 推送渠道
```

## 红线（绝对禁止的操作）
1. **禁止硬编码密钥/令牌**: 所有敏感配置必须通过环境变量或配置文件读取
2. **禁止直接打印敏感信息**: 日志中不得出现 API Key、Token 等敏感数据
3. **禁止未经处理的异常**: 所有网络请求、文件操作必须有适当的错误处理
4. **禁止覆盖已有数据**: 写入文件时必须检查目标文件是否存在，避免意外覆盖
5. **禁止高频请求**: 采集时必须遵守目标网站的 robots.txt 和频率限制
6. **禁止分发未审核内容**: 所有推送的内容必须经过整理器审核，状态为 `curated` 或 `published`
7. **禁止在代码中写死路径**: 使用相对路径或配置化的绝对路径
8. **禁止在 Agent 中写死模型名称**: 模型配置应通过外部配置管理

## 后续扩展方向
- 增加更多数据源 (arXiv、Twitter、Reddit)
- 支持向量数据库存储与语义检索
- 实现个性化推荐与订阅功能
- 添加 Web 管理界面
- 集成更多消息渠道 (钉钉、微信、Slack)