import os
import base64
import requests
import json

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
        print(f"Error parsing line: {line[:30]}..., error: {e}")
        return None

def main():
    try:
        resp = requests.get(SUBSCRIBE_URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch subscribe url: {e}")
        exit(1)

    try:
        content = base64.b64decode(resp.content).decode(errors='ignore')
    except Exception as e:
        print(f"Failed to base64 decode response content: {e}")
        exit(1)

    lines = content.splitlines()
    print(f"Total lines in decoded content: {len(lines)}")
    result = []
    for line in lines:
        if line.startswith("vmess://"):
            info = parse_vmess(line)
            if info:
                print(f"Parsed node: {info}")
                result.append(info)
    if not result:
        print("No vmess nodes found.")
    with open("IP.TXT", "w", encoding="utf-8") as f:
        f.write("\n".join(result))

if __name__ == "__main__":
    main()
