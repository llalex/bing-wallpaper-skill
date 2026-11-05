# 必应壁纸

简体中文 · [English](README.en.md)

用自然语言查找中国区必应壁纸。支持今日、最近十个自然日、主题和完整日期查询，提供桌面、手机竖屏或 4K 的 Bing 官方图片链接。 [壁纸站](https://bing.plmeizi.com/) · [开放 API](https://bing.plmeizi.com/api-docs)

## 安装

客户端的执行环境需要 **Python 3.8+**，并能通过 HTTPS 访问 `bing.plmeizi.com`。无需 API Key 或第三方 Python 包。可以用 `python --version` 检查客户端能找到的 Python。

### 终端安装

在工作区运行与你的客户端对应的一条命令。Skills CLI 需要 Node.js 22.20+。

| 客户端 | 安装命令 |
| --- | --- |
| Codex | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent codex` |
| Claude Code | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent claude-code` |
| Gemini CLI | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent gemini-cli` |
| Cursor | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent cursor` |
| OpenCode | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent opencode` |
| DeepSeek Harness | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent codex` |
| 其他受支持的客户端（交互选择） | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill` |

DeepSeek Harness 会读取 Codex 安装目标写入的共享目录 `.agents/skills/`。安装后用 Harness 打开同一工作区。
[Skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) · [DeepSeek Harness](https://deepseek-harness.github.io/deepseek-harness/en/reference/subsystems/skills)

Gemini CLI 也可以用自带命令直接安装。

```sh
gemini skills install https://github.com/llalex/bing-wallpaper-skill.git --scope workspace
```

[Gemini CLI 技能文档](https://geminicli.com/docs/cli/skills/)

### WorkBuddy 官方安装

- **技能市场**：上架后，打开「专家·技能·连接器 → 技能 → 技能市场」，搜索「必应壁纸」，点击技能卡片上的 **+** 安装。
- **上架前**：在本仓库选择 **Code → Download ZIP**。打开 WorkBuddy 的「技能 → 添加技能 → 上传技能」，直接导入 ZIP。安装后确认技能已启用，再新建任务。 [WorkBuddy 官方安装指南](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)

## 使用

安装后，直接在新对话中说：

- 「给我今天的手机壁纸」
- 「给我最近的 4K 必应壁纸」
- 「找三张较新的太阳壁纸」
- 「查 2026 年 11 月 4 日的必应壁纸」
- 「把第一张壁纸下载到当前工作区」

如果客户端提供执行记录，可以确认它加载了 `bing-wallpaper-skill` 并调用了 `scripts/wallpaper.py`。例如，「今天的手机壁纸」应调用 `today --resolution portrait`。如果未触发，先确认当前工作区和技能目录；如果脚本启动失败，再检查 Python 和网络。

### 直接运行脚本

从仓库根目录运行，结果以 JSON 输出。

```sh
python scripts/wallpaper.py today --resolution portrait
python scripts/wallpaper.py recent --resolution 4k
python scripts/wallpaper.py search --query "太阳" --sort recent --limit 3
python scripts/wallpaper.py search --query "2026-11-04"
```

主题搜索默认返回最多 5 条，`--limit` 可设为 1–10。语义策略下，`--sort recent` 会在相关度相近的结果中优先展示新图；关键词降级按日期倒序。排查时可加 `--verbose` 查看请求状态和耗时。 [API 参数与错误处理](references/api.zh-CN.md) · [Skill 指令](references/skill.zh-CN.md)

## 下载与版权

脚本查询 JSON。下载时，由具备文件保存能力的客户端或浏览器直接访问结果中的 `url`。搜索结果的 `page_url` 指向壁纸站详情页，`source_url` 指向原始介绍来源。图片版权归原作者或相应权利人所有，请保留版权信息并按授权使用。

## 许可证

Skill 代码和文档采用 [MIT 许可证](LICENSE)。
