# greenhouse/sensors/humidity.py
import random
import sys
sys.path.append('..')
from sensors.base_sensor import BaseSensor
from config import TOPICS, SENSOR_INTERVALS, SENSOR_RANGES

class HumiditySensor(BaseSensor):
    def __init__(self):
        super().__init__(
            sensor_id='HUMIDITY_01',
            topic=TOPICS['sensors']['humidity'],
            interval=SENSOR_INTERVALS['humidity']
        )
        self.min_humidity, self.max_humidity = SENSOR_RANGES['humidity']
    
    def read_value(self):
        return round((random.uniform(self.min_humidity, self.max_humidity)), 1)
    
    def get_unit(self):
        return '%'

if __name__ == '__main__':
    sensor = HumiditySensor()
    sensor.start()
