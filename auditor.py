import argparse
import json
import sys
import requests


parser = argparse.ArgumentParser(description="Zdir-Inspired File Server Security Auditor")
parser.add_argument("-u", "--url", required=True, help="Target base URL (e.g., http://localhost:6080)")
args = parser.parse_args()


target_url = args.url.rstrip("/")


if not target_url.startswith(("http://", "https://")):
    print("[!] Warning: Protocol missing. Automatically prepending 'http://'")
    target_url = "http://" + target_url

print(f"[*] Starting security audit on: {target_url}")

sensitive_paths = [
    "/config.json",
    "/.env",
    "/backup.zip",
    "/uploads/test.txt"
]

findings = []

print("\n[*] Scanning for exposed sensitive files...")
for path in sensitive_paths:
    check_url = target_url + path
    try:

        response = requests.get(check_url, timeout=3)
        
        
        if response.status_code == 200:
            print(f"[!] HIGH RISK: Exposed file found -> {check_url}")
            findings.append({"path": path, "status": 200, "risk": "Exposed Sensitive File"})
        else:
            print(f"[-] Safe: {path} (Status: {response.status_code})")
            
    except requests.exceptions.RequestException:
        print(f"[x] Could not connect or reach: {check_url}")
        

upload_endpoint = target_url + "/post"
print("\n[*] Testing upload endpoint security...")


files = {'file': ('shell.php', '<?php echo "test"; ?>', 'application/x-php')}

try:
    response = requests.post(upload_endpoint, files=files, timeout=5)
    if response.status_code in [200, 201]:
        print(f"[!] VULNERABILITY ALERT: Upload endpoint accepted file payload! (Status: {response.status_code})")
        findings.append({"endpoint": "/post", "status": response.status_code, "risk": "Unrestricted File Upload"})
    else:
        print(f"[+] Upload endpoint properly blocked or returned status: {response.status_code}")
except requests.exceptions.RequestException:
    print("[-] Upload endpoint not active or unreachable.")


report = {
    "target": target_url,
    "total_findings": len(findings),
    "vulnerabilities": findings
}

with open("audit_report.json", "w") as f:
    json.dump(report, f, indent=4)

print(f"\n[+] Audit complete! Saved {len(findings)} findings to 'audit_report.json'")