from datetime import datetime
import time
# import pytz

class HouseLights:
    def __init__(self, blynk):
        self.blynk = blynk
        self.house_lights_timer = 0
        self.house_lights_interval = 1000
        
    def run(self):
        while True:
            
            # utc = datetime.datetime.now() # UTC
            # eastern = pytz.timezone('US/Eastern')  # eastern timezone info
            # now = utc.astimezone(eastern)
            now = datetime.now()
            t = time.time_ns() // 1000000

            if (t - self.house_lights_timer) > self.house_lights_interval:
                self.house_lights_timer = t
                try:
                    # automate house lights
                    if now.hour == 7 and now.minute == 0:
                        print("turning house light on")
                        self.blynk.virtual_write('V1', 0, "house_lights")
                    elif now.hour == 8 and now.minute == 0:
                        print("turning house light off")
                        self.blynk.virtual_write('V1', 1, "house_lights")
                    elif now.hour == 5 and now.minute == 0:
                        print("turning house light on")
                        self.blynk.virtual_write('V1', 0, "house_lights")
                    elif now.hour == 8 and now.minute == 0:
                        print("turning house light off")
                        self.blynk.virtual_write('V1', 1, "house_lights")
                        

                except Exception as e:
                    print(e)
                    # pass

