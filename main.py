import threading
import time

# from text_message import SendMessage
# sms = SendMessage()

from notification_manager import NotificationManager
nm = NotificationManager()

from influxDB import InfluxDB
db = InfluxDB()

from Blynk import Blynk
blynk = Blynk(db, False)

from bms import BMS
bms = BMS(blynk, nm)

from solar import ChargeController
solar = ChargeController(blynk, nm)

from automation import Automation
automation = Automation(blynk, bms, solar, nm)

threads = []
threads_alive = [1, 1, 1, 1]


def restartThreads(i):
	print(f"Restarting {threads[i].name}")
	if threads[i].name == "Blynk":
		threads[i] = threading.Thread(target=blynk.run, name="Blynk")
	elif threads[i].name == "BMS":
		threads[i] = threading.Thread(target=bms.run, name="BMS")
	elif threads[i].name == "Solar":
		threads[i] = threading.Thread(target=solar.run, name="Solar")
	elif threads[i].name == "Automation":
		threads[i] = threading.Thread(target=automation.run, name="Automation")

	try:
		threads[i].start()
	except Exception as e:
		print(e)

	if threads[i].is_alive():
		print(f"{threads[i].name} thread successfully restarted")
		threads_alive[i] = 1


if __name__ == '__main__':
	threads.append(threading.Thread(target=blynk.run, name="Blynk"))
	threads.append(threading.Thread(target=bms.run, name="BMS"))
	threads.append(threading.Thread(target=solar.run, name="Solar"))
	threads.append(threading.Thread(target=automation.run, name="Automation"))

	for thread in threads:
		thread.start()

	while True:
		# control what happens when thread stops running for any reason
		# print(threads_alive)
		for i in range(0, len(threads)):
			if threads_alive[i] == 1 and not threads[i].is_alive():
				threads_alive[i] = 0
				nm.send_message(f"{threads[i].name} thread stopped running")

			elif not threads[i].is_alive():
				restartThreads(i)



