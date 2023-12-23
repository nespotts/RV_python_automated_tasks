import time
import requests

class Blynk:
	def __init__(self):
		self.endpoint = "https://blynk.cloud/external/api/"
		self.rv_brain_token = "fkY_GzSnp2MVq31eh4iSj6UIne4-RFY0"
		self.rv_battery_token = "a58EO0MExXyF1byGFDbb-WmtsQw71bdW"
		self.house_lights_token = "dWl-flniQB-bG9NC7p2hIl-H4OiNUpp7"
		self.read_rv_brain_pins = [0,1,2,3,4,5,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79]
		self.read_rv_battery_pins = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
		self.read_house_lights_pins = [0,1,2,3]
		self.rv_brain_pin_vals = {}
		self.rv_battery_pin_vals = {}
		self.house_lights_pin_vals = {}
		self.read_interval = 750
		self.read_timer = 0

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

					vals = self.virtual_read(self.read_rv_battery_pins, "rv_battery")
					if vals != False:
						self.rv_battery_pin_vals = vals

					vals = self.virtual_read(self.read_house_lights_pins, "house_lights")
					if vals != False:
						self.house_lights_pins = vals
					
					self.read_timer = t
					# print(self.pin_vals)
				except Exception as e:
					print(e)

