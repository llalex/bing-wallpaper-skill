# Wallpaper service API

[简体中文](api.zh-CN.md) · English

Service origin: https://bing.plmeizi.com. [Website API documentation](https://bing.plmeizi.com/api-docs).

| Operation | GET path | Query parameters |
| --- | --- | --- |
| Today | /api/v1/wallpapers/today | resolution |
| Recent days | /api/v1/wallpapers/recent | resolution |
| Search | /api/v1/wallpapers/search | q (1–100 characters), sort (relevance or recent), limit (1–10, default 5), resolution |

Data is for China and dates use Asia/Shanghai. The recent-days endpoint covers today and the previous nine calendar days. When the search strategy is semantic, sort=recent prefers newer dates within close relevance bands across the archive.

Resolution defaults to 1920x1080; portrait = 1080x1920, 4k/uhd = UHD, and 1080p = 1920x1080. Refer to the site documentation for all supported sizes. Each result has one image. Do not invent links by substituting sizes in URLs.

Responses use code/msg/data. Success is code=0; data.wallpapers contains title, date, copyright, source_url, url, resolution, width and height. Search includes data.sort and a page_url per result; use page_url as the provider's detail link. The image URL and original source URL are separate fields.

HTTP 400: fix input; 403: access blocked; 404 today: not yet available; 429: wait; 503: unavailable or busy. The script also handles non-JSON HTTP failures and reports Retry-After when the server provides a numeric delay. Do not automatically retry in a loop.

Full dates such as 2026-11-04 and 11.04 2026 use exact lookup. Read data.strategy to distinguish semantic, date and keyword. Keyword fallback matches all terms across titles, credits and descriptions, then sorts by date.

Add --verbose to log the operation, status and elapsed time to stderr. Stdout remains JSON for automation.
