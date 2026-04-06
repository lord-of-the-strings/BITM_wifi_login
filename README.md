# BITM WiFi Login Automator

Automatically logs into the BITM hostel/campus Wi-Fi on every system restart — no more typing credentials manually.

> **Requirements:** Python 3.x | Windows

---

## ⚡ Quick Setup

1. **Clone this repository**
```bash
   git clone https://github.com/trinayan-zenez/BITM_wifi_login.git
```

2. **Find your Python path**
   Open CMD and run:
```bash
   where python
```
   Copy the output path (e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python3x\python.exe`)

3. **Import the Task Scheduler task**
   - Open **Task Scheduler**
   - Click **Import Task** and select `wifi.xml`

4. **Edit the task action**
   - Go to the **Actions** tab → select the action → click **Edit**
   - **Program/script:** Paste your Python path from Step 2
   - **Arguments:** Paste the full path to `hostel_wifi.py`
   - **Start in:** Paste the path to the folder containing `hostel_wifi.py`

5. **Save and you're done!** 🎉  
   The script will now run automatically on every restart.

---

## 📁 Files
| File | Description |
|------|-------------|
| `hostel_wifi.py` | Main login automation script |
| `wifi.xml` | Pre-configured Task Scheduler task |

---

## 📝 Note
Make sure to update your Wi-Fi credentials inside `hostel_wifi.py` before running.
