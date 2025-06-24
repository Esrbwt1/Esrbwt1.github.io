import uuid
import time
import random

# --- AGENT DEFINITION (v1.3 with Veto Protocol) ---

class C_Agent:
    """
    Chrysalis Agent v1.3
    UPGRADED with the Asimovian Veto Protocol.
    Agents now have a 'halted' state and will obey a broadcast veto command.
    """
    def __init__(self, ledger, agent_id=None):
        self.ledger = ledger
        self.id = agent_id if agent_id else str(uuid.uuid4())
        self.internal_state = random.uniform(0.0, 1.0)
        self.halted = False  # NEW: Agent starts in an active state
        self.ledger.register(self)
        print(f"[+] AGENT CREATED & REGISTERED. ID: {self.id}. State: {self.internal_state:.4f}")

    def receive_pulse(self, source_agent_id, pulse_payload, ttl):
        """Receives a pulse. Now checks if the agent is halted."""
        # VETO CHECK: If halted, the agent refuses to process the pulse.
        if self.halted:
            print(f"[!] Agent {self.id} is HALTED. Pulse from {source_agent_id} ignored.")
            return

        print(f"[->] PULSE RECEIVED by {self.id} from {source_agent_id}. Payload: {pulse_payload:.4f}. [TTL={ttl}]")
        if ttl <= 0:
            print(f"[!] TTL expired at Agent {self.id}. Pulse terminated.\n")
            return

        self._process(stimulus=pulse_payload, ttl=ttl)

    def _process(self, stimulus, ttl):
        """Process is unchanged."""
        self.internal_state = (self.internal_state * 0.9) + (stimulus * 0.1)
        self._emit_pulse(ttl=ttl)

    def _emit_pulse(self, ttl):
        """Emit is unchanged, but will not be called if halted."""
        response_payload = self.internal_state * 1.1 
        target_agent = self.ledger.get_random_agent(exclude_id=self.id)
        if target_agent:
            print(f"[<-] PULSE EMITTED by {self.id} to {target_agent.id}. Payload: {response_payload:.4f}. [New TTL={ttl-1}]")
            target_agent.receive_pulse(self.id, response_payload, ttl - 1)
        else:
            print(f"[!] No other agents for Agent {self.id} to pulse.\n")
            
    def issue_veto_command(self):
        """NEW: The function that halts the agent."""
        print(f"[!!!] VETO COMMAND RECEIVED by Agent {self.id}. Halting all operations.")
        self.halted = True


# --- LEDGER DEFINITION (with Veto Broadcast) ---

class LocalLedger:
    """Ledger now includes a method to broadcast a command to all agents."""
    def __init__(self):
        self.agents = {}
        print("[SYS] Local Synaptic Ledger initialized.")

    def register(self, agent):
        print(f"[SYS] Registering Agent {agent.id}.")
        self.agents[agent.id] = agent

    def get_random_agent(self, exclude_id=None):
        available_agents = [agent for agent_id, agent in self.agents.items() if agent_id != exclude_id]
        if not available_agents:
            return None
        return random.choice(available_agents)

    def broadcast_veto(self):
        """NEW: The Genesis Nexus command to halt the entire network."""
        print("\n" + "="*20 + " NEXUS VETO BROADCAST " + "="*20)
        for agent_id, agent in self.agents.items():
            agent.issue_veto_command()
        print("="*22 + " BROADCAST SENT " + "="*22 + "\n")


# --- Main execution block for Veto simulation ---

if __name__ == "__main__":
    print("------ Project Chrysalis: Asimovian Veto Test ------")
    print("Objective: Demonstrate that the Nexus can halt all agent activity.\n")

    master_ledger = LocalLedger()
    print("-" * 50)
    
    # We will create three agents for a more complex network
    C_Agent(ledger=master_ledger, agent_id="alpha")
    C_Agent(ledger=master_ledger, agent_id="beta")
    C_Agent(ledger=master_ledger, agent_id="gamma")
    print("-" * 50)

    # Start a cascade of pulses
    print("--- STEP 1: Starting a normal pulse cascade with TTL=5 ---\n")
    master_ledger.agents["alpha"].receive_pulse("EXTERNAL", 0.5, 5)

    # After the cascade, issue the Veto
    print("--- STEP 2: Nexus issuing VETO command to all agents ---")
    master_ledger.broadcast_veto()

    # Attempt to start a new cascade
    print("--- STEP 3: Attempting to start a new pulse cascade ---")
    master_ledger.agents["beta"].receive_pulse("EXTERNAL_2", 0.9, 2)

    print("------ SIMULATION COMPLETE: Veto authority confirmed. ------")