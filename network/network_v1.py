import uuid
import time
import random

# --- AGENT DEFINITION (Slightly modified for network interaction) ---

class C_Agent:
    """
    Chrysalis Agent v1.1
    Modified to interact with a Ledger and send/receive Synaptic Pulses.
    """
    def __init__(self, ledger, agent_id=None):
        self.ledger = ledger
        self.id = agent_id if agent_id else str(uuid.uuid4())
        self.internal_state = random.uniform(0.0, 1.0)
        self.creation_time = time.time()
        
        # Agent automatically registers itself with the ledger upon creation
        self.ledger.register(self)
        print(f"[+] AGENT CREATED & REGISTERED. ID: {self.id}. Initial State: {self.internal_state:.4f}")

    def receive_pulse(self, source_agent_id, pulse_payload):
        """
        Receives a SynapticPulse from another agent.
        """
        print(f"[->] PULSE RECEIVED by Agent {self.id} from {source_agent_id}. Payload: {pulse_payload:.4f}")
        self._process(pulse_payload)

    def _process(self, stimulus):
        """Internal cognitive process, same as v1.0."""
        self.internal_state = (self.internal_state * 0.9) + (stimulus * 0.1)
        # In a network, a response is a new pulse to another agent.
        self._emit_pulse()

    def _emit_pulse(self):
        """
        Selects a random target from the ledger and sends it a new pulse.
        """
        response_payload = self.internal_state * 1.1 
        target_agent = self.ledger.get_random_agent(exclude_id=self.id)
        
        if target_agent:
            print(f"[<-] PULSE EMITTED by Agent {self.id} to {target_agent.id}. Payload: {response_payload:.4f}\n")
            target_agent.receive_pulse(self.id, response_payload)
        else:
            print(f"[!] No other agents in network for Agent {self.id} to pulse.\n")

# --- LEDGER DEFINITION ---

class LocalLedger:
    """
    A simple, local address book for agents to find each other.
    This acts as the most basic form of a nervous system.
    """
    def __init__(self):
        self.agents = {}
        print("[SYS] Local Synaptic Ledger initialized.")

    def register(self, agent):
        """Adds an agent to the network directory."""
        print(f"[SYS] Registering Agent {agent.id} in Ledger.")
        self.agents[agent.id] = agent

    def get_random_agent(self, exclude_id=None):
        """Finds a random agent in the directory, excluding the sender."""
        available_agents = [agent for agent_id, agent in self.agents.items() if agent_id != exclude_id]
        if not available_agents:
            return None
        return random.choice(available_agents)

# --- Main execution block for network simulation ---

if __name__ == "__main__":
    print("------ Project Chrysalis: Network Test v1.0 ------")
    print("Objective: Demonstrate communication between two C-Agents via a Local Ledger.\n")

    # 1. Initialize the central nervous system
    master_ledger = LocalLedger()
    print("-" * 50)

    # 2. Create two agents. They will automatically register with the ledger.
    agent_alpha = C_Agent(ledger=master_ledger, agent_id="alpha")
    agent_beta = C_Agent(ledger=master_ledger, agent_id="beta")
    print("-" * 50)
    
    # 3. Initiate the first pulse from an external source to Agent Alpha.
    # This starts the cascade.
    print("--- SIMULATING EXTERNAL STIMULUS to Agent alpha ---")
    initial_stimulus = random.uniform(0.0, 1.0)
    
    # Manually call receive_pulse for the very first stimulus
    agent_alpha.receive_pulse(source_agent_id="EXTERNAL", pulse_payload=initial_stimulus)

    print("------ SIMULATION COMPLETE ------")