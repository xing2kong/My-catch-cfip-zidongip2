import os
import requests
from urllib.parse import urlparse, unquote

SUBSCRIBE_URL = os.environ.get("SUBSCRIBE_URL")
if not SUBSCRIBE_URL:
    print("No SUBSCRIBE_URL found in environment variables.")
    exit(1)

print(f"Using SUBSCRIBE_URL: {SUBSCRIBE_URL}")

def parse_node(line):
    if line.startswith("vmess://") or line.startswith("vless://") or line.startswith("trojan://") or line.startswith("ss://"):
        # 解析主机和端口
        try:
            url = urlparse(line)
            address = url.hostname
            port = url.port
            remark = unquote(url.fragment) if url.fragment else ""
            return f"{address}:{port}#{remark}"
        except Exception as e:
            print(f"Error parsing: {e}")
            return None
    return None

def main():
    resp = requests.get(SUBSCRIBE_URL, timeout=10)
    content = resp.text
    print("==== 订阅内容前10行 ====")
    for i, line in enumerate(content.splitlines()[:10]):
        print(f"{i+1}: {line}")
    lines = content.splitlines()
    print(f"Total lines: {len(lines)}")
    result = []
    for line in lines:
        info = parse_node(line.strip())
        if info:
            print(f"Parsed node: {info}")
            result.append(info)
    if not result:
        print("No valid nodes found.")
    with open("IP.TXT", "w", encoding="utf-8") as f:
        f.write("\n".join(result))

if __name__ == "__main__":
    main()
