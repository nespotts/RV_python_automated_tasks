import threading
import time

from Blynk import Blynk
blynk = Blynk()

from bms import BMS
bms = BMS(blynk)

from solar import ChargeController
solar = ChargeController(blynk)

from automation import Automation
automation = Automation(blynk, bms, solar)

from text_message import TextMessage
sms = TextMessage()

threads = []

if __name__ == '__main__':
	threads.append(threading.Thread(target=blynk.run, name="Blynk"))
	threads.append(threading.Thread(target=bms.run, name="BMS"))
	threads.append(threading.Thread(target=solar.run, name="Solar"))
	threads.append(threading.Thread(target=automation.run, name="Automation"))

	for thread in threads:
		thread.start()

	threads_alive = [1,1,1,1]
	while True:
		# control what happens when thread stops running for any reason
		for i in range(0, len(threads)):
			if threads_alive[i] == 1 and not threads[i].is_alive():
				threads_alive[i] = 0
				print(threads[i].name)
				sms.send_sms(f"RV thread {threads[i].name} stopped running")
		


