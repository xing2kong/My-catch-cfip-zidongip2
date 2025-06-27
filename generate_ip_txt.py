import os
import base64
import requests
import json
from urllib.parse import urlparse, unquote, parse_qs

SUBSCRIBE_URL = os.environ.get("SUBSCRIBE_URL")
if not SUBSCRIBE_URL:
    print("No SUBSCRIBE_URL found in environment variables.")
    exit(1)

print(f"Using SUBSCRIBE_URL: {SUBSCRIBE_URL}")

def parse_vmess(line):
    try:
        json_str = base64.b64decode(line[8:] + "=" * (-len(line[8:]) % 4)).decode()
        node = json.loads(json_str)
        remark = node.get("ps", "")
        address = node.get("add", "")
        port = node.get("port", "")
        return f"{address}:{port}#{remark}"
    except Exception as e:
        print(f"Error parsing vmess: {e}")
        return None

def parse_vless(line):
    try:
        # vless://uuid@host:port?params#remark
        url = urlparse(line)
        address = url.hostname
        port = url.port
        remark = unquote(url.fragment) if url.fragment else ""
        return f"{address}:{port}#{remark}"
    except Exception as e:
        print(f"Error parsing vless: {e}")
        return None

def parse_trojan(line):
    try:
        # trojan://password@host:port?params#remark
        url = urlparse(line)
        address = url.hostname
        port = url.port
        remark = unquote(url.fragment) if url.fragment else ""
        return f"{address}:{port}#{remark}"
    except Exception as e:
        print(f"Error parsing trojan: {e}")
        return None

def parse_ss(line):
    try:
        # ss://base64-encode(method:password)@host:port#remark
        url = urlparse(line)
        address = url.hostname
        port = url.port
        remark = unquote(url.fragment) if url.fragment else ""
        return f"{address}:{port}#{remark}"
    except Exception as e:
        print(f"Error parsing ss: {e}")
        return None

def main():
    resp = requests.get(SUBSCRIBE_URL, timeout=10)
    resp.raise_for_status()
    content = base64.b64decode(resp.content).decode(errors='ignore')
    lines = content.splitlines()
    print(f"Total lines in decoded content: {len(lines)}")
    result = []
    for line in lines:
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
            print(f"Parsed node: {info}")
            result.append(info)
    if not result:
        print("No valid nodes found.")
    with open("IP.TXT", "w", encoding="utf-8") as f:
        f.write("\n".join(result))

if __name__ == "__main__":
    main()
