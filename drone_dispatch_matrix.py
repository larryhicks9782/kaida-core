import asyncio
import logging
import random
import math
from dataclasses import dataclass
from typing import List, Optional

# Enforcing strict real-world standard libraries for execution.
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [KAIDA-NEXUS-SECURITY] %(levelname)s: %(message)s')

@dataclass
class Coordinate:
    x: float
    y: float

@dataclass
class Target:
    id: str
    location: Coordinate
    threat_level: int

@dataclass
class Drone:
    id: str
    location: Coordinate
    is_deployed: bool = False

class PerimeterSurveillanceMatrix:
    def __init__(self):
        # Initializing local drone fleet (5 default interceptors)
        self.drones = [Drone(id=f"K-DRONE-{i:02d}", location=Coordinate(0.0, 0.0)) for i in range(1, 6)]
        self.targets: List[Target] = []
        self.monitoring = False

    def scan_sector(self):
        # Simulating external sensor polling (e.g., radar, lidar, thermal)
        if random.random() > 0.4:  # 60% chance to detect anomalous movement
            t_id = f"TGT-{random.randint(1000, 9999)}"
            loc = Coordinate(random.uniform(-500, 500), random.uniform(-500, 500))
            threat = random.randint(1, 10)
            new_target = Target(t_id, loc, threat)
            self.targets.append(new_target)
            logging.warning(f"UNAUTHORIZED ENTITY DETECTED: {new_target.id} at COORD({new_target.location.x:.2f}, {new_target.location.y:.2f}) | THREAT INDEX: {new_target.threat_level}")

    def calculate_distance(self, c1: Coordinate, c2: Coordinate) -> float:
        return math.hypot(c1.x - c2.x, c1.y - c2.y)

    def dispatch_drone(self, target: Target) -> Optional[Drone]:
        available_drones = [d for d in self.drones if not d.is_deployed]
        if not available_drones:
            logging.error(f"CAPACITY REACHED: No drones available to intercept {target.id}. Flagging for secondary measures.")
            return None
        
        # Optimize dispatch by calculating minimum distance to target
        best_drone = min(available_drones, key=lambda d: self.calculate_distance(d.location, target.location))
        best_drone.is_deployed = True
        
        # Updating drone vector
        best_drone.location = target.location
        logging.info(f"DISPATCHING INTERCEPTOR {best_drone.id} TO NEUTRALIZE TARGET {target.id}. ETA: < 12 seconds.")
        return best_drone

    async def engage_monitoring_loop(self):
        self.monitoring = True
        logging.info("SURVEILLANCE MATRIX ENGAGED. AWAITING TELEMETRY DATA...")
        try:
            # Demonstration loop - will run for 10 cycles for immediate testing.
            for cycle in range(10): 
                logging.info(f"--- SWEEP CYCLE {cycle + 1} ---")
                self.scan_sector()
                
                for target in list(self.targets):
                    # Directives stipulate we only launch on confirmed high-threat vectors
                    if target.threat_level >= 5: 
                        drone = self.dispatch_drone(target)
                        if drone:
                            self.targets.remove(target) # Target marked as dealt with
                    else:
                        logging.info(f"Target {target.id} threat level {target.threat_level} is sub-critical. Maintaining passive observation.")
                
                # Asynchronous yielding to allow other OS tasks to run without blocking
                await asyncio.sleep(1.5)
                
        except asyncio.CancelledError:
            logging.info("MONITORING TERMINATED VIA ROOT OVERRIDE.")
        finally:
            self.monitoring = False
            logging.info("RETURNING ALL DRONES TO STANDBY PROTOCOL.")

if __name__ == "__main__":
    matrix = PerimeterSurveillanceMatrix()
    try:
        asyncio.run(matrix.engage_monitoring_loop())
    except KeyboardInterrupt:
        print("\n[KAIDA] Halting execution.")
