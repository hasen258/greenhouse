# greenhouse/actuators/irrigation.py

"""
Actionneur Irrigation - Serre Intelligente

Objectif :
- Recevoir commandes MQTT (ON / OFF)
- Simuler l'irrigation
- Publier son état (retained)
- Utiliser QoS critique pour les commandes importantes
"""

# ==========================================================
# PERMETTRE IMPORT DU DOSSIER PARENT (greenhouse/)
# ==========================================================

import sys
sys.path.append('..')  # ajoute le dossier parent au PYTHONPATH

# ==========================================================
# IMPORTS
# ==========================================================

import time
import paho.mqtt.client as mqtt

from config import (
    BROKER_HOST,
    BROKER_PORT,
    BROKER_KEEPALIVE,
    QOS_CRITICAL,
    RETAIN_STATE,
    TOPICS
)

# ==========================================================
# ÉTAT INTERNE
# ==========================================================

irrigation_state = "OFF"  # État initial


# ==========================================================
# CALLBACK CONNEXION
# ==========================================================

def on_connect(client, userdata, flags, rc):
    """
    Appelé lors de la connexion au broker MQTT.
    """
    if rc == 0:
        print("✅ Irrigation connectée au broker MQTT")

        # Abonnement au topic de commande
        client.subscribe(
            TOPICS["actuators"]["irrigation"]["cmd"],
            qos=QOS_CRITICAL
        )

        print("📡 Abonné au topic commande irrigation")

        # Publier l'état initial (important si retained activé)
        publish_state(client)

    else:
        print("❌ Échec connexion MQTT")


# ==========================================================
# CALLBACK RÉCEPTION MESSAGE
# ==========================================================

def on_message(client, userdata, msg):
    """
    Appelé lorsqu'une commande est reçue.
    """
    global irrigation_state

    payload = msg.payload.decode().strip().upper()
    print(f"\n📩 Commande reçue : {payload}")

    # Vérifier validité commande
    if payload not in ["ON", "OFF"]:
        print("⚠️ Commande invalide (utiliser ON ou OFF)")
        return

    # Changement d'état uniquement si nécessaire
    if payload != irrigation_state:
        irrigation_state = payload

        simulate_irrigation(irrigation_state)
        publish_state(client)
    else:
        print("ℹ️ État déjà actif, aucune action")


# ==========================================================
# SIMULATION VISUELLE
# ==========================================================

def simulate_irrigation(state):
    """
    Simulation simple de l'irrigation.
    """
    if state == "ON":
        print("\n💧 Irrigation ACTIVÉE")
        print("🌱 Arrosage en cours...")
        time.sleep(1)
        print("💦 Eau distribuée aux plantes\n")
    else:
        print("\n🛑 Irrigation DÉSACTIVÉE")
        print("🌱 Arrosage arrêté\n")


# ==========================================================
# PUBLICATION ÉTAT (RETAINED)
# ==========================================================

def publish_state(client):
    """
    Publie l'état actuel.
    Retained=True → les nouveaux abonnés reçoivent l'état immédiatement.
    """
    client.publish(
        TOPICS["actuators"]["irrigation"]["state"],
        irrigation_state,
        qos=QOS_CRITICAL,
        retain=RETAIN_STATE
    )

    print(f"📤 État publié : {irrigation_state}")


# ==========================================================
# PROGRAMME PRINCIPAL
# ==========================================================

def main():
    """
    Initialise le client MQTT et démarre l'écoute.
    """

    client = mqtt.Client(client_id="irrigation_actuator")

    client.on_connect = on_connect
    client.on_message = on_message

    # Connexion au broker
    client.connect(
        BROKER_HOST,
        BROKER_PORT,
        BROKER_KEEPALIVE
    )

    print("🚀 Actionneur irrigation en attente de commandes...\n")

    # Boucle infinie MQTT
    client.loop_forever()


# ==========================================================
# POINT D’ENTRÉE
# ==========================================================

if __name__ == "__main__":
    main()