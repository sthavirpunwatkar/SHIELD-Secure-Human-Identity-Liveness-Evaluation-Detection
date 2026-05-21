import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
import datetime

class FirebaseService:
    def __init__(self, service_account_path=None):
        """
        Initializes Firebase Admin SDK with placeholders.
        """
        self.db = None
        self.bucket = None
        
        if service_account_path and os.path.exists(service_account_path):
            try:
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred, {
                    'storageBucket': 'your-project-id.appspot.com' # Placeholder
                })
                self.db = firestore.client()
                self.bucket = storage.bucket()
                print("Firebase initialized successfully.")
            except Exception as e:
                print(f"Error initializing Firebase: {e}")
        else:
            print("Warning: Firebase service account not found. Running in Mock Mode.")

    def log_verification(self, data):
        """
        Logs verification metadata to Firestore.
        """
        if self.db:
            try:
                doc_ref = self.db.collection('verifications').document()
                data['timestamp'] = firestore.SERVER_TIMESTAMP
                doc_ref.set(data)
                return doc_ref.id
            except Exception as e:
                print(f"Error logging to Firestore: {e}")
        else:
            print(f"[Mock] Firestore Log: {data}")
            return "mock_id_123"

    def upload_snapshot(self, image_bytes, filename):
        """
        Uploads a verification snapshot to Firebase Storage.
        """
        if self.bucket:
            try:
                blob = self.bucket.blob(f"snapshots/{filename}")
                blob.upload_from_string(image_bytes, content_type='image/jpeg')
                return blob.public_url
            except Exception as e:
                print(f"Error uploading to Storage: {e}")
        else:
            print(f"[Mock] Storage Upload: {filename}")
            return f"https://mockstorage.com/{filename}"

# Global instance for easy import
firebase_service = FirebaseService()
