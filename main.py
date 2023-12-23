import threading
import time

from text_message import SendMessage
sms = SendMessage()

from Blynk import Blynk
blynk = Blynk()

from bms import BMS
bms = BMS(blynk, sms)

from solar import ChargeController
solar = ChargeController(blynk, sms)

from automation import Automation
automation = Automation(blynk, bms, solar)

# from house_lights import HouseLights
# house_lights = HouseLights(blynk)

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
    # elif threads[i].name == "House Lights":
    #     threads[i] = threading.Thread(target=house_lights.run, name="House Lights")

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
    # threads.append(threading.Thread(target=house_lights.run, name="House Lights"))

    for thread in threads:
        thread.start()

    while True:
        # control what happens when thread stops running for any reason
        for i in range(0, len(threads)):
            if threads_alive[i] == 1 and not threads[i].is_alive():
                threads_alive[i] = 0
                sms.send_message(f"{threads[i].name} thread stopped running")

            elif not threads[i].is_alive():
                restartThreads(i)



