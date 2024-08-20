


class Transaction:

    def __init__(self, content, date):
        self.content  = content
        self.parse_content(content)
        self.date = date

    def parse_content(self, content):
        if "credited" in content:
            self.credit = True
        elif "debited" in content:
            self.credit = False
        elif "Cheque" in content:
            self.credit = False

        self.amount = float(content.split("AED")[1].split()[0])

        if content.startswith("Dear"):
            if "Cheque" in content:
                self.account = content.split("a/c *")[1].split(".")[0]
                self.balance = float(content.split("balance is")[1].split(".")[0])
            else:
                self.account = content.split("account *")[1].split(".")[0]
                self.balance = float(content.split("balance is AED")[1])
        elif content.startswith("Transaction"):
            self.account = content.split("a/c *")[1].split()[0]
            self.balance = float(content.split("Avl Bal is AED")[1])

        if "=" in self.account:
            self.account = self.account.split("=")[0]
        elif "***" in self.account:
            self.account = self.account.split("***")[1][-3:] 

        self.account = int(self.account)

    def __str__(self):
        # print(self.content)
        return f"Date: {self.date}\n" \
               f"Account: {self.account}\n" \
               f"Amount: {self.amount}\n" \
               f"Balance: {self.balance}\n" \
               f"Credit: {self.credit}\n"


