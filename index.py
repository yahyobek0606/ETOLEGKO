#!/usr/bin/env python3
"""Measure download speed by fetching a URL several times sequentially.

Usage: python3 index.py <url> [--count N]
Requires Python 3.7+, no third-party packages.
"""

import argparse
import http.client
import sys
import time
import urllib.error
import urllib.request

from const import CHUNK_SIZE, BYTES_IN_MB

def download(url):
    """Download the full response body. Returns (bytes_received, seconds)."""
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "index-script/1.0",
            "Cache-Control": "no-cache",
            "Accept-Encoding": "identity",
        },
    )
    received = 0
    start = time.perf_counter()
    with urllib.request.urlopen(request, timeout=60) as response:
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            received += len(chunk)
    elapsed = time.perf_counter() - start
    return received, elapsed


def main():
    parser = argparse.ArgumentParser(description="Measure download speed of a URL.")
    parser.add_argument("url", help="address to download, e.g. a large image")
    parser.add_argument(
        "-n", "--count", type=int, default=10, help="number of requests (default: 10)"
    )
    args = parser.parse_args()

    if not args.url.startswith(("http://", "https://")):
        parser.error("URL must start with http:// or https://")
    if args.count < 1:
        parser.error("--count must be at least 1")

    total_bytes = 0
    total_time = 0.0

    print(f"Downloading {args.url} {args.count} times...\n", flush=True)
    for i in range(1, args.count + 1):
        try:
            size, elapsed = download(args.url)
        except urllib.error.HTTPError as e:
            print(f"Request {i}: HTTP error {e.code} {e.reason}", file=sys.stderr)
            return 1
        except (urllib.error.URLError, http.client.HTTPException, OSError) as e:
            reason = getattr(e, "reason", e)
            print(f"Request {i}: network error: {reason}", file=sys.stderr)
            return 1

        total_bytes += size
        total_time += elapsed
        speed = size / BYTES_IN_MB / elapsed if elapsed > 0 else 0.0
        print(
            f"Request {i:>2}/{args.count}: {elapsed:7.3f} s  "
            f"{size / BYTES_IN_MB:9.3f} MB  {speed:8.2f} MB/s",
            flush=True,
        )

    avg_time = total_time / args.count
    avg_speed = total_bytes / BYTES_IN_MB / total_time if total_time > 0 else 0.0

    print()
    print(f"Average request time: {avg_time:.3f} s")
    print(f"Total downloaded:     {total_bytes / BYTES_IN_MB:.3f} MB ({total_bytes} bytes)")
    print(f"Download speed:       {avg_speed:.2f} MB/s")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)
