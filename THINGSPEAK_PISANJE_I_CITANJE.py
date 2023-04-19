import urllib.request
import requests
import serial
import time
from threading import Thread

PORT  = 'COM5' #port koji arduino koristi za komunikaciju moze da se vidi u tools pa port u ARDUINO IDE okruzenju
BAUD_RATE = 9600

CHANNEL_ID = '1893711'
API_KEY_WRITE = '45MLHBC1D8AYQ3A1'
API_KEY_READ = 'GVR64F7L2YEZRVMO'

BASE_URL = 'https://api.thingspeak.com'

WRITE_URL = '{}/update?api_key={}'.format(BASE_URL, API_KEY_WRITE)
READ_CHANNEL_URL = '{}/channels/{}/feeds.json?api_key={}'.format(BASE_URL, CHANNEL_ID, API_KEY_READ)
READ_FIELD1_URL = '{}/channels/{}/fields/{}.json?api_key={}&results={}'.format(BASE_URL, CHANNEL_ID, 1, API_KEY_READ, 10)

temp = requests.get(READ_FIELD1_URL)

dataJsonT = temp.json()

feeds = dataJsonT["feeds"]
temperature = []
for x in feeds:
    x = float(x["field1"])
    temperature.append(x)

def processData(data):
    processedData = {}
    dataList = data.split()

    if len(dataList) >= 2:
        processedData["temp_value"] = dataList[0]
        processedData["osv_value"] = dataList[1]
        sendTS(processedData)

def sendTS(data):
    resp = urllib.request.urlopen("{}&field1={}&field2={}".format(WRITE_URL, data["temp_value"], data["osv_value"]))

def receive(serialCom):
    receivedMessage = ""
    while True:
        if serialCom.in_waiting > 0:
            receivedMessage = serialCom.read(size = serialCom.in_waiting).decode('ascii')
            processData(receivedMessage)
        time.sleep(5)

serialCommunication = serial.Serial(PORT, BAUD_RATE)

receivingThread = Thread(target=receive, args = (serialCommunication, ))
receivingThread.start()