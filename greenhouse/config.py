# greenhouse/config.py

"""
Configuration centrale du système IoT Serre Intelligente
Toutes les constantes du projet doivent être définies ici.
"""

# ==========================================================
# MQTT BROKER
# ==========================================================

BROKER_HOST = "localhost" # au lieu de "test.mosquitto.org"
BROKER_PORT = 1883
BROKER_KEEPALIVE = 60

# QoS
QOS_DEFAULT = 0
QOS_CRITICAL = 1   # commandes importantes

# Retained messages
RETAIN_STATE = True


# ==========================================================
# TOPICS MQTT
# ==========================================================

TOPICS = {

    # ---- Capteurs ----
    "sensors": {
        "temp_soil": "greenhouse/sensors/temp_soil",
        "humidity": "greenhouse/sensors/humidity",
        "light": "greenhouse/sensors/light",
        "water": "greenhouse/sensors/water_level"
    },

    # ---- Actionneurs ----
    "actuators": {
        "irrigation": {
            "cmd": "greenhouse/actuators/irrigation/cmd",
            "state": "greenhouse/actuators/irrigation/state"
        },
        "lighting": {
            "cmd": "greenhouse/actuators/lighting/cmd",
            "state": "greenhouse/actuators/lighting/state"
        }
    },

    # ---- Alertes ----
    "alerts": "greenhouse/alerts"
}


# ==========================================================
# SEUILS MÉTIER (Business Rules)
# ==========================================================

THRESHOLDS = {
    "humidity_low": 40,     # %
    "water_min": 20,        # %
    "light_low": 300,       # lux
    "temp_critical": 32     # °C
}


# ==========================================================
# INTERVALLES DE PUBLICATION (secondes)
# ==========================================================

SENSOR_INTERVALS = {
    "temp_soil": 5,
    "humidity": 7,
    "light": 6,
    "water": 10
}


# ==========================================================
# PLAGES DE SIMULATION
# ==========================================================

SENSOR_RANGES = {
    "temp_soil": (15.0, 35.0),
    "humidity": (20.0, 90.0),
    "light": (0, 1000),
    "water": (0.0, 100.0)
}
# ==========================================================
# CONFIGURATION TEMPORELLE (Règle éclairage)
# ==========================================================
DAY_START_HOUR = 8
DAY_END_HOUR = 18