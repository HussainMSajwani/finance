import json
import imaplib
import email
from email.parser import BytesParser

def parse_transaction(email_message):
    pass

class Mail:
    def __init__(self, credentials_file, imap_server="imap.gmail.com"):
        
        with open(credentials_file) as file:
            credentials = json.load(file)
            self.username = credentials["username"]
            self.password = credentials["password"]

        try:
            self.mail = imaplib.IMAP4_SSL(imap_server)
            self.mail.login(self.username, self.password)
            self.mail.select("inbox")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Check Credentials")

        self.parser = BytesParser()

    def parse_msg_data(self, msg_data):
        email_data = msg_data[0][1]
        email_message = self.parser.parsebytes(email_data)
        
        subject = email_message['Subject']
        content = email_message.get_payload()
        date = email.utils.parsedate(email_message['Date'])
        return subject, content, date


    def get_all_emails(self):
        status, messages = self.mail.search(None, '(ALL)')
        mail_ids = messages[0].split()
        out = []
        if mail_ids:
            for num in mail_ids:
                status, msg_data = self.mail.fetch(num, '(RFC822)')
                subject, content, date = self.parse_msg_data(msg_data)
                out.append((subject, content, date))
                #printtent)

        return out  


    def get_unseen_emails(self):
        status, messages = self.mail.search(None, '(UNSEEN)')
        mail_ids = messages[0].split()
        out = []
        if mail_ids:
            for num in mail_ids:
                status, msg_data = self.mail.fetch(num, '(RFC822)')
                subject, content, date = self.parse_msg_data(msg_data)
                out.append((subject, content, date))
                #printtent)
        else:
            print("No new emails")
        return out


    def get_last_n_emails(self, n):
        status, messages = self.mail.search(None, '(ALL)')
        mail_ids = messages[0].split()
        
        out = []
        if mail_ids:
            for num in mail_ids[-n:]:
                status, msg_data = self.mail.fetch(num, '(RFC822)')
                subject, content, date = self.parse_msg_data(msg_data)
                out.append((subject, content, date))
                #printtent)
        
        return out

    def __del__(self):
        self.mail.logout() 

        