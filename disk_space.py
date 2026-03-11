import psutil
import time
import smtplib
from email.mime.text import MIMEText

# Configuration
DISK_THRESHOLD = 90                 # percent
CHECK_INTERVAL = 10                 # seconds
ALERT_DURATION = 300                # 5 minutes
ALERT_EMAIL = "receipinetmailid@gmail.com"  # recipient
SENDER_EMAIL = "sendermailid@gmail.com"     # sender
SENDER_PASSWORD = "your_app_password_here"  # Gmail App Password

# Dictionary to track high usage counts per partition
high_disk_count = {}

# Number of consecutive checks needed to trigger alert
required_count = ALERT_DURATION // CHECK_INTERVAL

def send_email(disk_info):
    """
    Send an email alert with the disk usage details.
    """
    subject = "High Disk Usage Alert"
    body_lines = ["Disk usage has been above threshold for 5 minutes:"]
    for partition, percent in disk_info.items():
        body_lines.append(f"{partition}: {percent}%")
    body = "\n".join(body_lines)

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ALERT_EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, ALERT_EMAIL, msg.as_string())
        server.quit()
        print(f"Alert email sent to {ALERT_EMAIL} from {SENDER_EMAIL}")
    except Exception as e:
        print("Failed to send email:", e)

def monitor_disks():
    global high_disk_count
    while True:
        disk_info_for_alert = {}
        partitions = psutil.disk_partitions()
        
        for part in partitions:
            try:
                usage = psutil.disk_usage(part.mountpoint)
                percent_used = usage.percent
                print(f"Disk Usage for {part.device} ({part.mountpoint}): {percent_used}%")
                
                # Initialize counter for partition if not exists
                if part.device not in high_disk_count:
                    high_disk_count[part.device] = 0
                
                if percent_used > DISK_THRESHOLD:
                    high_disk_count[part.device] += 1
                    print(f"High disk count for {part.device}: {high_disk_count[part.device]}")
                    
                    # Add to alert info if count exceeds required
                    if high_disk_count[part.device] >= required_count:
                        disk_info_for_alert[part.device] = percent_used
                        high_disk_count[part.device] = 0  # reset after alert
                else:
                    high_disk_count[part.device] = 0
                
            except PermissionError:
                print(f"Skipping {part.device} ({part.mountpoint}): Permission denied")

        # Send email if any disk exceeded threshold for required time
        if disk_info_for_alert:
            send_email(disk_info_for_alert)

        print("-" * 50)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_disks()
