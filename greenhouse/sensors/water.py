# greenhouse/sensors/water.py
import random
import sys
sys.path.append('..')
from sensors.base_sensor import BaseSensor
from config import TOPICS, SENSOR_INTERVALS, SENSOR_RANGES

class WaterLevelSensor(BaseSensor):
    def __init__(self):
        super().__init__(
            sensor_id='WATER_LEVEL_01',
            topic=TOPICS['sensors']['water'],
            interval=SENSOR_INTERVALS['water']
        )
        self.min_level, self.max_level = SENSOR_RANGES['water']
    
    def read_value(self):
        return round((random.uniform(self.min_level, self.max_level)), 1)
    
    def get_unit(self):
        return '%'

if __name__ == '__main__':
    sensor = WaterLevelSensor()
    sensor.start()
