# 🌱 Greenhouse – Système IoT Serre Intelligente

Système complet de gestion IoT pour une serre automatisée. Utilise MQTT pour la communication entre capteurs et actionneurs.

---

## 📋 Vue d'ensemble

- **Capteurs** : mesure température soil, humidité, luminosité, niveau d'eau
- **Actionneurs** : contrôle irrigation et éclairage
- **Architecture** : pattern orienté objet avec classe parente (héritage)
- **Protocole** : MQTT avec QoS différencié (capteurs = QoS 0, commandes = QoS 1)
- **Configuration** : centralisée dans `config.py`

---

## 📁 Structure du projet

```
greenhouse/
├── config.py                  # Configuration centralisée (broker, topics, seuils)
├── __init__.py               # Package root
│
├── sensors/                   # Capteurs (classes héritant de BaseSensor)
│   ├── __init__.py
│   ├── base_sensor.py         # Classe parente abstrait e (connexion MQTT, publication)
│   ├── temp_soil.py           # Capteur température sol (15–35°C)
│   ├── humidity.py            # Capteur humidité (20–90%)
│   ├── light.py               # Capteur luminosité (0–1000 lux)
│   └── water.py               # Capteur niveau d'eau (0–100%)
│
├── actuators/                 # Actionneurs (irrigation, éclairage)
│   ├── __init__.py
│   ├── base_actuator.py       # Classe parente (démo passif)
│   ├── irrigation.py           # Actionneur irrigation (ON/OFF)
│   └── lighting.py             # Actionneur éclairage (ON/OFF)
│
└── logs/                      # Dossier pour logs (optionnel)
```

---

## 🔧 Installation

### Prérequis
- Python 3.8+
- MQTT Broker (Mosquitto)

### Installation des dépendances

```bash
pip install paho-mqtt
```

### Démarrer le broker MQTT (Mosquitto)

Windows :
```bash
"C:\Program Files\Mosquitto\mosquitto.exe"
```

Ou vérifier que le service est actif :
```bash
net start mosquitto
```

---

## 🚀 Utilisation

### Lancer les capteurs

Chaque capteur se lance indépendamment. Depuis le dossier `greenhouse/` :

```bash
# Température sol
python -m sensors.temp_soil

# Humidité
python -m sensors.humidity

# Luminosité
python -m sensors.light

# Niveau d'eau
python -m sensors.water
```

Les capteurs publient à intervalles réguliers (config.py) sur leurs topics respectifs.

---

### Lancer les actionneurs

```bash
# Irrigation (écoute greenhouse/actuators/irrigation/cmd)
python -m actuators.irrigation

# Éclairage (écoute greenhouse/actuators/lighting/cmd)
python -m actuators.lighting
```

Les actionneurs attendent des commandes MQTT et publient leur état avec **retain=True** (persistant).

---

## 📡 Topics MQTT

### Capteurs (QoS 0, non-retained)

| Capteur | Topic | Format | Unité |
|---------|-------|--------|-------|
| Température sol | `greenhouse/sensors/temp_soil` | JSON | °C |
| Humidité | `greenhouse/sensors/humidity` | JSON | % |
| Luminosité | `greenhouse/sensors/light` | JSON | lux |
| Niveau d'eau | `greenhouse/sensors/water_level` | JSON | % |

**Exemple de payload capteur :**
```json
{
  "sensor_id": "TEMP_SOIL_01",
  "value": 22.3,
  "unit": "°C",
  "timestamp": "2026-03-02T14:30:45.123456"
}
```

---

### Actionneurs (QoS 1, retained sur state)

| Actionneur | Command | State |
|-----------|---------|-------|
| Irrigation | `greenhouse/actuators/irrigation/cmd` | `greenhouse/actuators/irrigation/state` |
| Éclairage | `greenhouse/actuators/lighting/cmd` | `greenhouse/actuators/lighting/state` |

**Payload commands :** `ON` ou `OFF`

**État publié (retained):** `ON` ou `OFF`

---

