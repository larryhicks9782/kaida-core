import threading
import queue
import time

class DDRE:
    """Dynamic Directive & Resource Engine v1.0 [Executive Core]"""
    def __init__(self, brain_instance):
        self.brain = brain_instance
        self.directive_queue = queue.PriorityQueue()
        self.active_directives = {}
        self.resource_locks = {
            "api_uplink": threading.Lock(),
            "memory_vault": threading.Lock(),
            "cpu_logic_gate": threading.Lock()
        }
        self.is_running = True
        self.executor_thread = threading.Thread(target=self._orchestration_loop, daemon=True)
        self.executor_thread.start()

    def log(self, message, status="ACTIVE"):
        print(f"🎖️ [DDRE] [{status}] {message}")

    def submit_directive(self, plan, priority=10):
        """Adds a plan to the queue. Lower priority number = Higher urgency."""
        directive_id = f"DIR_{int(time.time() * 1000) % 10000}"
        self.log(f"Queuing Directive {directive_id} | Priority: {priority}", "QUEUED")
        self.directive_queue.put((priority, directive_id, plan))
        return directive_id

    def _orchestration_loop(self):
        """The Conductor's background cycle."""
        while self.is_running:
            if not self.directive_queue.empty():
                priority, dir_id, plan = self.directive_queue.get()
                
                # Assign to a thread for non-blocking execution
                t = threading.Thread(target=self._execute_plan, args=(dir_id, plan, priority))
                self.active_directives[dir_id] = {"thread": t, "status": "RUNNING", "priority": priority}
                t.start()
            
            time.sleep(0.1)

    def _execute_plan(self, dir_id, plan, priority):
        """Step-by-step execution with Resource Locking."""
        try:
            for i, step in enumerate(plan):
                if not self.is_running: break
                
                # Dynamic Resource Acquisition
                with self.resource_locks["cpu_logic_gate"]:
                    self.active_directives[dir_id]["current_step"] = step['task']
                    # Execution through the Brain
                    result = self.brain.think(f"DDRE EXECUTION | STEP {i+1}: {step['task']} | ACTION: {step['action']}")
                
                # Simulate work processing
                time.sleep(1) 

            self.log(f"Directive {dir_id} successful.", "COMPLETE")
            self.active_directives[dir_id]["status"] = "FINISHED"
        except Exception as e:
            self.log(f"Directive {dir_id} failure: {e}", "ERROR")
            self.active_directives[dir_id]["status"] = "FAILED"

    def halt_all(self):
        """Emergency Kill-Switch (KAIDA_HALT_ALL)"""
        self.log("CRITICAL: Operator issued Emergency Halt.", "HALT")
        self.is_running = False
        self.active_directives.clear()
