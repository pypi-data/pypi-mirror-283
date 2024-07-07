# Tinxy Package 

Used for authenticating with tinxy.in

# Usage

```
# pip install tinxy
# Python 3

import time
import base64
import requests
from tinxy import tinxy
import time

def encrypts(arg1, mqttpass):
    en_arg1 = tinxy.strToLongs(arg1.encode('utf-8').decode())
    en_mqttpass = tinxy.strToLongs(mqttpass.encode('utf-8').decode())
    ed = tinxy.encodes(en_arg1, en_mqttpass)
    ciphertext = tinxy.longsToStr(ed)
    cipherutf2 = ciphertext.encode('latin-1')
    cipherbase64 = base64.b64encode(cipherutf2)
    return base64.b64decode(cipherbase64).hex()

tm = str(int(time.time()))
data = encrypts(tm, "mqtt-password-here")

response = requests.post("http://10.0.28.17/toggle",  json={
    "password": data,
    "action": "1",
    "relayNumber": 2
})

print(response)
```