import uuid
import time
import random

# --- AGENT DEFINITION (v1.2 with TTL logic) ---

class C_Agent:
    """
    Chrysalis Agent v1.2
    UPGRADED with a Time-To-Live (TTL) mechanism to prevent infinite loops.
    """
    def __init__(self, ledger, agent_id=None):
        self.ledger = ledger
        self.id = agent_id if agent_id else str(uuid.uuid4())
        self.internal_state = random.uniform(0.0, 1.0)
        self.creation_time = time.time()
        self.ledger.register(self)
        print(f"[+] AGENT CREATED & REGISTERED. ID: {self.id}. Initial State: {self.internal_state:.4f}")

    # MODIFICATION: receive_pulse now accepts a ttl
    def receive_pulse(self, source_agent_id, pulse_payload, ttl):
        """
        Receives a SynapticPulse. Now checks TTL before processing.
        """
        print(f"[->] PULSE RECEIVED by Agent {self.id} from {source_agent_id}. Payload: {pulse_payload:.4f}. [TTL={ttl}]")
        
        # TERMINATION CONDITION: If TTL has expired, the pulse dies.
        if ttl <= 0:
            print(f"[!] TTL expired at Agent {self.id}. Pulse terminated.\n")
            return

        self._process(stimulus=pulse_payload, ttl=ttl)

    # MODIFICATION: _process now passes the TTL along
    def _process(self, stimulus, ttl):
        """Internal cognitive process, same as before."""
        self.internal_state = (self.internal_state * 0.9) + (stimulus * 0.1)
        self._emit_pulse(ttl=ttl)

    # MODIFICATION: _emit_pulse now decrements the TTL for the next agent
    def _emit_pulse(self, ttl):
        """
        Selects a random target and sends it a new pulse with a decremented TTL.
        """
        response_payload = self.internal_state * 1.1 
        target_agent = self.ledger.get_random_agent(exclude_id=self.id)
        
        if target_agent:
            print(f"[<-] PULSE EMITTED by Agent {self.id} to {target_agent.id}. Payload: {response_payload:.4f}. [New TTL={ttl-1}]")
            # Pass the decremented TTL to the next agent in the chain
            target_agent.receive_pulse(self.id, response_payload, ttl - 1)
        else:
            print(f"[!] No other agents in network for Agent {self.id} to pulse.\n")

# --- LEDGER DEFINITION (Unchanged) ---

class LocalLedger:
    def __init__(self):
        self.agents = {}
        print("[SYS] Local Synaptic Ledger initialized.")
    def register(self, agent):
        print(f"[SYS] Registering Agent {agent.id} in Ledger.")
        self.agents[agent.id] = agent
    def get_random_agent(self, exclude_id=None):
        available_agents = [agent for agent_id, agent in self.agents.items() if agent_id != exclude_id]
        if not available_agents:
            return None
        return random.choice(available_agents)

# --- Main execution block for network simulation ---

if __name__ == "__main__":
    print("------ Project Chrysalis: Network Test v1.1 (Debugged) ------")
    print("Objective: Demonstrate a CONTROLLED chain reaction using a TTL.\n")

    master_ledger = LocalLedger()
    print("-" * 60)

    agent_alpha = C_Agent(ledger=master_ledger, agent_id="alpha")
    agent_beta = C_Agent(ledger=master_ledger, agent_id="beta")
    print("-" * 60)
    
    print("--- SIMULATING EXTERNAL STIMULUS to Agent alpha with TTL of 4 ---")
    initial_stimulus = random.uniform(0.0, 1.0)
    
    # MODIFICATION: The first pulse is sent with an initial TTL of 4
    agent_alpha.receive_pulse(source_agent_id="EXTERNAL", pulse_payload=initial_stimulus, ttl=4)

    print("------ SIMULATION COMPLETE: Controlled Termination ------")