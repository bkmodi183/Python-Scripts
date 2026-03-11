# Disk Monitoring Script

## **Purpose**

This Python script continuously monitors all disk partitions on a server.

* It checks disk usage every **10 seconds**.
* If any disk stays above a threshold (default **90%**) for **5 minutes**, it automatically sends an **email alert**.
* The script can be run in **real-time** as a background service on **Windows** or **Linux**, so no manual intervention is needed.

This is useful for **server monitoring**, **preventing disk full issues**, and **proactive system maintenance**.

---

## **Script Explanation**

Key points in the script:

1. **Disk Measurement**

```python
usage = psutil.disk_usage(part.mountpoint)
percent_used = usage.percent
```

* Measures disk usage as a percentage of total space for each partition.
* `psutil.disk_partitions()` lists all mounted drives/partitions.

2. **Threshold Check**

```python
if percent_used > DISK_THRESHOLD:
    high_disk_count[part.device] += 1
```

* If disk usage exceeds threshold (e.g., 90%), a counter increases for that partition.
* If usage drops below threshold, the counter resets.

3. **Alert Trigger**

```python
if high_disk_count[part.device] >= required_count:
    disk_info_for_alert[part.device] = percent_used
    high_disk_count[part.device] = 0
```

* If disk usage remains above the threshold for **5 minutes** (30 consecutive readings at 10-second intervals), the script sends an email alert.
* Each partition is tracked separately.

4. **Email Sending**

```python
smtplib.SMTP("smtp.gmail.com", 587)
```

* Sends email via Gmail SMTP.
* Replace `SENDER_EMAIL` with your email (e.g., `sendermailid@gmail.com`) and `SENDER_PASSWORD` with a Gmail **App Password**.
* Recipient email: `receipinetmailid@gmail.com`.

---

## **Requirements**

* Python 3.x
* `psutil` library
* Internet connection for sending email
* Gmail account with **App Password** for SMTP

Install psutil:

```bash
pip install psutil
```

---

## **Setup Instructions**

### **1️⃣ Windows**

#### **Option A: Run manually**

1. Save script as `disk_alert.py` (e.g., `C:\monitor\disk_alert.py`)
2. Open **Command Prompt**:

```cmd
python C:\monitor\disk_alert.py
```

3. The script prints disk usage every 10 seconds. Email is sent automatically when threshold is reached.

#### **Option B: Run as background service (Task Scheduler)**

1. Open **Task Scheduler → Create Basic Task → Name: `Disk Monitor`**
2. Trigger: **At startup**
3. Action: **Start a Program**

   * Program: `python`
   * Arguments: `C:\monitor\disk_alert.py`
   * Start in: `C:\monitor\`
4. Check **Run whether user is logged on or not**
5. Finish → script will run in background continuously.

#### **Optional:** Convert to .exe

```cmd
pip install pyinstaller
pyinstaller --onefile disk_alert.py
```

* Use the generated `.exe` in Task Scheduler instead of Python.

---

### **2️⃣ Linux**

#### **Option A: Run manually**

1. Save script as `/home/username/monitor/disk_alert.py`
2. Run:

```bash
python3 /home/username/monitor/disk_alert.py
```

3. Disk usage prints every 10 seconds; email triggers if threshold exceeded.

#### **Option B: Run as systemd service**

1. Create service file `/etc/systemd/system/disk_monitor.service`:

```ini
[Unit]
Description=Disk Monitor Script

[Service]
ExecStart=/usr/bin/python3 /home/username/monitor/disk_alert.py
Restart=always
User=username
WorkingDirectory=/home/username/monitor

[Install]
WantedBy=multi-user.target
```

2. Enable and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable disk_monitor.service
sudo systemctl start disk_monitor.service
```

3. Check logs in real-time:

```bash
sudo journalctl -u disk_monitor.service -f
```

---

## **Configuration**

| Variable          | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| `DISK_THRESHOLD`  | Disk usage % that triggers alert (default 90)                      |
| `CHECK_INTERVAL`  | Time between checks (seconds, default 10)                          |
| `ALERT_DURATION`  | Time disk must remain high to trigger alert (seconds, default 300) |
| `SENDER_EMAIL`    | Email that sends alert (e.g., `sendermailid@gmail.com`)            |
| `SENDER_PASSWORD` | Gmail **App Password**                                             |
| `ALERT_EMAIL`     | Recipient email (e.g., `receipinetmailid@gmail.com`)               |

---

## **Output Example**

```text
Disk Usage for C:\ (C:\): 72%
Disk Usage for D:\ (D:\): 91%
High disk count for D:\: 1
Disk Usage for E:\ (E:\): 40%
--------------------------------------------------
...
Disk Usage for D:\ (D:\): 92%
High disk count for D:\: 30
Alert email sent to receipinetmailid@gmail.com from sendermailid@gmail.com
--------------------------------------------------
```

---

## **Notes / Best Practices**

* Each partition is tracked separately; only **one alert per high-disk event** is sent.
* Ensure the sender email has **SMTP access** (Gmail App Password if 2FA enabled).
* Can be run **continuously in background** as a service/daemon.
* Logging disk usage to a file can help track trends and storage growth.

---
