import uuid
import time
import random

class C_Agent:
    """
    Chrysalis Agent v1.0
    The foundational, hyper-lightweight cognitive unit of Project Chrysalis.
    This version is designed to be instantiated and tested in a local environment.
    """
    def __init__(self, agent_id=None):
        """
        Initializes the agent.
        Each agent has a unique ID and a simple internal state.
        """
        self.id = agent_id if agent_id else str(uuid.uuid4())
        # The Internal State Vector (ISV) starts as a single float.
        # This represents the agent's current 'charge' or 'activation level'.
        self.internal_state = random.uniform(0.0, 1.0)
        self.creation_time = time.time()
        
        print(f"[+] AGENT CREATED. ID: {self.id}. Initial State: {self.internal_state:.4f}")

    def receive_stimulus(self, stimulus_value):
        """
        Receives an external input stimulus (a simple float) and processes it.
        This represents the agent's 'receptor' function.
        """
        print(f"[->] STIMULUS RECEIVED by Agent {self.id}. Value: {stimulus_value:.4f}")
        self._process(stimulus_value)

    def _process(self, stimulus):
        """
        The agent's internal cognitive process.
        v1.0 uses a simple weighted average to simulate adaptation.
        The agent's state 'learns' by moving slightly towards the stimulus value.
        """
        # A simple learning rule: 90% old state, 10% new stimulus.
        self.internal_state = (self.internal_state * 0.9) + (stimulus * 0.1)
        self._emit_response()

    def _emit_response(self):
        """
        Produces an output based on the new internal state.
        This represents the agent's 'effector' function.
        """
        # A simple transformation for the response.
        response_value = self.internal_state * 1.1 
        print(f"[<-] RESPONSE EMITTED by Agent {self.id}. New State: {self.internal_state:.4f}. Response: {response_value:.4f}\n")
        return response_value

# --- Main execution block for testing ---
# This code will only run when the file is executed directly.
# It allows us to test a single agent's functionality.
if __name__ == "__main__":
    print("--- C_Agent v1.0 Standalone Test ---")
    print("Objective: Instantiate one C_Agent and simulate a stimulus-response cycle.\n")

    # 1. Instantiate the Genesis Agent
    genesis_agent = C_Agent(agent_id="genesis-001")

    # 2. Simulate an external world event providing a stimulus
    time.sleep(1) 
    external_stimulus = random.uniform(0.0, 1.0)
    print(f"--- SIMULATING EXTERNAL STIMULUS ({external_stimulus:.4f}) ---")
    
    # 3. Agent receives, processes, and responds to the stimulus
    genesis_agent.receive_stimulus(external_stimulus)

    print("--- TEST COMPLETE ---")