#!/usr/bin/env python3
"""Inventory public Carlo Math pages and their embedded source assets."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


ROOT_URL = "https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/"
ROOT_PATH = "/chjs.ntpc.edu.tw/carlovemath"
USER_AGENT = "CarloMathSlidesCatalog/1.0 (+public educational inventory)"
DRIVE_ID_RE = re.compile(
    r"(?:/file/d/|[?&](?:id)=)([A-Za-z0-9_-]{10,})",
)
YOUTUBE_ID_RE = re.compile(
    r"(?:youtube\.com/(?:embed/|watch\?v=)|youtu\.be/)([A-Za-z0-9_-]{6,})",
)


def stable_url(value: str) -> str | None:
    """Return a canonical internal site URL, or None for an external link."""
    absolute = urljoin("https://sites.google.com", html.unescape(value))
    parsed = urlsplit(absolute)
    if parsed.netloc != "sites.google.com" or not parsed.path.startswith(ROOT_PATH):
        return None
    path = quote(unquote(parsed.path).rstrip("/"), safe="/")
    if path == ROOT_PATH:
        path += "/"
    return urlunsplit(("https", parsed.netloc, path, "", ""))


def clean_text(value: str) -> str:
    return " ".join(html.unescape(value).split())


class SiteParser(HTMLParser):
    """Collect page labels, metadata, and embedded asset references."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.drive_files: dict[str, str] = {}
        self.youtube_ids: set[str] = set()
        self.page_title = ""
        self.heading = ""
        self._anchor_href: str | None = None
        self._anchor_text: list[str] = []
        self._capture_title = False
        self._capture_h1 = False

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "a":
            self._anchor_href = values.get("href")
            self._anchor_text = []
        elif tag == "title":
            self._capture_title = True
        elif tag == "h1" and not self.heading:
            self._capture_h1 = True
        elif tag == "meta":
            if values.get("property") == "og:title" and values.get("content"):
                self.page_title = clean_text(values["content"])

        candidates = [
            values.get("href", ""),
            values.get("src", ""),
            values.get("data-src", ""),
        ]
        label = clean_text(values.get("aria-label", ""))
        if label.startswith("Drive,"):
            label = clean_text(label.removeprefix("Drive,"))
        for candidate in candidates:
            if not candidate:
                continue
            for file_id in DRIVE_ID_RE.findall(html.unescape(candidate)):
                current = self.drive_files.get(file_id, "")
                self.drive_files[file_id] = label or current
            self.youtube_ids.update(YOUTUBE_ID_RE.findall(html.unescape(candidate)))

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._anchor_href:
            self.links.append(
                (self._anchor_href, clean_text("".join(self._anchor_text))),
            )
            self._anchor_href = None
            self._anchor_text = []
        elif tag == "title":
            self._capture_title = False
        elif tag == "h1":
            self._capture_h1 = False

    def handle_data(self, data: str) -> None:
        if self._anchor_href:
            self._anchor_text.append(data)
        if self._capture_title and not self.page_title:
            self.page_title += data
        if self._capture_h1:
            self.heading += data


def parse_page(source: str) -> SiteParser:
    parser = SiteParser()
    parser.feed(source)

    # Some Drive and YouTube references occur only inside generated script data.
    for file_id in DRIVE_ID_RE.findall(source):
        parser.drive_files.setdefault(file_id, "")
    parser.youtube_ids.update(YOUTUBE_ID_RE.findall(source))
    parser.page_title = clean_text(parser.page_title)
    parser.heading = clean_text(parser.heading)
    return parser


def fetch(url: str, timeout: float, attempts: int = 3) -> tuple[str, str]:
    """Fetch one UTF-8 page and return source plus the final URL."""
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset, errors="replace"), response.url
        except (HTTPError, URLError, TimeoutError) as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(0.5 * (2**attempt))
    assert last_error is not None
    raise last_error


