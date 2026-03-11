# Memory Monitoring Script

## **Purpose**

This Python script continuously monitors memory (RAM) utilization on a server.

* It checks memory usage every **10 seconds**.
* If the memory stays above a threshold (default **80%**) for **5 minutes**, it automatically sends an **email alert**.
* The script can be run in **real-time** as a background service on **Windows** or **Linux**, so no manual intervention is needed.

This is useful for **server monitoring**, **DevOps operations**, or detecting **high memory conditions** before they cause service disruption.

---

## **Script Explanation**

Key points in the script:

1. **Memory Measurement**

```python
memory_percent = psutil.virtual_memory().percent
```

* Measures memory usage as a percentage of total RAM.
* `psutil.virtual_memory()` provides detailed stats including total, used, and available memory.

2. **Threshold Check**

```python
if memory_percent > MEMORY_THRESHOLD:
    high_memory_count += 1
```

* If memory exceeds threshold (80%), a counter increases.
* If memory drops below threshold, the counter resets.

3. **Alert Trigger**

```python
if high_memory_count >= required_count:
    send_email(memory_percent)
    high_memory_count = 0
```

* If memory remains high for **5 minutes** (30 consecutive readings at 10-second intervals), the script sends an email alert.

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

1. Save script as `memory_alert.py` (e.g., `C:\monitor\memory_alert.py`)
2. Open **Command Prompt**:

```cmd
python C:\monitor\memory_alert.py
```

3. The script prints memory usage every 10 seconds. Email is sent automatically when threshold is reached.

#### **Option B: Run as background service (Task Scheduler)**

1. Open **Task Scheduler** → Create Basic Task → Name: `Memory Monitor`
2. Trigger: **At startup**
3. Action: **Start a Program**

   * Program: `python`
   * Arguments: `C:\monitor\memory_alert.py`
   * Start in: `C:\monitor\`
4. Check **Run whether user is logged on or not**
5. Finish → script will run in background continuously.

#### **Optional:** Convert to .exe

```cmd
pip install pyinstaller
pyinstaller --onefile memory_alert.py
```

* Use the generated `.exe` in Task Scheduler instead of Python.

---

### **2️⃣ Linux**

#### **Option A: Run manually**

1. Save script as `/home/username/monitor/memory_alert.py`
2. Run:

```bash
python3 /home/username/monitor/memory_alert.py
```

3. Memory usage prints every 10 seconds; email triggers if threshold exceeded.

#### **Option B: Run as systemd service**

1. Create service file `/etc/systemd/system/memory_monitor.service`:

```ini
[Unit]
Description=Memory Monitor Script

[Service]
ExecStart=/usr/bin/python3 /home/username/monitor/memory_alert.py
Restart=always
User=username
WorkingDirectory=/home/username/monitor

[Install]
WantedBy=multi-user.target
```

2. Enable and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable memory_monitor.service
sudo systemctl start memory_monitor.service
```

3. Check logs in real-time:

```bash
sudo journalctl -u memory_monitor.service -f
```

---

## **Configuration**

| Variable           | Description                                                          |
| ------------------ | -------------------------------------------------------------------- |
| `MEMORY_THRESHOLD` | Memory % that triggers alert (default 80)                            |
| `CHECK_INTERVAL`   | Time between checks (seconds, default 10)                            |
| `ALERT_DURATION`   | Time memory must remain high to trigger alert (seconds, default 300) |
| `SENDER_EMAIL`     | Email that sends alert (e.g., `sendermailid@gmail.com`)              |
| `SENDER_PASSWORD`  | Gmail **App Password**                                               |
| `ALERT_EMAIL`      | Recipient email (e.g., `receipinetmailid@gmail.com`)                 |

---

## **Output Example**

```text
Current Memory Usage: 82%
High memory count: 1
Current Memory Usage: 85%
High memory count: 2
...
Current Memory Usage: 91%
High memory count: 30
Alert email sent to receipinetmailid@gmail.com from sendermailid@gmail.com
```

---

## **Notes / Best Practices**

* Only **one alert email per high-memory event**. Counter resets after sending.
* Ensure the sender email has **SMTP access** (Gmail App Password if 2FA enabled).
* Can be run **continuously in background** as a service/daemon.
* Logging memory usage to a file can help track trends.

---
