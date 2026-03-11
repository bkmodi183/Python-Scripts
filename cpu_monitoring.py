import psutil
import time
import smtplib
from email.mime.text import MIMEText

# Configuration
CPU_THRESHOLD = 80
CHECK_INTERVAL = 10       # seconds
ALERT_DURATION = 300      # 5 minutes
ALERT_EMAIL = "receipinetmailid@gmail.com"  # recipient
SENDER_EMAIL = "sendermailid@gmail.com"     # sender
SENDER_PASSWORD = "your_app_password_here"  # sender's Gmail app password

high_cpu_count = 0
required_count = ALERT_DURATION // CHECK_INTERVAL

def send_email(cpu_value):
    subject = "High CPU Alert"
    body = f"CPU usage has been above {CPU_THRESHOLD}% for 5 minutes.\nCurrent CPU: {cpu_value}%"

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


def monitor_cpu():
    global high_cpu_count
    psutil.cpu_percent(interval=None)  # initialize measurement

    while True:
        current_cpu = psutil.cpu_percent(interval=1)
        print("Current CPU:", current_cpu)

        if current_cpu > CPU_THRESHOLD:
            high_cpu_count += 1
            print("High CPU count:", high_cpu_count)

            if high_cpu_count >= required_count:
                send_email(current_cpu)
                high_cpu_count = 0  # reset after sending alert
        else:
            high_cpu_count = 0

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_cpu()
