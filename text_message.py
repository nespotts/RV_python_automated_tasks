import requests

class TextMessage:
    def __init__(self):
        self.triggers = {
            "nathan": "text_nathan",
            "emily": "text_emily",
        }
        self.IFTTT_KEY = "cA6SJcKRjiMKvcbQWazyQO"
        self.IFTTT_URL = "https://maker.ifttt.com/trigger/"

    def send_sms(self, msg: str, trigger: str=False):
        if not trigger:
            trigger = self.triggers["nathan"]

        api_endpoint = f"{self.IFTTT_URL}{trigger}/with/key/{self.IFTTT_KEY}"
        print(api_endpoint)
        # message syntax: {value1} on {Occurred At}
        parameters = {"value1": msg}
        try:
            text_response = requests.get(url=api_endpoint, params=parameters)
            text_response.raise_for_status()
        except Exception as e:
            print(e)
        else:
            print(text_response.status_code)
        

if __name__ == "__main__":
    # test sms message
    sms = TextMessage()

    sms.send_sms("Test text message")