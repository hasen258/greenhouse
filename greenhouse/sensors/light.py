# greenhouse/sensors/light.py
import random
import sys
sys.path.append('..')
from sensors.base_sensor import BaseSensor
from config import TOPICS, SENSOR_INTERVALS, SENSOR_RANGES

class LightSensor(BaseSensor):
    def __init__(self):
        super().__init__(
            sensor_id='LIGHT_01',
            topic=TOPICS['sensors']['light'],
            interval=SENSOR_INTERVALS['light']
        )
        self.min_light, self.max_light = SENSOR_RANGES['light']
    
    def read_value(self):
        return int(random.uniform(self.min_light, self.max_light))
    
    def get_unit(self):
        return 'lux'

if __name__ == '__main__':
    sensor = LightSensor()
    sensor.start()
