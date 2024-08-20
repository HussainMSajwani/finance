import sqlite3
import os

class ADIBAcct:
    def __init__(self, account_id):
        self.account_id = account_id
        self.db_path = f'ADIB_acct_{account_id}.db'
        self._create_database()

    def _create_database(self):
        """Create the transactions table if it doesn't exist."""
        if not os.path.exists(self.db_path):
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_id TEXT NOT NULL,
                        amount REAL NOT NULL,
                        type TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (account_id, amount, type)
                VALUES (?, ?, 'deposit')
            ''', (self.account_id, amount))
            conn.commit()

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        if self.get_balance() < amount:
            raise ValueError("Insufficient funds.")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (account_id, amount, type)
                VALUES (?, ?, 'withdrawal')
            ''', (self.account_id, amount))
            conn.commit()

    def get_balance(self):
        """Calculate the current balance of the account."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT SUM(CASE WHEN type = 'deposit' THEN amount
                                WHEN type = 'withdrawal' THEN -amount
                                ELSE 0 END)
                FROM transactions
                WHERE account_id = ?
            ''', (self.account_id,))
            balance = cursor.fetchone()[0]
            return balance if balance is not None else 0.0

    def get_transactions(self):
        """Return a list of all transactions for the account."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, amount, type, timestamp
                FROM transactions
                WHERE account_id = ?
                ORDER BY timestamp DESC
            ''', (self.account_id,))
            return cursor.fetchall()

