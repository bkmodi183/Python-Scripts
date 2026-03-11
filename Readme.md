# CPU Monitoring Script

## **Purpose**

This Python script continuously monitors CPU utilization on a server.

* It checks CPU usage every **10 seconds**.
* If the CPU stays above a threshold (default **80%**) for **5 minutes**, it automatically sends an **email alert**.
* The script can be run in **real-time** as a background service on **Windows** or **Linux**, so no manual intervention is needed.

This is useful for **server monitoring**, **DevOps operations**, or detecting **high CPU conditions** before they cause service disruption.

---

## **Script Explanation**

Key points in the script:

1. **CPU Measurement**

```python
current_cpu = psutil.cpu_percent(interval=1)
```

* Measures CPU usage over 1 second.
* `psutil.cpu_percent(interval=None)` is called first to initialize the measurement.

2. **Threshold Check**

```python
if current_cpu > CPU_THRESHOLD:
    high_cpu_count += 1
```

* If CPU exceeds threshold (80%), a counter increases.
* If CPU drops below threshold, the counter resets.

3. **Alert Trigger**

```python
if high_cpu_count >= required_count:
    send_email(current_cpu)
    high_cpu_count = 0
```

* If CPU remains high for **5 minutes** (30 consecutive readings at 10-second intervals), the script sends an email alert.

4. **Email Sending**

```python
smtplib.SMTP("smtp.gmail.com", 587)
```

* Sends email via Gmail SMTP.
* Replace `SENDER_EMAIL` with your email (e.g., `friendclubabv@gmail.com`) and `SENDER_PASSWORD` with a Gmail **App Password**.
* Recipient email: `bkmodi183@gmail.com`.

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

1. Save script as `cpu_alert.py` (e.g., `C:\monitor\cpu_alert.py`)
2. Open **Command Prompt**:

```cmd
python C:\monitor\cpu_alert.py
```

3. The script prints CPU usage every 10 seconds. Email is sent automatically when threshold is reached.

#### **Option B: Run as background service (Task Scheduler)**

1. Open **Task Scheduler** → Create Basic Task → Name: `CPU Monitor`
2. Trigger: **At startup**
3. Action: **Start a Program**

   * Program: `python`
   * Arguments: `C:\monitor\cpu_alert.py`
   * Start in: `C:\monitor\`
4. Check **Run whether user is logged on or not**
5. Finish → script will run in background continuously.

#### **Optional:** Convert to .exe

```cmd
pip install pyinstaller
pyinstaller --onefile cpu_alert.py
```

* Use the generated `.exe` in Task Scheduler instead of Python.

---

### **2️⃣ Linux**

#### **Option A: Run manually**

1. Save script as `/home/username/monitor/cpu_alert.py`
2. Run:

```bash
python3 /home/username/monitor/cpu_alert.py
```

3. CPU prints every 10 seconds; email triggers if threshold exceeded.

#### **Option B: Run as systemd service**

1. Create service file `/etc/systemd/system/cpu_monitor.service`:

```ini
[Unit]
Description=CPU Monitor Script

[Service]
ExecStart=/usr/bin/python3 /home/username/monitor/cpu_alert.py
Restart=always
User=username
WorkingDirectory=/home/username/monitor

[Install]
WantedBy=multi-user.target
```

2. Enable and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable cpu_monitor.service
sudo systemctl start cpu_monitor.service
```

3. Check logs in real-time:

```bash
sudo journalctl -u cpu_monitor.service -f
```

---

## **Configuration**

| Variable          | Description                                                       |
| ----------------- | ----------------------------------------------------------------- |
| `CPU_THRESHOLD`   | CPU % that triggers alert (default 80)                            |
| `CHECK_INTERVAL`  | Time between checks (seconds, default 10)                         |
| `ALERT_DURATION`  | Time CPU must remain high to trigger alert (seconds, default 300) |
| `SENDER_EMAIL`    | Email that sends alert (e.g., `friendclubabv@gmail.com`)          |
| `SENDER_PASSWORD` | Gmail **App Password**                                            |
| `ALERT_EMAIL`     | Recipient email (e.g., `bkmodi183@gmail.com`)                     |

---

## **Output Example**

```text
Current CPU: 82
High CPU count: 1
Current CPU: 85
High CPU count: 2
...
Current CPU: 91
High CPU count: 30
Alert email sent to bkmodi183@gmail.com from friendclubabv@gmail.com
```

---

## **Notes / Best Practices**

* Only **one alert email per high-CPU event**. Counter resets after sending.
* Ensure the sender email has **SMTP access** (Gmail App Password if 2FA enabled).
* Can be run **continuously in background** as a service/daemon.
* Logging CPU to a file can help track trends.
