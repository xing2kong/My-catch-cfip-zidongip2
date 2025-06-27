import os
import base64
import requests
import json
from urllib.parse import urlparse, unquote

SUBSCRIBE_URL = os.environ.get("SUBSCRIBE_URL")
if not SUBSCRIBE_URL:
    print("No SUBSCRIBE_URL found in environment variables.")
    exit(1)

print(f"Using SUBSCRIBE_URL: {SUBSCRIBE_URL}")

headers = {
    "User-Agent": "clash"
}

def parse_vmess(line):
    try:
        data = base64.b64decode(line[8:] + "=" * (-len(line[8:]) % 4)).decode('utf-8')
        node = json.loads(data)
        address = node.get("add", "")
        port = node.get("port", "")
        remark = node.get("ps", "")
        return f"{address}:{port}#{remark}"
    except Exception as e:
        print(f"Error parsing vmess: {e}")
        return None

def parse_vless(line):
    try:
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
        url = urlparse(line)
        address = url.hostname
        port = url.port
        remark = unquote(url.fragment) if url.fragment else ""
        return f"{address}:{port}#{remark}"
    except Exception as e:
        print(f"Error parsing ss: {e}")
        return None

def main():
    try:
        resp = requests.get(SUBSCRIBE_URL, headers=headers, timeout=10)
        raw_content = resp.content
        try:
            decoded = base64.b64decode(raw_content + b"=" * (-len(raw_content) % 4)).decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Base64 decode failed: {e}")
            decoded = raw_content.decode('utf-8', errors='ignore')
        print("==== 解码后内容前10行 ====")
        for i, line in enumerate(decoded.splitlines()[:10]):
            print(f"{i+1}: {line}")
        lines = decoded.splitlines()
        print(f"Total lines: {len(lines)}")
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
                print(f"Parsed node: {info}")
                result.append(info)
        if not result:
            print("No valid nodes found.")
        with open("IP.TXT", "w", encoding="utf-8") as f:
            f.write("\n".join(result))
    except Exception as e:
        print(f"Failed to fetch or process subscribe url: {e}")

if __name__ == "__main__":
    main()
