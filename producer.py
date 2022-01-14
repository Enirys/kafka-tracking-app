from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time
import requests

#GET REQUEST FROM MAPBOX
request = requests.get('https://api.mapbox.com/directions/v5/mapbox/cycling/10.101284980773926,35.67428460426141;10.110859291766474,35.67233111505834?alternatives=false&geometries=geojson&overview=full&steps=false&access_token=pk.eyJ1IjoiZW5pcnlzayIsImEiOiJja3dvcG54Ym8wNTZrMnZwNnE2YjlsbHl2In0.-X0y3-lZJkW8aSSOLVtaog')
results = request.json()

#SAVE COORDINATES TO JSON FILE
cf = open('./data/new-coordonnees.json','w')
cf.write(json.dumps(results))
cf.close()

#READ COORDINATES FROM GEOJSON
input_file = open('./data/new-coordonnees.json')
json_array = json.load(input_file)
coordinates = json_array['routes'][0]['geometry']['coordinates']

#GENERATE UUID
def generate_uuid():
    return uuid.uuid4()

#KAFKA PRODUCER
client = KafkaClient(hosts="localhost:9092")
topic = client.topics['driver']
producer = topic.get_sync_producer()

#CONSTRUCT MESSAGE AND SEND IT TO KAFKA
data = {}

def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = 'Car' + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(1)

        #if it reaches last coordinate, start from beginning
        if i == len(coordinates)-1:
            i = 0
        else:
            i += 1

generate_checkpoint(coordinates)