def page_record(
    url: str,
    navigation_label: str,
    timeout: float,
) -> dict[str, object]:
    try:
        source, final_url = fetch(url, timeout)
        parser = parse_page(source)
        decoded_path = unquote(urlsplit(url).path)
        path_parts = [part for part in decoded_path.split("/")[3:] if part]
        drive_files = [
            {
                "id": file_id,
                "title": title or None,
                "preview_url": f"https://drive.google.com/file/d/{file_id}/preview",
                "download_url": (
                    "https://drive.google.com/uc?export=download&id=" + file_id
                ),
            }
            for file_id, title in sorted(parser.drive_files.items())
        ]
        return {
            "url": url,
            "final_url": stable_url(final_url) or final_url,
            "navigation_label": navigation_label or None,
            "page_title": parser.page_title or None,
            "heading": parser.heading or None,
            "path_parts": path_parts,
            "drive_files": drive_files,
            "youtube_ids": sorted(parser.youtube_ids),
            "page_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "fetch_status": "ok",
            "error": None,
        }
    except Exception as error:  # Keep failed URLs visible in the inventory.
        return {
            "url": url,
            "final_url": None,
            "navigation_label": navigation_label or None,
            "page_title": None,
            "heading": None,
            "path_parts": [],
            "drive_files": [],
            "youtube_ids": [],
            "page_sha256": None,
            "fetch_status": "error",
            "error": f"{type(error).__name__}: {error}",
        }


def root_source(args: argparse.Namespace) -> tuple[str, str]:
    if args.root_html:
        path = Path(args.root_html)
        return path.read_text(encoding="utf-8"), ROOT_URL
    return fetch(ROOT_URL, args.timeout)


def discover_pages(source: str) -> dict[str, str]:
    parser = parse_page(source)
    discovered = {stable_url(ROOT_URL): "Home"}
    for href, label in parser.links:
        url = stable_url(href)
        if url:
            current = discovered.get(url, "")
            discovered[url] = label or current
    return {url: label for url, label in discovered.items() if url is not None}


def build_inventory(args: argparse.Namespace) -> dict[str, object]:
    source, final_url = root_source(args)
    discovered = discover_pages(source)
    urls = sorted(discovered)
    if args.limit:
        urls = urls[: args.limit]

    records: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(page_record, url, discovered[url], args.timeout): url
            for url in urls
        }
        for index, future in enumerate(as_completed(futures), start=1):
            record = future.result()
            records.append(record)
            status = record["fetch_status"]
            print(f"[{index:>4}/{len(urls)}] {status}: {futures[future]}", file=sys.stderr)

    records.sort(key=lambda item: str(item["url"]))
    ok_count = sum(record["fetch_status"] == "ok" for record in records)
    drive_count = sum(len(record["drive_files"]) for record in records)
    unique_drive_count = len(
        {
            asset["id"]
            for record in records
            for asset in record["drive_files"]
        },
    )
    youtube_count = len(
        {
            video_id
            for record in records
            for video_id in record["youtube_ids"]
        },
    )
    return {
        "schema_version": 1,
        "root_url": ROOT_URL,
        "root_final_url": stable_url(final_url) or final_url,
        "generated_at": datetime.now(UTC).isoformat(),
        "root_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "summary": {
            "discovered_pages": len(discovered),
            "requested_pages": len(urls),
            "fetched_pages": ok_count,
            "failed_pages": len(records) - ok_count,
            "embedded_drive_references": drive_count,
            "unique_drive_files": unique_drive_count,
            "unique_youtube_videos": youtube_count,
        },
        "pages": records,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="catalog/site_pages.json")
    parser.add_argument("--root-html", help="Use a local root HTML file for testing")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--limit", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.workers < 1 or args.workers > 12:
        raise SystemExit("--workers must be between 1 and 12")
    inventory = build_inventory(args)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(inventory["summary"], ensure_ascii=False, indent=2))
    return 1 if inventory["summary"]["failed_pages"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
