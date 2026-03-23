"""
Smart Helmet for Coal Mine Workers
Author: Kogila Harsha Vardhan Varma
Hardware: Arduino + Buzzer, GSM, Gas & Temperature Sensors
"""

import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# SENSOR SIMULATIONS
# ─────────────────────────────────────────────

class GasSensor:
    """MQ-2/MQ-7 Gas Sensor simulation (ppm)"""
    def get_ppm(self):
        return random.uniform(0, 600)

class TemperatureSensor:
    """DHT11/DS18B20 Temperature simulation (°C)"""
    def get_temp(self):
        return random.uniform(25, 80)

class AccelerometerSensor:
    """MPU6050 Fall detection simulation"""
    def detect_fall(self):
        return random.choice([False, False, False, False, True])

class GSMModule:
    """SIM800L GSM simulation"""
    def send_sms(self, number, message):
        logger.info(f"📱 SMS → {number}: {message}")

    def call(self, number):
        logger.info(f"📞 CALLING → {number}")

class Buzzer:
    def beep(self, msg):
        print(f"🔔 HELMET ALERT: {msg}")


# ─────────────────────────────────────────────
# MAIN SYSTEM
# ─────────────────────────────────────────────

class SmartHelmetSystem:
    GAS_THRESHOLD = 400       # ppm — danger level
    TEMP_THRESHOLD = 60       # °C  — danger level
    CONTROL_ROOM = "+919849499491"  # supervisor number

    def __init__(self):
        self.gas = GasSensor()
        self.temp = TemperatureSensor()
        self.accel = AccelerometerSensor()
        self.gsm = GSMModule()
        self.buzzer = Buzzer()
        self.running = False
        logger.info("✅ Smart Helmet System Initialized")

    def check_gas(self):
        ppm = self.gas.get_ppm()
        logger.info(f"💨 Gas Level: {ppm:.1f} ppm")
        if ppm > self.GAS_THRESHOLD:
            self.buzzer.beep(f"DANGER! Gas level {ppm:.0f}ppm! Evacuate!")
            self.gsm.send_sms(self.CONTROL_ROOM, f"⚠️ Gas Leak! Worker in danger. Level: {ppm:.0f}ppm")
            logger.warning(f"⚠️  GAS DANGER: {ppm:.1f} ppm")

    def check_temperature(self):
        temp = self.temp.get_temp()
        logger.info(f"🌡️  Temperature: {temp:.1f}°C")
        if temp > self.TEMP_THRESHOLD:
            self.buzzer.beep(f"HIGH TEMP {temp:.0f}°C! Move away!")
            self.gsm.send_sms(self.CONTROL_ROOM, f"🌡️ High Temp Alert! {temp:.0f}°C detected.")
            logger.warning(f"🌡️  HIGH TEMP: {temp:.1f}°C")

    def check_fall(self):
        if self.accel.detect_fall():
            self.buzzer.beep("FALL DETECTED! Worker may be injured!")
            self.gsm.send_sms(self.CONTROL_ROOM, "🆘 Worker FALL detected! Send help immediately!")
            self.gsm.call(self.CONTROL_ROOM)
            logger.warning("🆘 FALL DETECTED")

    def run(self):
        self.running = True
        logger.info("⛏️  Smart Helmet Active — Worker Protected")
        while self.running:
            self.check_gas()
            self.check_temperature()
            self.check_fall()
            time.sleep(2)

    def stop(self):
        self.running = False
        logger.info("⛔ Helmet System OFF")


if __name__ == "__main__":
    helmet = SmartHelmetSystem()
    try:
        helmet.run()
    except KeyboardInterrupt:
        helmet.stop()
