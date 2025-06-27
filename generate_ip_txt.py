import os
import base64
import requests
import json

SUBSCRIBE_URL = os.environ.get("SUBSCRIBE_URL")

def parse_vmess(line):
    try:
        json_str = base64.b64decode(line[8:] + "=" * (-len(line[8:]) % 4)).decode()
        node = json.loads(json_str)
        remark = node.get("ps", "")
        address = node.get("add", "")
        port = node.get("port", "")
        return f"{address}:{port}#{remark}"
    except Exception:
        return None

def main():
    resp = requests.get(SUBSCRIBE_URL, timeout=10)
    content = base64.b64decode(resp.content).decode(errors='ignore')
    lines = content.splitlines()
    result = []
    for line in lines:
        if line.startswith("vmess://"):
            info = parse_vmess(line)
            if info:
                result.append(info)
    with open("IP.TXT", "w", encoding="utf-8") as f:
        f.write("\n".join(result))

if __name__ == "__main__":
    main()
