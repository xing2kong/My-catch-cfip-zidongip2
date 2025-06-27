import os
import base64
import requests
import json
from urllib.parse import urlparse, unquote

SUBSCRIBE_URL = os.environ.get("SUBSCRIBE_URL")
if not SUBSCRIBE_URL:
    print("No SUBSCRIBE_URL found in environment variables.")
    exit(1)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

def parse_vmess(line):
    try:
        data = base64.b64decode(line[8:] + "=" * (-len(line[8:]) % 4)).decode('utf-8')
        node = json.loads(data)
        address = node.get("add", "")
        port = node.get("port", "")
        remark = node.get("ps", "")
        return f"{address}:{port}#{remark}"
    except Exception:
        return None

def parse_vless(line):
    try:
        url = urlparse(line)
        address = url.hostname
        port = url.port
        remark = unquote(url.fragment) if url.fragment else ""
        return f"{address}:{port}#{remark}"
    except Exception:
        return None

def parse_trojan(line):
    try:
        url = urlparse(line)
        address = url.hostname
        port = url.port
        remark = unquote(url.fragment) if url.fragment else ""
        return f"{address}:{port}#{remark}"
    except Exception:
        return None

def parse_ss(line):
    try:
        url = urlparse(line)
        address = url.hostname
        port = url.port
        remark = unquote(url.fragment) if url.fragment else ""
        return f"{address}:{port}#{remark}"
    except Exception:
        return None

def main():
    resp = requests.get(SUBSCRIBE_URL, headers=headers, timeout=10)
    raw_content = resp.content
    try:
        decoded = base64.b64decode(raw_content + b"=" * (-len(raw_content) % 4)).decode('utf-8', errors='ignore')
    except Exception:
        decoded = raw_content.decode('utf-8', errors='ignore')
    lines = decoded.splitlines()
    result = []
    for line in lines:
        line = line.strip()
        if line.startswith("vmess://"):
            info = parse_vmess(line)
        elif line.startswith("vless://"):
            info = parse_vless(line)
        elif line.startswith("trojan://"):
            info = parse_trojan(line)
        elif line.startswith("ss://"):
            info = parse_ss(line)
        else:
            info = None
        if info:
            result.append(info)
    with open("IP.TXT", "w", encoding="utf-8") as f:
        f.write("\n".join(result))

if __name__ == "__main__":
    main()
