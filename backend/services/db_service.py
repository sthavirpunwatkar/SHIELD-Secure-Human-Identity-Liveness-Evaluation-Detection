import os
import sqlite3
import datetime

class LocalDBService:
    def __init__(self, db_path='shield_local.db', storage_dir='local_storage/snapshots'):
        """
        Initializes SQLite DB and local storage.
        """
        self.db_path = db_path
        self.storage_dir = storage_dir
        
        # Ensure storage directory exists
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Initialize SQLite DB
        self._init_db()

    def _init_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS verifications (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    verdict TEXT,
                    confidence REAL,
                    details TEXT,
                    image_url TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
            print(f"Local SQLite DB initialized at {self.db_path}.")
        except Exception as e:
            print(f"Error initializing SQLite DB: {e}")

    def log_verification(self, data):
        """
        Logs verification metadata to SQLite DB.
        """
        try:
            import uuid
            doc_id = str(uuid.uuid4())
            session_id = data.get("session_id", "")
            verdict = data.get("verdict", "")
            confidence = data.get("confidence", 0.0)
            import json
            details = json.dumps(data.get("details", {}))
            image_url = data.get("image_url", "")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO verifications (id, session_id, verdict, confidence, details, image_url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (doc_id, session_id, verdict, confidence, details, image_url))
            conn.commit()
            conn.close()
            return doc_id
        except Exception as e:
            print(f"Error logging to SQLite DB: {e}")
            return "error_id"

    def upload_snapshot(self, image_bytes, filename):
        """
        Uploads a verification snapshot to local storage.
        """
        try:
            file_path = os.path.join(self.storage_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(image_bytes)
            # Return a local URL or path
            return f"/snapshots/{filename}"
        except Exception as e:
            print(f"Error saving snapshot locally: {e}")
            return f"error/{filename}"

# Global instance for easy import
db_service = LocalDBService()
