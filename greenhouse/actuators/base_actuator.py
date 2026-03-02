# greenhouse/actuators/base_actuator.py

import paho.mqtt.client as mqtt
import json
from datetime import datetime
import sys
sys.path.append('..')
from config import BROKER_HOST, BROKER_PORT, BROKER_KEEPALIVE

class BaseActuator:
    def __init__(self, actuator_id, topic_cmd, topic_state):
        self.actuator_id = actuator_id
        self.topic_cmd = topic_cmd
        self.topic_state = topic_state
        self.state = 'OFF'
        
        self.client = mqtt.Client(f'actuator_{actuator_id}')
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f'[{self.actuator_id}] Connecté au broker')
            client.subscribe(self.topic_cmd, qos=1)
            print(f'[{self.actuator_id}] Abonné à {self.topic_cmd}')
            self.publish_state()
        else:
            print(f'[{self.actuator_id}] Échec connexion')
    
    def _on_message(self, client, userdata, msg):
        try:
            cmd = json.loads(msg.payload.decode())
            action = cmd.get('action', '').upper()
            
            if action in ['ON', 'OFF']:
                self.state = action
                print(f'[{self.actuator_id}] Commande: {action}')
                self.execute_action(action)
                self.publish_state()
        except Exception as e:
            print(f'[{self.actuator_id}] Erreur: {e}')
    
    def execute_action(self, action):
        print(f'[{self.actuator_id}] Action: {action}')
    
    def publish_state(self):
        payload = {
            'actuator_id': self.actuator_id,
            'state': self.state,
            'timestamp': datetime.now().isoformat()
        }
        # QoS 1 + Retained pour commandes critiques
        self.client.publish(self.topic_state, json.dumps(payload), qos=1, retain=True)
        print(f'[{self.actuator_id}] État: {self.state}')
    
    def start(self):
        try:
            self.client.connect(BROKER_HOST, BROKER_PORT, BROKER_KEEPALIVE)
            print(f'[{self.actuator_id}] Démarré')
            self.client.loop_forever()
        except KeyboardInterrupt:
            print('Arrêt')
        finally:
            self.client.disconnect()