import imaplib
import email
from email.header import decode_header
import time

# Your email credentials

# Create an IMAP4 class with SSL 
def check_emails():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)

        # Select the mailbox you want to check (in this case, the inbox)
        mail.select("inbox")

        # Search for unseen emails
        status, messages = mail.search(None, '(UNSEEN)')
        mail_ids = messages[0].split()

        if mail_ids:
            for num in mail_ids:
                status, msg_data = mail.fetch(num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        # Decode the email subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else 'utf-8')
                        print(f"New email from: {msg['From']}")
                        print(f"Subject: {subject}")
        else:
            print("No new emails.")
        
        # Logout from the email server
        mail.logout()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        check_emails()
        time.sleep(60)  # Wait for 1 minute before checking again
