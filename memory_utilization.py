import psutil
import time
import smtplib
from email.mime.text import MIMEText

# Configuration
MEMORY_THRESHOLD = 80                 # percent
CHECK_INTERVAL = 10                   # seconds
ALERT_DURATION = 300                  # 5 minutes
ALERT_EMAIL = "receipinetmailid@gmail.com"  # recipient
SENDER_EMAIL = "sendermailid@gmail.com"     # sender
SENDER_PASSWORD = "your_app_password_here"  # sender Gmail App Password

high_memory_count = 0
required_count = ALERT_DURATION // CHECK_INTERVAL

def send_email(memory_value):
    subject = "High Memory Usage Alert"
    body = f"Memory usage has been above {MEMORY_THRESHOLD}% for 5 minutes.\nCurrent Memory Usage: {memory_value}%"

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


def monitor_memory():
    global high_memory_count

    while True:
        memory_percent = psutil.virtual_memory().percent
        print("Current Memory Usage:", memory_percent, "%")

        if memory_percent > MEMORY_THRESHOLD:
            high_memory_count += 1
            print("High memory count:", high_memory_count)

            if high_memory_count >= required_count:
                send_email(memory_percent)
                high_memory_count = 0  # reset after sending alert
        else:
            high_memory_count = 0

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_memory()
