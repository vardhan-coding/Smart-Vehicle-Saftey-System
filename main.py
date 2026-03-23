"""
Smart Vehicle Safety System
Author: Kogila Harsha Vardhan Varma
Simulation: Pure Python-based vehicle safety system 
"""

import time
import random
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# SENSOR SIMULATIONS (Replace with real GPIO)
# ─────────────────────────────────────────────

class IRSensor:
    """Simulates IR sensor for red traffic signal detection"""
    def detect_red_signal(self):
        return random.choice([True, False, False, False])  # 25% chance

class LightSensor:
    """Simulates headlight failure detection"""
    def headlight_ok(self):
        return random.choice([True, True, True, False])  # 75% ok

class SpeedSensor:
    """Simulates speed reading in km/h"""
    def get_speed(self):
        return random.randint(0, 80)

class GPSModule:
    """Simulates GPS location"""
    def get_location(self):
        lat = 14.4426 + random.uniform(-0.01, 0.01)
        lon = 79.9865 + random.uniform(-0.01, 0.01)
        return {"lat": round(lat, 4), "lon": round(lon, 4)}

    def in_school_zone(self, location):
        return random.choice([True, False, False, False])

class Buzzer:
    """Simulates buzzer alert"""
    def beep(self, message):
        print(f"🔔 BUZZER ALERT: {message}")


# ─────────────────────────────────────────────
# MAIN SYSTEM
# ─────────────────────────────────────────────

class SmartVehicleSafetySystem:
    def __init__(self):
        self.ir = IRSensor()
        self.light = LightSensor()
        self.speed = SpeedSensor()
        self.gps = GPSModule()
        self.buzzer = Buzzer()
        self.vehicle_stopped = False
        self.running = False
        logger.info("✅ Smart Vehicle Safety System Initialized")

    def check_red_signal(self):
        if self.ir.detect_red_signal():
            self.vehicle_stopped = True
            self.buzzer.beep("Red Signal Detected! Vehicle Stopping...")
            logger.warning("🚦 RED SIGNAL → Vehicle Stopped")
        else:
            self.vehicle_stopped = False

    def check_headlight(self):
        if not self.light.headlight_ok():
            self.buzzer.beep("Headlight Failure! Stopping vehicle.")
            logger.warning("💡 HEADLIGHT FAILURE → Vehicle Stopped")
            self.vehicle_stopped = True

    def check_speed_zone(self):
        location = self.gps.get_location()
        speed = self.speed.get_speed()
        if self.gps.in_school_zone(location) and speed > 20:
            self.buzzer.beep(f"School Zone! Speed {speed}km/h → Reducing...")
            logger.warning(f"🏫 SCHOOL ZONE at {location} → Speed {speed}km/h too high!")

    def check_gps(self):
        location = self.gps.get_location()
        logger.info(f"📍 GPS: {location}")

    def run(self):
        self.running = True
        logger.info("🚗 Vehicle Safety System Running...")
        while self.running:
            self.check_red_signal()
            self.check_headlight()
            self.check_speed_zone()
            self.check_gps()
            time.sleep(2)

    def stop(self):
        self.running = False
        logger.info("⛔ System Stopped")


if __name__ == "__main__":
    system = SmartVehicleSafetySystem()
    try:
        system.run()
    except KeyboardInterrupt:
        system.stop()
