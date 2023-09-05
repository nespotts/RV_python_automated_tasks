import datetime
import time
import pytz

class Automation:
    def __init__(self, blynk, bms, solar):
        self.blynk = blynk
        self.bms = bms
        self.solar = solar
        self.water_heater_state = 0 # 0-off 3-on
        self.inverter_state = 0 # 0-off 1-starting 2-waiting on inverter 3-on
        self.state = 0 # 0-inverter & WH off, 1-invert on WH off, 2-inverter on WH on, 3-inverter starting
        self.inverter_start_timer = 0
        self.state_timer = 0
        self.state_interval = 500

        self.load_timer = 0
        self.load_interval = 750

    def run(self):
        # if time of day is corrrect a
        # and if battery is above 95%
        # 
        while True:
            t = time.time_ns() // 1000000

            if (t - self.state_timer) > self.state_interval:
                self.state_timer = t
                try:    
                    automation_en = self.blynk.get_pin_val('V78')
                    if automation_en == 1:
                        # self.manage_inverter()
                        # self.manage_water_heater()
                        self.syncState()
                        self.stateMachine()
                    else:
                        print('automation disabled')
                except Exception as e:
                    print(e)

            if (t - self.load_timer) > self.load_interval:
                self.load_timer = t
                try:    
                    self.calc_load_current()
                except Exception as e:
                    print(e)


    def stateMachine(self):
        schedule = self.blynk.get_pin_val('V77').split("\x00")
        soc = self.blynk.get_pin_val('V45')
        soc_range = self.blynk.get_pin_val('V79').split("-")

        min_hour = int(schedule[0]) // 3600
        max_hour = int(schedule[1]) // 3600
        inverter_off_hour = 23

        soc_turn_on = float(soc_range[1])
        soc_turn_off = float(soc_range[0])

        utc = datetime.datetime.now() # UTC
        eastern = pytz.timezone('US/Eastern')  # eastern timezone info
        now = utc.astimezone(eastern)

        match self.state:
            case 0: # inverter & WH off
                # check if it's time to turn on
                if (soc >= soc_turn_on and now.hour >= min_hour and now.hour < max_hour):
                    self.state = 1
                    self.blynk.virtual_write('V74', 1)
                    self.inverter_start_timer = time.time() # in seconds
                    print("Starting Inverter")
            case 1: # inverter starting
                if (time.time() - self.inverter_start_timer >= 10):
                    self.state = 2
                    print("Inverter Running")
            case 2: # inverter on, WH off
                if (soc >= soc_turn_on and now.hour >= min_hour and now.hour < max_hour):
                    self.state = 3
                    self.blynk.virtual_write('V73', 1)
                    print("Turning Water Heater On")
                elif now.hour >= inverter_off_hour:
                    self.state = 0
                    self.blynk.virtual_write('V73', 0)
                    self.blynk.virtual_write('V74', 0)
                    print("Turning Inverter Off for the Night")
            case 3: # inverter & WH on
                if (soc <= soc_turn_off or now.hour < min_hour or now.hour >= max_hour):
                    self.state = 2
                    self.blynk.virtual_write('V73', 0)
                    print("Turning Water Heater Off")
                elif now.hour >= inverter_off_hour:
                    self.state = 0
                    self.blynk.virtual_write('V73', 0)
                    self.blynk.virtual_write('V74', 0)
                    print("Turning Inverter Off for the Night")


    def syncState(self):
        inverter_switch = self.blynk.get_pin_val('V74')
        water_heater = self.blynk.get_pin_val('V73')

        if inverter_switch == 0 and water_heater == 0:
            self.state = 0
        elif inverter_switch == 1 and water_heater == 0 and self.state != 1:
            self.state = 2
        elif inverter_switch == 0 and water_heater == 1:
            self.blynk.virtual_write('V73', 0)
            self.state = 0
        elif inverter_switch == 1 and water_heater == 1:
            self.state = 3
            

    def calc_load_current(self):
        battery_current = self.bms.battery['current']
        solar_current = self.solar.solar_data['battery_current']
            
        load_current = solar_current - battery_current
        res = self.blynk.virtual_write('V72', load_current)