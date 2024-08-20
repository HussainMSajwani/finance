import threading
from Mail import Mail
import json
from Transaction import Transaction


def main():
    credentials_file = "credentials.json"
    mail = Mail(credentials_file)
    mails = mail.get_last_n_emails(10)
    
    for subject, content, date in mails:
        t = Transaction(content, date)
        print(t)

if __name__ == "__main__":
    main()