import typer
import psutil
import logging
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_username"
SMTP_PASSWORD = "your_password"
ALERT_EMAIL = "your_alert_email@example.com"

logging.basicConfig(
    filename="cryptojacking.log", level=logging.INFO, format="%(asctime)s - %(message)s"
)

app = typer.Typer()


def send_alert(message: str) -> None:
    """Send an email alert with the specified message."""
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        msg = MIMEText(message)
        msg["Subject"] = "Cryptojacking Alert"
        msg["From"] = SMTP_USERNAME
        msg["To"] = ALERT_EMAIL

        server.sendmail(SMTP_USERNAME, ALERT_EMAIL, msg.as_string())
        server.quit()
    except Exception as e:
        logging.error(f"Error sending email alert: {str(e)}")


@app.command()
def monitor(
    cpu_threshold: float = 70, memory_threshold: float = 70, alert_threshold: int = 3
) -> None:
    """
    Monitor system resources for cryptojacking.
    """
    consecutive_alerts = 0

    while True:
        # Get CPU and memory usage
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent

        # Check if CPU or memory usage exceeds thresholds
        if cpu_percent > cpu_threshold or memory_percent > memory_threshold:
            alert_message = f"Possible cryptojacking detected!\nCPU Usage: {cpu_percent}% | Memory Usage: {memory_percent}%"
            logging.warning(alert_message)

            consecutive_alerts += 1
            if consecutive_alerts >= alert_threshold:
                send_alert(alert_message)
                consecutive_alerts = 0
        else:
            consecutive_alerts = 0


if __name__ == "__main__":
    app()
