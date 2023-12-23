import time
import requests
from create_datastream_dict import createBlynkDatastreams

class Blynk:
	def __init__(self, db):
		self.db = db
		self.endpoint = "https://blynk.cloud/external/api/"
		self.rv_brain_token = "fkY_GzSnp2MVq31eh4iSj6UIne4-RFY0"
		self.rv_battery_token = "a58EO0MExXyF1byGFDbb-WmtsQw71bdW"
		self.house_lights_token = "dWl-flniQB-bG9NC7p2hIl-H4OiNUpp7"
		self.read_rv_brain_pins = [0,1,2,3,4,5,6,7,8,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79]
		self.read_rv_battery_pins = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
		self.read_house_lights_pins = [0,1,2,3]
		self.rv_brain_pin_vals = {}
		self.rv_battery_pin_vals = {}
		self.house_lights_pin_vals = {}
		self.read_interval = 750
		self.read_timer = 0
		ds = createBlynkDatastreams()
  
		# generate by running create_datastream_dict.py
		# should generate at runtime
		# self.rv_brain_datastreams = [{'name': 'Booster Power', 'pin': 'V0'}, {'name': 'Star Link Power', 'pin': 'V1'}, {'name': 'InternetSchedule', 'pin': 'V2'}, {'name': 'Booster Power Feedback', 'pin': 'V3'}, {'name': 'Starlink Power Feedback', 'pin': 'V4'}, {'name': 'inverter_off_time', 'pin': 'V5'}, {'name': 'inverter_temp', 'pin': 'V6'}, {'name': 'inverter_current', 'pin': 'V7'}, {'name': 'dc_dc_current', 'pin': 'V8'}, {'name': 'battery_voltage', 'pin': 'V41'}, {'name': 'battery_current', 'pin': 'V42'}, {'name': 'battery_capacity', 'pin': 'V43'}, {'name': 'battery_state_of_charge', 'pin': 'V44'}, {'name': 'battery_state_of_charge_percent', 'pin': 'V45'}, {'name': 'battery_power', 'pin': 'V46'}, {'name': 'solar1_voltage', 'pin': 'V47'}, {'name': 'solar1_current', 'pin': 'V48'}, {'name': 'solar1_power', 'pin': 'V49'}, {'name': 'solar1_battery_voltage', 'pin': 'V50'}, {'name': 'solar1_battery_current', 'pin': 'V51'}, {'name': 'solar1_state_of_charge', 'pin': 'V52'}, {'name': 'solar1_controller_temp', 'pin': 'V53'}, {'name': 'solar2_voltage', 'pin': 'V54'}, {'name': 'solar2_current', 'pin': 'V55'}, {'name': 'solar2_power', 'pin': 'V56'}, {'name': 'solar2_battery_voltage', 'pin': 'V57'}, {'name': 'solar2_battery_current', 'pin': 'V58'}, {'name': 'solar2_state_of_charge', 'pin': 'V59'}, {'name': 'solar2_controller_temp', 'pin': 'V60'}, {'name': 'solar3_voltage', 'pin': 'V61'}, {'name': 'solar3_current', 'pin': 'V62'}, {'name': 'solar3_power', 'pin': 'V63'}, {'name': 'solar3_battery_voltage', 'pin': 'V64'}, {'name': 'solar3_battery_current', 'pin': 'V65'}, {'name': 'solar3_state_of_charge', 'pin': 'V66'}, {'name': 'solar3_controller_temp', 'pin': 'V67'}, {'name': 'solar_current', 'pin': 'V68'}, {'name': 'solar_power', 'pin': 'V69'}, {'name': 'solar_battery_current', 'pin': 'V70'}, {'name': 'solar_battery_voltage', 'pin': 'V71'}, {'name': 'load_current', 'pin': 'V72'}, {'name': 'water_heater', 'pin': 'V73'}, {'name': 'inverter', 'pin': 'V74'}, {'name': 'relay3', 'pin': 'V75'}, {'name': 'relay4', 'pin': 'V76'}, {'name': 'automation_active_hours', 'pin': 'V77'}, {'name': 'automation_enable', 'pin': 'V78'}, {'name': 'automation_soc_range', 'pin': 'V79'}]		
		# self.rv_battery_datastreams = [{'name': 'bms1_voltage', 'pin': 'V5'}, {'name': 'bms1_current', 'pin': 'V6'}, {'name': 'bms1_state_of_charge', 'pin': 'V7'}, {'name': 'bms1_discharge_status', 'pin': 'V8'}, {'name': 'bms1_charge_status', 'pin': 'V9'}, {'name': 'bms1_battery_temp', 'pin': 'V10'}, {'name': 'bms1_bms_temp', 'pin': 'V11'}, {'name': 'bms1_balance_capacity', 'pin': 'V12'}, {'name': 'bms1_rate_capacity', 'pin': 'V13'}, {'name': 'bms1_cell1_voltage', 'pin': 'V14'}, {'name': 'bms1_cell2_voltage', 'pin': 'V0'}, {'name': 'bms1_cell3_voltage', 'pin': 'V15'}, {'name': 'bms1_cell4_voltage', 'pin': 'V16'}, {'name': 'bms1_cell1_bal_en', 'pin': 'V1'}, {'name': 'bms1_cell2_bal_en', 'pin': 'V2'}, {'name': 'bms1_cell3_bal_en', 'pin': 'V3'}, {'name': 'bms1_cell4_bal_en', 'pin': 'V4'}, {'name': 'bms1_cycle_count', 'pin': 'V47'}, {'name': 'bms1_fault_count', 'pin': 'V48'}, {'name': 'bms2_voltage', 'pin': 'V17'}, {'name': 'bms2_current', 'pin': 'V18'}, {'name': 'bms2_state_of_charge', 'pin': 'V19'}, {'name': 'bms2_discharge_status', 'pin': 'V20'}, {'name': 'bms2_charge_status', 'pin': 'V21'}, {'name': 'bms2_battery_temp', 'pin': 'V22'}, {'name': 'bms2_bms_temp', 'pin': 'V23'}, {'name': 'bms2_balance_capacity', 'pin': 'V24'}, {'name': 'bms2_rate_capacity', 'pin': 'V25'}, {'name': 'bms2_cell1_voltage', 'pin': 'V49'}, {'name': 'bms2_cell2_voltage', 'pin': 'V50'}, {'name': 'bms2_cell3_voltage', 'pin': 'V51'}, {'name': 'bms2_cell4_voltage', 'pin': 'V52'}, {'name': 'bms2_cell1_bal_en', 'pin': 'V53'}, {'name': 'bms2_cell2_bal_en', 'pin': 'V54'}, {'name': 'bms2_cell3_bal_en', 'pin': 'V55'}, {'name': 'bms2_cell4_bal_en', 'pin': 'V56'}, {'name': 'bms2_cycle_count', 'pin': 'V57'}, {'name': 'bms2_fault_count', 'pin': 'V58'}, {'name': 'bms3_voltage', 'pin': 'V29'}, {'name': 'bms3_current', 'pin': 'V30'}, {'name': 'bms3_state_of_charge', 'pin': 'V31'}, {'name': 'bms3_discharge_status', 'pin': 'V32'}, {'name': 'bms3_charge_status', 'pin': 'V33'}, {'name': 'bms3_battery_temp', 'pin': 'V34'}, {'name': 'bms3_bms_temp', 'pin': 'V35'}, {'name': 'bms3_balance_capacity', 'pin': 'V36'}, {'name': 'bms3_rate_capacity', 'pin': 'V37'}, {'name': 'bms3_cell1_voltage', 'pin': 'V26'}, {'name': 'bms3_cell2_voltage', 'pin': 'V63'}, {'name': 'bms3_cell3_voltage', 'pin': 'V27'}, {'name': 'bms3_cell4_voltage', 'pin': 'V64'}, {'name': 'bms3_cell1_bal_en', 'pin': 'V28'}, {'name': 'bms3_cell2_bal_en', 'pin': 'V65'}, {'name': 'bms3_cell3_bal_en', 'pin': 'V59'}, {'name': 'bms3_cell4_bal_en', 'pin': 'V60'}, {'name': 'bms3_cycle_count', 'pin': 'V61'}, {'name': 'bms3_fault_count', 'pin': 'V62'}, {'name': 'battery_voltage', 'pin': 'V41'}, {'name': 'battery_current', 'pin': 'V42'}, {'name': 'battery_capacity', 'pin': 'V43'}, {'name': 'battery_state_of_charge', 'pin': 'V44'}, {'name': 'battery_state_of_charge_percent', 'pin': 'V45'}, {'name': 'battery_power', 'pin': 'V46'}]
		# self.house_lights_datastreams = [{'name': 'relay1', 'pin': 'V0'}, {'name': 'relay2', 'pin': 'V1'}, {'name': 'relay1_feedback', 'pin': 'V2'}, {'name': 'relay2_feedback', 'pin': 'V3'}]
		self.rv_brain_datastreams = ds.process_html(1)
		self.rv_battery_datastreams = ds.process_html(2)
		self.house_lights_datastreams = ds.process_html(3)

	def virtual_write(self, pin, value, device="rv_brain"):
		if device == "rv_brain":
			token = self.rv_brain_token
		elif device == "rv_battery":
			token = self.rv_battery_token
		else:
			token = self.house_lights_token
   
		url = self.endpoint + "update?token=" + token + "&" + str(pin) + "=" + str(value)
		# print(1)
		response = requests.get(url=url)
		# print(2)

		# print(response.status_code)
		return response.status_code
		if response.status_code == 200:
			return 1
		else:
			return 0
		
	def virtual_write_batch(self, pins, values, device="rv_brain"):
		if device == "rv_brain":
			token = self.rv_brain_token
		elif device == "rv_battery":
			token = self.rv_battery_token
		else:
			token = self.house_lights_token
   
		url = self.endpoint + "batch/update?token=" + token
		for i in range(len(pins)):
			pin_str = ""
			if isinstance(pins[i], int):
				pin_str = f"V{pins[i]}"
			elif not pins[i].__contains__('V'):
				pin_str = f"V{pins[i]}"
			else:
				pin_str = pins[i]
			url += "&" + pin_str + "=" + str(values[i])
	
		try:
			response = requests.get(url=url, timeout=3)
			return response.status_code
		except requests.Timeout as e:
			print(e)
			return 500
		except requests.RequestException as e:
			print(e)
			return 500
	

	def virtual_read(self, pins, device="rv_brain"):
		if device == "rv_brain":
			token = self.rv_brain_token
		elif device == "rv_battery":
			token = self.rv_battery_token
		else:
			token = self.house_lights_token
   
		pin_list = ""
		for pin in pins:
			pin_list += "&V" + str(pin)

		url = self.endpoint + "get?token=" + token + str(pin_list)
		# print(3)
		try:
			response = requests.get(url=url, timeout=3)
			status = response.status_code
			if status == 200:
				vals = response.json()
				# print(vals)
				return vals
			else:
				return False
		except requests.Timeout as e:
			print(e)
			return False
		except requests.RequestException as e:
			print(e)
			return False
		# print(4)

	
	def get_pin_vals(self, pins, device="rv_battery"):
		output = []
		for pin in pins:
			pin_str = ""
			if isinstance(pin, int):
				pin_str = f"V{pin}"
			elif not pin.__contains__('V'):
				pin_str = f"V{pin}"
			else:
				pin_str = pin
			# print(pin_str, self.pin_vals)
			try:
				if device == "rv_battery":
					output.append(self.rv_battery_pin_vals[pin_str])
				elif device == "rv_brain":
					output.append(self.rv_brain_pin_vals[pin_str])
				else:
					output.append(self.house_lights_pin_vals[pin_str])
			except IndexError:
				return False

		return output
	
	
	def get_pin_val(self, pin, device="rv_battery"):
		pin_str = ""
		if isinstance(pin, int):
			pin_str = f"V{pin}"
		elif not pin.__contains__('V'):
			pin_str = f"V{pin}"
		else:
			pin_str = pin
		# print(pin_str, self.pin_vals)
 
		try:
			if device == "rv_battery":
				# print(self.rv_battery_pin_vals)
				return self.rv_battery_pin_vals[pin_str]
			elif device == "rv_brain":
				# print(self.rv_brain_pin_vals)
				return self.rv_brain_pin_vals[pin_str]
			else:
				return self.house_lights_pin_vals[pin_str]
		except IndexError:
			print(False)
			return False


	def run(self):
		while True:
			t = time.time_ns() // 1000000

			if (t - self.read_timer) >= self.read_interval:
				try:
					vals = self.virtual_read(self.read_rv_brain_pins, "rv_brain")
					if vals != False:
						self.rv_brain_pin_vals = vals
						# upload data to influxDB

					vals = self.virtual_read(self.read_rv_battery_pins, "rv_battery")
					if vals != False:
						self.rv_battery_pin_vals = vals
						# upload data to influxDB

					vals = self.virtual_read(self.read_house_lights_pins, "house_lights")
					if vals != False:
						self.house_lights_pins = vals
						# upload data to influxDB
						
					self.read_timer = t
					# print(self.pin_vals)



				except Exception as e:
					print(e)

