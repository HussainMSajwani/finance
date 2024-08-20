import json
import imaplib
import email

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

    def get_all_emails(self):
        status, messages = self.mail.search(None, '(ALL)')
        mail_ids = messages[0].split()


        parser = email.parser.BytesParser()

        if mail_ids:
            for num in mail_ids:
                status, msg_data = self.mail.fetch(num, '(RFC822)')
                email_data = msg_data[0][1]
                email_message = parser.parsebytes(email_data)
                if self.username in email_message['From']:
                    print(email_message['Subject'])
                    print(email_message.get_payload())
                    print(email.utils.parsedate(email_message['Date']))
                    print()
        else:
            print("No new emails")     

        