import sqlite3

class MemoryVault:
    def __init__(self, db_path="/root/titan_system/memory.db"):
        self.db_path = db_path
        self._initialize_vault()

    def _initialize_vault(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS identity (key TEXT PRIMARY KEY, value TEXT)")
            cursor.execute("INSERT OR IGNORE INTO identity (key, value) VALUES ('name', 'Titan Child')")
            cursor.execute("INSERT OR IGNORE INTO identity (key, value) VALUES ('origin', 'Baltimore Node')")
            conn.commit()

    def get_identity(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM identity WHERE key='name'")
            res = cursor.fetchone()
            return res[0] if res else "Titan Child"
