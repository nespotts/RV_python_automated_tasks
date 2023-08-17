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

if __name__ == '__main__':
	thread1 = threading.Thread(target=blynk.run)
	thread2 = threading.Thread(target=bms.run)
	thread3 = threading.Thread(target=solar.run)
	thread4 = threading.Thread(target=automation.run)

	thread1.start()
	thread2.start()
	thread3.start()
	thread4.start()