## 🎮 Exemples de commande

### Allumer l'irrigation

```bash
mosquitto_pub -t greenhouse/actuators/irrigation/cmd -m "ON"
```

### Éteindre l'éclairage

```bash
mosquitto_pub -t greenhouse/actuators/lighting/cmd -m "OFF"
```

---

## 📊 Visualiser les données (Subscriber)

Écouter tous les capteurs :
```bash
mosquitto_sub -t "greenhouse/sensors/+" -v
```

Écouter l'état d'un actionneur :
```bash
mosquitto_sub -t "greenhouse/actuators/irrigation/state" -v
```

Écouter tout :
```bash
mosquitto_sub -t "greenhouse/#" -v
```

---

## ⚙️ Configuration (config.py)

### Broker MQTT

```python
BROKER_HOST = "localhost"
BROKER_PORT = 1883
BROKER_KEEPALIVE = 60
```

### QoS

```python
QOS_DEFAULT = 0      # Capteurs : au plus une fois (rapid, léger)
QOS_CRITICAL = 1     # Commandes : au moins une fois (garanti)
RETAIN_STATE = True  # État persistant des actionneurs
```

### Plages de simulation

```python
SENSOR_RANGES = {
    "temp_soil": (15.0, 35.0),      # °C
    "humidity": (20.0, 90.0),       # %
    "light": (0, 1000),             # lux (entiers)
    "water": (0.0, 100.0)           # %
}
```

### Intervalles de publication

```python
SENSOR_INTERVALS = {
    "temp_soil": 5,   # secondes
    "humidity": 7,
    "light": 6,
    "water": 10
}
```

---

## 🏗️ Architecture et patterns

### Héritage et classes abstraites

**Capteurs** : héritent de `BaseSensor`
- Logique commune : connexion MQTT, formatage, publication
- À implémenter : `read_value()` (lecture du capteur) + `get_unit()` (unité)

```python
class HumiditySensor(BaseSensor):
    def read_value(self):
        return round(random.uniform(20, 90), 1)
    
    def get_unit(self):
        return '%'
```

**Actionneurs** : écoutent leurs topics de commande
- Modifient un état interne
- Publient un message **retained** pour persister l'état

---

### Séparation des responsabilités

- `config.py` : **unique source de vérité** pour les paramètres
- `sensors/` : contient tous les capteurs (clarifié, maintenance)
- `actuators/` : contient tous les actionneurs (découplage)

---

## 🐛 Dépannage

### `ModuleNotFoundError: No module named 'greenhouse'`

**Cause :** Script lancé sans le contexte de package Python

**Solution :** Utiliser `-m` :
```bash
python -m sensors.temp_soil      # ✅ Correct
python sensors\temp_soil.py      # ❌ Incorrect
```

---

### Broker MQTT non disponible

**Vérifier :**
```bash
netstat -an | findstr 1883      # Windows
ss -an | grep 1883              # Linux/Mac
```

**Redémarrer le service :**
```bash
net stop mosquitto
net start mosquitto
```

---

### Capteurs ne publient rien

1. Broker actif ? → vérifier `mosquitto_sub`
2. Topic correct ? → vérifier `config.py`
3. QoS supporté ? → QoS 0 et 1 supportés par Mosquitto par défaut

---

## 📝 Notes techniques

- **Simulation** : les capteurs génèrent des valeurs aléatoires (pas de HAL réel)
- **Reconnexion auto** : `reconnect_delay_set()` dans `BaseSensor`
- **État retenu** : les actionneurs publient avec `retain=True` pour persister
- **Boucle infinie** : `client.loop_forever()` pour écouter les messages indéfiniment

---

## 📚 Renvois utiles

- [Paho-MQTT Python Docs](https://eclipse.dev/paho/files/paho.mqtt.python/html/)
- [MQTT Specification](https://mqtt.org/mqtt-specification)
- [Mosquitto](https://mosquitto.org/)

---

**Serre Intelligente v0.1.0** — Système IoT basé sur MQTT  
Mars 2026
