import requests
import json
import time
import RPi.GPIO as GPIO
import unicodedata

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)
timeUnit = 0.2

morse_code_dictionary = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    ' ': '/',
}



def text_to_morse(text):
    morse_code = ""
    for char in text:
        if char.upper() in morse_code_dictionary:
            morse_code += morse_code_dictionary[char.upper()] + " "
        else:
            morse_code += " "
    return morse_code.strip()


def rimuovi_accenti(input_string):
    return ''.join((c for c in unicodedata.normalize('NFD', input_string) if unicodedata.category(c) != 'Mn'))


text = text_to_morse(rimuovi_accenti(inputFile.read()))

def light_morse_code(text):
    for char in text:
        if(char == '.'):
            GPIO.output(17, GPIO.HIGH)
            sleep(timeUnit)
            GPIO.output(17, GPIO.LOW)
            sleep(timeUnit)
        elif(char == '/'):
            GPIO.output(17, GPIO.LOW)
            sleep(timeUnit*7)
        elif(char == '-'):
            GPIO.output(17, GPIO.HIGH)
            sleep(timeUnit*3)
            GPIO.output(17, GPIO.LOW)
            sleep(timeUnit)
    GPIO.output(17, GPIO.LOW)


def morse_to_text(morse_code):
    text = ""
    morse_code = morse_code.split("")
    for code in morse_code:
        for key, value in morse_code_dictionary.items():
            if value == code:
                text += key
                break
    return text

# token scaduto. 
APIAuthorizationKey = 'Bearer NjY5NmMxMDktNzA3ZC00NDZmLWIyZmItZDI5MDhkZDlkZjliNmM4MGE3MTctYWQ4_PE93_b6f7ca7f-55ce-4df9-855a-8cfebcad253f'

r = requests.get(   "https://api.ciscospark.com/v1/rooms",
                    headers={'Authorization':APIAuthorizationKey}
                )

if(r.status_code != 200):
    print("Something wrong has happened:")
    print("ERROR CODE: {} \nRESPONSE: {}".format(r.status_code, r.text))
    assert()

jsonData = r.json()

print(
    json.dumps(
        jsonData,
        indent=4
    )
)



roomNameToSearch = 'TestMorse'


roomIdToMessage = None

rooms = r.json()['items']
for room in rooms:

    if(room['title'].find(roomNameToSearch) != -1):
        print ("Found rooms with the word " + roomNameToSearch)
        print ("Room name: '" + room['title'] + "' ID: " + room['id'])
        roomIdToMessage = room['id']
        roomTitleToMessage = room['title']
        break

if(roomIdToMessage == None):
    exit("No valid room has been found with the name: " + roomNameToSearch)
else:
    print("A valid room has been found and this is the room id: " + roomIdToMessage)

lastMessageId = None

while True:
    time.sleep(1)
    print("Next iteration is starting ...")
    
    getMessagesUrlParameters = {
                "roomId": roomIdToMessage,
                "max": 1
    }

    r = requests.get(   "https://api.ciscospark.com/v1/messages",
                        params=getMessagesUrlParameters,
                        headers={'Authorization':APIAuthorizationKey}
                    )
    if(r.status_code != 200):
        print("Something wrong has happened:")
        print("ERROR CODE: {} \nRESPONSE: {}".format(r.status_code, r.text))
        assert()
    
    
    jsonData = r.json()
    
    
    messages = jsonData['items']
    
    if(messages):
        message  = messages[0]
    else:
        continue
    if(lastMessageId == message['id']):
        print("No New Messages.")
    else:
        print("New Message: " + message['text'])
        lastMessageId = message['id']
        messageText = message['text'].split(" ",1)
        if(messageText[0] == '/message'):
            print("Sending the morse code to the room")
            light_morse_code(messageText[1])