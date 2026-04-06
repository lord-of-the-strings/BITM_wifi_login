import os, time, re, requests, subprocess
from requests.adapters import HTTPAdapter
from urllib3.util.connection import create_connection
from urllib3.poolmanager import PoolManager
import socket

os.system("netsh wlan disconnect")
time.sleep(2)
os.system("netsh wlan connect name=xxxxx") #replace by wifi name

USERNAME_VALUE = "xxxxxx" #replace by username
PASSWORD_VALUE = "xxxxxx" #replace by password

BASE_URL  = "http://192.168.0.2:8090" #replace by base url of captive portal
LOGIN_URL = f"{BASE_URL}/login.xml"

# ── Get the IP of the connected adapter ───────────────
def get_wifi_ip():
    result = subprocess.run("ipconfig", capture_output=True, text=True)
    # Find block with 192.168.0.2's subnet OR just grab first active IPv4
    blocks = result.stdout.split("\n\n")
    for block in blocks:
        if "172.16." in block or "192.168." in block:
            match = re.search(r"IPv4 Address.*?:\s+([\d.]+)", block)
            if match:
                return match.group(1)
    return None

# ── Wait for IP ────────────────────────────────────────
print("[*] Waiting for IP...")
my_ip = None
for _ in range(30):
    my_ip = get_wifi_ip()
    if my_ip:
        print(f"[*] Using interface IP: {my_ip}")
        break
    time.sleep(2)
else:
    print("[!] No IP found.")
    exit(1)

# ── Custom adapter that binds to our interface ─────────
class SourceAddressAdapter(HTTPAdapter):
    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['source_address'] = (self.source_address, 0)
        super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount("http://", SourceAddressAdapter(my_ip))

# ── Wait for portal ────────────────────────────────────
print("[*] Probing portal...")
for attempt in range(20):
    try:
        session.get(f"{BASE_URL}/httpclient.html", timeout=5)
        print("[*] Portal reachable!")
        break
    except Exception as e:
        print(f"[.] ({attempt+1}/20) {e}")
        time.sleep(3)
else:
    print("[!] Portal unreachable.")
    exit(1)

# ── Login ──────────────────────────────────────────────
payload = {
    "mode":        "191",
    "username":    USERNAME_VALUE,
    "password":    PASSWORD_VALUE,
    "a":           str(int(time.time() * 1000)),
    "producttype": "0"
}

try:
    r = session.post(LOGIN_URL, data=payload, timeout=10)
    print(f"[*] Response: {r.text[:300]}")
    if "signed in" in r.text.lower():
        print("[+] Login SUCCESSFUL!")
    elif "invalid" in r.text.lower() or "failed" in r.text.lower():
        print("[-] Wrong credentials")
    else:
        print("[?] Check response above")
except Exception as e:
    print(f"[!] Error: {e}")
