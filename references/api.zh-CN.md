# 壁纸服务 API

简体中文 · [English](api.md)

服务地址为 `https://bing.plmeizi.com`。 [网站 API 文档](https://bing.plmeizi.com/api-docs)

| 操作 | GET 路径 | 查询参数 |
| --- | --- | --- |
| 今日壁纸 | `/api/v1/wallpapers/today` | `resolution` |
| 近期壁纸 | `/api/v1/wallpapers/recent` | `resolution` |
| 搜索壁纸 | `/api/v1/wallpapers/search` | 必填 `q`（1–100 个字符）；可选 `sort`（默认 `relevance`，也可用 `recent`）、`limit`（1–10，默认 5）、`resolution` |

当前返回中国区数据，日期使用 `Asia/Shanghai`。近期接口覆盖今天及之前九个自然日。主题搜索使用语义策略时，`sort=recent` 会在整个归档中对相关度相近的结果优先展示新图。

默认分辨率为 1920×1080。`portrait` 为 1080×1920，`4k` 和 `uhd` 为 UHD，`1080p` 为 1920×1080。完整规格见网站 API 文档。每条结果只返回一个规格的图片，其他规格可通过 `resolution` 重新请求。

响应包含 `code`、`msg` 和 `data`。成功时 `code=0`，`data.wallpapers` 中的每条壁纸包含 `title`、`date`、`copyright`、`source_url`、`url`、`resolution`、`width` 和 `height`。其中 `url` 是官方图片地址，`source_url` 是原始介绍来源。搜索响应另含 `data.sort`，每条搜索结果的 `page_url` 指向本站详情页。

| HTTP 状态 | 处理方式 |
| --- | --- |
| 400 | 检查并修正输入参数。 |
| 403 | 访问受限。 |
| 404（今日接口） | 今日壁纸暂不可用。 |
| 429 | 请求受限，等待后再试。 |
| 503 | 服务不可用或繁忙。 |

脚本也处理 HTTP 错误中的非 JSON 响应。服务端提供数字形式的 `Retry-After` 时，脚本会输出等待秒数。请避免自动循环重试。

完整日期（如 `2026-11-04` 或 `11.04 2026`）走精确查询。读取 `data.strategy` 区分 `semantic`（语义检索）、`date`（精确日期）和 `keyword`（关键词降级）。关键词降级会在标题、版权信息和描述中匹配所有查询词，再按日期倒序返回。

添加 `--verbose` 可将操作、状态和耗时输出到 stderr。stdout 保持 JSON，便于自动化处理。
