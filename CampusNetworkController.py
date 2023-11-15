import scapy
from scapy.layers.inet import *
from fastapi import FastAPI, Body
from scapy.sendrecv import send, sniff
from pydantic import BaseModel
from CountMinSketch import CountMinSketch

app = FastAPI()

count = 10
address = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
port = {
    "10.0.0.1": {
        "sport": 1,
        "dport": 1
        },
    "10.0.0.2": {
        "sport": 1,
        "dport": 1
        },
    "10.0.0.3": {
        "sport": 1,
        "dport": 1
        }
    }

sketch = CountMinSketch()
class Item(BaseModel):
    src: str
    dst: str
    sport: str
    dport: str
    
def Callback(packet):
    key = packet['IP'].src + '-' + packet['IP'].dst + '-' + packet['TCP'].sport + '-' + packet['TCP'].dport + '-TCP'
    sketch.add(key)

@app.get("/send")
async def Send():
    for _ in range(0, count):
        i = random.randint(0, 3)
        j = random.randint(0, 3)
        while i == j:
            j = random.randint(0, 3)

        package = IP(src = address[i],
                     dst = address[j]) / TCP(sport = port[address[i]]["sport"],
                                             dport = port[address[j]]["dport"])
        send(package)
    sniff(filter = "tcp", prn = Callback)    

@app.post("/sketch")
async def Sketch(item: Item = Body(...)):
    key = item.src + '-' + item.dst + '-' + item.sport + '-' + item.dport + '-TCP'
    return { "Key": key, "Value": sketch.get(key) }    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)