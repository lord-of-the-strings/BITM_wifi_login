import os
os.system("netsh wlan disconnect")
import requests
import time
#----ONLY CHANGE THESE THREE VALUES----#
os.system("netsh wlan connect name=CAMPUS-WIFI")
USERNAME_VALUE = "btech1013425"
PASSWORD_VALUE = "8008299586"
#----DO NOT CHANGE BELOW UNLESS YOU KNOW WHAT YOU ARE DOING----#
BASE_URL  = "http://192.168.0.2:8090"
LOGIN_URL = f"{BASE_URL}/login.xml"
session = requests.Session()
timestamp = str(int(time.time() * 1000))
payload = {
    "mode":        "191",
    "username":    USERNAME_VALUE,
    "password":    PASSWORD_VALUE,
    "a":           timestamp,
    "producttype": "0"
}
print("[*] Sending login request to Sophos...")
try:
    response = session.post(LOGIN_URL, data=payload, timeout=10)
    print(f"[*] Status code: {response.status_code}")
    print(f"[*] Response: {response.text[:500]}")
    if "You are signed in" in response.text or "logged" in response.text.lower():
        print("[+] Login SUCCESSFUL!")
    elif "Invalid" in response.text or "failed" in response.text.lower():
        print("[-] Login FAILED — check credentials")
    else:
        print("[?] Check response above to confirm login status")
except requests.exceptions.ConnectionError:
    print("[!] Cannot reach 192.168.0.2:8090 — connect to college WiFi first!")
except Exception as e:
    print(f"[!] Error: {e}")
