from datetime import datetime
import random

from .base import BaseHandler

cutoff = 6

times = []
hums = []
temps = []


class HydrometerHandler(BaseHandler):
    async def get(self):
        """
        Get last 6 measurements
        """
        last = int(self.get_argument("last", 1))
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hum = random.uniform(0.0, 100.0)
        temp = random.uniform(-40.0, 40.0)
        global times
        global hums
        global temps
        times = times[-10:] + [time]
        hums = hums[-10:] + [hum]
        temps = temps[-10:] + [temp]
        table = {
            'x': times[-last:],
            'Humidity': hums[-last:],
            'Temperature': temps[-last:],
        }
        self.write(table)
