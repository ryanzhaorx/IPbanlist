import re
import os

def is_valid_ipv4(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

def process_ip_content(content, output_dir="results", ips_per_file=1000):
    seen_ips = set()
    file_count = 1
    output_lines = []

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        ip_part = line.split()[0]
        if is_valid_ipv4(ip_part):
            if ip_part not in seen_ips:
                seen_ips.add(ip_part)
                output_lines.append(ip_part)

                if len(seen_ips) % ips_per_file == 0:
                    write_to_file(output_lines, f"{output_dir}/{file_count}.txt")
                    output_lines = []
                    file_count += 1

    # 写入剩余不足1000的IP
    if output_lines:
        write_to_file(output_lines, f"{output_dir}/{file_count}.txt")

    print(f"✅ 共提取 {len(seen_ips)} 个唯一IPv4地址，保存为 {file_count} 个文件。")
    return file_count

def write_to_file(lines, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    import sys
    input_url = sys.argv[1]
    import requests
    response = requests.get(input_url)
    response.raise_for_status()
    process_ip_content(response.text)
