"""
Dual Motor System for Fishing Boats
Author: Kogila Harsha Vardhan Varma
Hardware: Arduino + Current & Voltage Sensors, Buzzer, DC Motors
"""

import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# SENSOR SIMULATIONS
# ─────────────────────────────────────────────

class CurrentSensor:
    def get_current(self, motor_id):
        if motor_id == "main":
            return random.uniform(0.5, 5.0)
        return random.uniform(0.5, 4.5)

class VoltageSensor:
    def get_voltage(self, motor_id):
        return random.uniform(10.0, 14.0)

class DCMotor:
    def __init__(self, name):
        self.name = name
        self.running = False

    def start(self):
        self.running = True
        logger.info(f"⚙️  Motor [{self.name}] STARTED")

    def stop(self):
        self.running = False
        logger.info(f"🛑 Motor [{self.name}] STOPPED")

class Buzzer:
    def alert(self, msg):
        print(f"🔔 ALERT: {msg}")


# ─────────────────────────────────────────────
# MAIN SYSTEM
# ─────────────────────────────────────────────

class DualMotorBoatSystem:
    CURRENT_THRESHOLD = 4.5  # Amps — motor failure threshold

    def __init__(self):
        self.main_motor = DCMotor("MAIN")
        self.backup_motor = DCMotor("BACKUP")
        self.current_sensor = CurrentSensor()
        self.voltage_sensor = VoltageSensor()
        self.buzzer = Buzzer()
        self.active_motor = "main"
        self.running = False
        logger.info("✅ Dual Motor Boat System Initialized")

    def monitor_motors(self):
        current = self.current_sensor.get_current(self.active_motor)
        voltage = self.voltage_sensor.get_voltage(self.active_motor)
        logger.info(f"📊 [{self.active_motor.upper()}] Current: {current:.2f}A | Voltage: {voltage:.2f}V")

        if current > self.CURRENT_THRESHOLD:
            self.handle_motor_failure()

    def handle_motor_failure(self):
        logger.warning(f"⚠️  {self.active_motor.upper()} MOTOR FAILED!")
        self.buzzer.alert(f"{self.active_motor.upper()} Motor Failed! Switching to backup...")

        if self.active_motor == "main":
            self.main_motor.stop()
            self.backup_motor.start()
            self.active_motor = "backup"
            logger.info("✅ Switched to BACKUP Motor")
        else:
            logger.error("❌ Both motors failed! Emergency stop.")
            self.buzzer.alert("EMERGENCY: Both motors failed! Call for help!")
            self.stop()

    def run(self):
        self.running = True
        self.main_motor.start()
        logger.info("🚤 Boat System Running...")
        while self.running:
            self.monitor_motors()
            time.sleep(2)

    def stop(self):
        self.running = False
        self.main_motor.stop()
        self.backup_motor.stop()
        logger.info("⛔ System Stopped")


if __name__ == "__main__":
    system = DualMotorBoatSystem()
    try:
        system.run()
    except KeyboardInterrupt:
        system.stop()
