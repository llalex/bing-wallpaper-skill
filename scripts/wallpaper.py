#!/usr/bin/env python3
"""Read the Bing wallpaper service using only the Python standard library."""
import argparse
import json
import sys
from time import monotonic
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

SITE = "https://bing.plmeizi.com"
MAX_BODY = 256 * 1024


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def fetch(url):
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "bing-wallpaper-skill/0.1"})
    # Semantic search may need to warm the model before responding.
    timeout = 25 if urlsplit(url).path.endswith("/search") else 10
    with build_opener(NoRedirect()).open(request, timeout=timeout) as response:
        raw = response.read(MAX_BODY + 1)
        if len(raw) > MAX_BODY:
            raise ValueError("response is too large")
        return json.loads(raw.decode("utf-8"))


def output(data):
    # ASCII JSON escapes are reversible and work in non-UTF-8 Windows shells.
    print(json.dumps(data, ensure_ascii=True))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["today", "recent", "search"])
    parser.add_argument("--query")
    parser.add_argument("--sort", choices=["relevance", "recent"])
    parser.add_argument("--limit", type=int, choices=range(1, 11))
    parser.add_argument("--resolution")
    parser.add_argument("--base-url", default=SITE, help="Override service origin for local testing")
    parser.add_argument("--verbose", action="store_true", help="Write request diagnostics to stderr")
    args = parser.parse_args(argv)
    try:
        origin = urlsplit(args.base_url)
        local = origin.hostname in ("localhost", "127.0.0.1", "::1")
        if not origin.hostname or origin.username is not None or origin.password is not None or (
            origin.scheme != "https" and not (origin.scheme == "http" and local)
        ) or origin.path not in ("", "/") or origin.query or origin.fragment:
            raise ValueError
        origin.port  # Reject malformed ports before issuing a request.
    except ValueError:
        parser.error("--base-url must be an HTTPS origin or a loopback HTTP origin")

    params = {}
    if args.resolution is not None:
        params["resolution"] = args.resolution
    if args.operation == "search":
        query = (args.query or "").strip()
        if not 1 <= len(query) <= 100:
            parser.error("search requires --query with 1 to 100 characters")
        params.update(q=query, sort=args.sort or "relevance", limit=args.limit or 5)
    elif args.query is not None or args.sort is not None or args.limit is not None:
        parser.error("--query, --sort and --limit apply to search only")

    url = args.base_url.rstrip("/") + "/api/v1/wallpapers/" + args.operation
    if params:
        url += "?" + urlencode(params)
    try:
        started = monotonic()
        body = fetch(url)
        if not isinstance(body, dict) or body.get("code") != 0 or not isinstance(body.get("data"), dict):
            raise ValueError("invalid response envelope")
        if not isinstance(body["data"].get("wallpapers"), list):
            raise ValueError("invalid result list")
        if args.operation == "search" and body["data"].get("sort") != params["sort"]:
            raise ValueError("requested ordering was not applied")
        if args.verbose:
            print("operation={} code=0 count={} elapsed_ms={:.0f}".format(
                args.operation, len(body["data"]["wallpapers"]), (monotonic() - started) * 1000
            ), file=sys.stderr)
        output(body)
        return 0
    except HTTPError as error:
        body = {"code": error.code, "msg": error.reason, "data": None}
        try:
            payload = json.loads(error.read(MAX_BODY).decode("utf-8"))
            if isinstance(payload, dict) and isinstance(payload.get("msg"), str):
                body["msg"] = payload["msg"]
        except (ValueError, OSError):
            pass
        retry_after = (error.headers or {}).get("Retry-After", "")
        if 1 <= len(retry_after) <= 9 and all("0" <= digit <= "9" for digit in retry_after):
            body["retry_after"] = int(retry_after)
        error.close()
    except (URLError, OSError):
        body = {"code": 503, "msg": "Wallpaper service could not be reached", "data": None}
    except ValueError:
        body = {"code": 502, "msg": "Invalid wallpaper service response", "data": None}
    # Keep stdout as a single JSON object for the agent to consume.
    if args.verbose:
        print("operation={} code={} elapsed_ms={:.0f}".format(
            args.operation, body["code"], (monotonic() - started) * 1000
        ), file=sys.stderr)
    output(body)
    return 1


if __name__ == "__main__":
    sys.exit(main())
