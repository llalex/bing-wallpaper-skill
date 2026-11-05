# Bing Wallpaper

[简体中文](README.md) · English

Find Bing wallpapers for China with natural language. Browse today's wallpaper or the last ten calendar days, or search by theme or exact date. Results include official Bing image links for desktops, phones, or 4K displays. [Wallpaper site](https://bing.plmeizi.com/) · [Public API](https://bing.plmeizi.com/api-docs)

## Install

Your client's execution environment needs **Python 3.8+** and HTTPS access to `bing.plmeizi.com`. No API key or third-party Python packages are required. Run `python --version` to check which Python the environment can find.

### Install from the terminal

Choose one command for your client and run it from your workspace. The Skills CLI requires Node.js 22.20+.

| Client | Command |
| --- | --- |
| Codex | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent codex` |
| Claude Code | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent claude-code` |
| Gemini CLI | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent gemini-cli` |
| Cursor | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent cursor` |
| OpenCode | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent opencode` |
| DeepSeek Harness | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill --agent codex` |
| Other supported clients (interactive selection) | `npx skills@latest add https://github.com/llalex/bing-wallpaper-skill --skill bing-wallpaper-skill` |

DeepSeek Harness reads the shared `.agents/skills/` directory that the Codex target writes to. Open the same workspace in Harness.
[Skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) · [DeepSeek Harness](https://deepseek-harness.github.io/deepseek-harness/en/reference/subsystems/skills)

Gemini CLI also offers a built-in installer.

```sh
gemini skills install https://github.com/llalex/bing-wallpaper-skill.git --scope workspace
```

[Gemini CLI skill documentation](https://geminicli.com/docs/cli/skills/)

### Install in WorkBuddy

- **Skills Market** — Once listed, open **Experts, Skills, and Connectors → Skills → Skills Market**, search for **Bing Wallpaper** (必应壁纸), and click **+**.
- **Before the listing goes live** — Select **Code → Download ZIP** in this repository. In WorkBuddy, open **Skills → Add Skill → Upload Skill** and upload the ZIP. Check that the skill is enabled, then start a new task. [Official WorkBuddy installation guide](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)

## Use

Start a new chat and try one of these prompts.

- “Give me today's Bing wallpaper for my phone.”
- “Show me recent Bing wallpapers in 4K.”
- “Find three newer Bing wallpapers about the sun.”
- “Find the Bing wallpaper for November 4, 2026.”
- “Download the first wallpaper to the current workspace.”

If your client shows an execution trace, check that it loaded `bing-wallpaper-skill` and ran `scripts/wallpaper.py`. For example, a request for today's phone wallpaper should run `today --resolution portrait`. If the skill does not load, check the workspace and skill directory. If the script fails to start, check Python and network access.

### Run the script directly

Run these commands from the repository root. The script outputs JSON.

```sh
python scripts/wallpaper.py today --resolution portrait
python scripts/wallpaper.py recent --resolution 4k
python scripts/wallpaper.py search --query "太阳" --sort recent --limit 3
python scripts/wallpaper.py search --query "2026-11-04"
```

Theme search returns up to five results by default. Set `--limit` to 1–10 to change that. In semantic search, `--sort recent` favors newer results within similar relevance bands. Keyword fallback orders results by date, newest first. Add `--verbose` to see the request status and elapsed time. [API parameters and error handling](references/api.md)

## Downloads and image rights

The script queries JSON. To save an image, use a client or browser that can open the returned `url` and save the file. In search results, `page_url` links to the wallpaper site's detail page and `source_url` links to the original description. Image rights belong to the original creators or respective rights holders. Keep the image credits and follow the applicable terms.

## License

The skill code and documentation are available under the [MIT License](LICENSE).
