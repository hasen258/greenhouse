# greenhouse/sensors/base_sensor.py

import json
import time
from datetime import datetime
import paho.mqtt.client as mqtt

from greenhouse.config import (
    BROKER_HOST,
    BROKER_PORT,
    BROKER_KEEPALIVE,
    QOS_DEFAULT
)


class BaseSensor:

    def __init__(self, sensor_id, topic, interval):
        self.sensor_id = sensor_id
        self.topic = topic
        self.interval = interval

        # Client MQTT (compatible Paho v2)
        self.client = mqtt.Client(client_id=f"sensor_{sensor_id}", protocol=mqtt.MQTTv311)

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

        # Reconnexion automatique
        self.client.reconnect_delay_set(min_delay=1, max_delay=10)

        self.running = False
        self.message_count = 0

    # ==========================================================
    # Callbacks MQTT
    # ==========================================================

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[{self.sensor_id}] ✅ Connecté au broker")
        else:
            print(f"[{self.sensor_id}] ❌ Échec connexion (code {rc})")

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print(f"[{self.sensor_id}] ⚠ Déconnexion inattendue – tentative de reconnexion...")

    # ==========================================================
    # Méthodes à implémenter dans les sous-classes
    # ==========================================================

    def read_value(self):
        raise NotImplementedError("read_value() doit être implémentée")

    def get_unit(self):
        return ""

    # ==========================================================
    # Publication MQTT
    # ==========================================================

    def publish_data(self):
        try:
            value = self.read_value()

            payload = {
                "sensor_id": self.sensor_id,
                "value": value,
                "unit": self.get_unit(),
                "timestamp": datetime.now().isoformat()
            }

            result = self.client.publish(
                self.topic,
                json.dumps(payload),
                qos=QOS_DEFAULT
            )

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                self.message_count += 1
                print(f"[{self.sensor_id}] #{self.message_count} -> {value} {self.get_unit()}")
            else:
                print(f"[{self.sensor_id}] ❌ Erreur publication")

        except Exception as e:
            print(f"[{self.sensor_id}] ❌ Exception: {e}")

    # ==========================================================
    # Lifecycle
    # ==========================================================

    def start(self):
        try:
            print(f"[{self.sensor_id}] Connexion au broker {BROKER_HOST}:{BROKER_PORT}...")

            self.client.connect(BROKER_HOST, BROKER_PORT, BROKER_KEEPALIVE)
            self.client.loop_start()

            print(f"[{self.sensor_id}] 🚀 Capteur démarré")
            print(f"[{self.sensor_id}] Topic: {self.topic}")
            print(f"[{self.sensor_id}] Intervalle: {self.interval}s\n")

            self.running = True

            while self.running:
                self.publish_data()
                time.sleep(self.interval)

        except KeyboardInterrupt:
            print(f"\n[{self.sensor_id}] 🛑 Arrêt demandé par l'utilisateur")

        finally:
            self.stop()

    def stop(self):
        if self.running:
            self.running = False

        self.client.loop_stop()
        self.client.disconnect()

        print(f"[{self.sensor_id}] 🔴 Arrêté ({self.message_count} messages envoyés)")