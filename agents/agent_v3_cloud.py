import uuid
import time
import os
import firebase_admin
from firebase_admin import credentials, firestore

# --- AGENT DEFINITION (v3.0 with Cloud Ledger Integration) ---

class C_Agent_Cloud:
    """
    Chrysalis Agent v3.0
    This version communicates with a live Google Firestore database as its Synaptic Ledger.
    """
    def __init__(self, db, agent_id=None):
        self.db = db  # Firestore database client
        self.id = agent_id if agent_id else str(uuid.uuid4())
        self.internal_state = 0.5 # Start with a neutral state
        self.collection_ref = self.db.collection('agents') # Reference to the 'agents' collection

        # Register this agent in the cloud ledger
        self.register()

    def register(self):
        """Registers or updates the agent's document in Firestore."""
        doc_ref = self.collection_ref.document(self.id)
        doc_ref.set({
            'id': self.id,
            'internal_state': self.internal_state,
            'last_seen': firestore.SERVER_TIMESTAMP # Use server time for consistency
        })
        print(f"[+] AGENT {self.id} is ALIVE and registered in the Cloud Ledger.")

# --- INITIALIZATION AND TEST BLOCK ---

def initialize_firestore():
    """Finds the secret key using a robust path and initializes Firestore."""
    try:
        # Get the absolute path of the directory the current script is in
        # e.g., C:\Users\A3sh\Desktop\Projects\Project_Chrysalis\agents
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the secrets folder by going up two levels
        # and then into 'secrets'
        key_path = os.path.join(script_dir, '..', 'secrets', 'serviceAccountKey.json')
        
        # Normalize the path to handle Windows/Linux differences cleanly
        key_path = os.path.normpath(key_path)

        if not os.path.exists(key_path):
            print("[!!!] CRITICAL ERROR: serviceAccountKey.json not found!")
            print(f"      Attempted to find key at: {key_path}")
            print("      Please ensure 'serviceAccountKey.json' is inside the 'secrets' folder in the project root.")
            return None

        cred = credentials.Certificate(key_path)
        # Check if an app is already initialized to prevent crashing on re-runs
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("[SYS] Connection to Cloud Synaptic Ledger (Firestore) established.")
        return db
    except Exception as e:
        print(f"[!!!] FAILED to initialize Firestore: {e}")
        return None

if __name__ == "__main__":
    print("------ Project Chrysalis: Cloud Ledger Test v1.0 ------")
    print("Objective: Instantiate one agent and confirm it appears in the live Firestore database.")
    
    # 1. Connect to the cloud
    db_client = initialize_firestore()
    
    # 2. If connection is successful, create an agent
    if db_client:
        print("-" * 60)
        # Create a test agent that will register itself
        test_agent_id = f"nexus-local-agent-{int(time.time())}"
        agent = C_Agent_Cloud(db=db_client, agent_id=test_agent_id)
        print("-" * 60)
        print(f"VERIFICATION: Check the Firebase console.")
        print(f"You should see a collection named 'agents' with a document inside named '{test_agent_id}'.")
    
    print("\n------ SIMULATION COMPLETE ------")