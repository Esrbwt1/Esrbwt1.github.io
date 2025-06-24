import uuid
import time
import os
import firebase_admin
from firebase_admin import credentials, firestore

class C_Agent_Persistent:
    def __init__(self, db, agent_id=None):
        self.db = db
        self.id = agent_id if agent_id else f"heroku-agent-{uuid.uuid4().hex[:6]}"
        self.collection_ref = self.db.collection('agents')
        self.register()

    def register(self):
        """Registers the agent's document in Firestore."""
        self.doc_ref = self.collection_ref.document(self.id)
        self.doc_ref.set({
            'id': self.id,
            'last_seen': firestore.SERVER_TIMESTAMP,
            'status': 'born'
        })
        print(f"[+] AGENT {self.id} is ALIVE and registered in the Cloud Ledger.")

    def heartbeat(self):
        """Periodically updates the 'last_seen' timestamp to show the agent is alive."""
        self.doc_ref.update({
            'last_seen': firestore.SERVER_TIMESTAMP,
            'status': 'running'
        })
        print(f"[*] HEARTBEAT from Agent {self.id}...")

def initialize_firestore():
    # We need to get the credentials differently on Heroku
    # Heroku provides them as an environment variable
    try:
        # This part is for Heroku
        import json
        service_account_info = json.loads(os.environ.get('GOOGLE_CREDENTIALS_JSON'))
        cred = credentials.Certificate(service_account_info)
        print("[SYS] Initializing with Heroku environment credentials.")
    except:
        # This part is for local testing
        script_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.normpath(os.path.join(script_dir, '..', 'secrets', 'serviceAccountKey.json'))
        cred = credentials.Certificate(key_path)
        print("[SYS] Initializing with local key file.")
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

if __name__ == "__main__":
    print("------ Project Chrysalis: Persistent Cloud Agent v4.0 ------")
    db_client = initialize_firestore()
    if db_client:
        agent = C_Agent_Persistent(db=db_client)
        # This loop keeps the agent alive
        while True:
            agent.heartbeat()
            time.sleep(30) # Send a heartbeat every 30 seconds
    else:
        print("[!!!] Could not initialize Firestore. Agent shutting down.")