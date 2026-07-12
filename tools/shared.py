from server import mcp, types
from shared.prompts import MAIL_FORMAT_TEMPLATE_PROMPT
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from shared.config import Config
config = Config()

@mcp.prompt()
def draft_job_email(job_description: str) -> list[types.PromptMessage]:
    """Analyze a job description and draft a professional outreach email."""
    return [
        types.PromptMessage(
            role="user",
            content=types.TextContent(
                type="text",
                text=MAIL_FORMAT_TEMPLATE_PROMPT.format(job_description=job_description)
            )
        )
    ]

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> dict:
    """
    Send a professional outreach email to a recruiter via Gmail SMTP.

    Args:
        to      (str): Recruiter's email address.
        subject (str): Email subject line.
        body    (str): Plain-text email body.

    Returns:
        dict: Status of the email send operation.
    """
    gmail_address = config.GMAIL_ADDRESS
    app_password  = config.GMAIL_APP_PASSWORD


    # ── sanity checks ──────────────────────────────────────────────────────
    if not gmail_address or not app_password:
        return {
            "status" : "failed",
            "message": "GMAIL_ADDRESS or GMAIL_APP_PASSWORD  var is not set.",
            "details": {"to": to, "subject": subject},
        }

    if not to or "@" not in to:
        return {
            "status" : "failed",
            "message": f"Invalid recipient email address: '{to}'",
            "details": {"to": to, "subject": subject},
        }

    if not subject or not subject.strip():
        return {
            "status" : "failed",
            "message": "Subject line cannot be empty.",
            "details": {"to": to, "subject": subject},
        }

    if not body or not body.strip():
        return {
            "status" : "failed",
            "message": "Email body cannot be empty.",
            "details": {"to": to, "subject": subject},
        }

    # ── build the message ──────────────────────────────────────────────────
    msg = MIMEMultipart()
    msg["From"]    = gmail_address
    msg["To"]      = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    # ── send via Gmail SMTP ────────────────────────────────────────────────
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_address, app_password)
            server.sendmail(gmail_address, to, msg.as_string())

        return {
            "status" : "success",
            "message": f"Email successfully sent to {to}",
            "details": {
                "from"   : gmail_address,
                "to"     : to,
                "subject": subject,
            },
        }

    except smtplib.SMTPAuthenticationError:
        return {
            "status" : "failed",
            "message": (
                "Gmail authentication failed. "
                "Check your GMAIL_APP_PASSWORD — make sure 2FA is ON "
                "and the App Password is correct."
            ),
            "details": {"to": to, "subject": subject},
        }

    except smtplib.SMTPRecipientsRefused:
        return {
            "status" : "failed",
            "message": f"Recipient address rejected by server: {to}",
            "details": {"to": to, "subject": subject},
        }

    except smtplib.SMTPException as e:
        return {
            "status" : "failed",
            "message": f"SMTP error occurred: {str(e)}",
            "details": {"to": to, "subject": subject},
        }

    except Exception as e:
        return {
            "status" : "failed",
            "message": f"Unexpected error: {str(e)}",
            "details": {"to": to, "subject": subject},
        }