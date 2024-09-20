import schwabdev
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import datetime
import time 
import json
import subprocess

from stream_fields import translate

def playsound():
    process = subprocess.Popen(['./play-sound.sh'])

def main():
    # Create a MongoClient instance
    # client = MongoClient("mongodb://localhost:27017/")
    # db = client["stockalerts"]
    # # Collection Name
    # col = db["stocks"]
    #  x = col.find_one()
    #  print(x)
    
    load_dotenv()  # load environment variables from .env file
    import datetime
    import time

    client = schwabdev.Client(os.getenv('app_key'), os.getenv('app_secret'), os.getenv('callback_url'), verbose=True)
    streamer = client.stream

    def represents_int(s):
        try: 
            int(s)
        except ValueError:
            return False
        else:
            return True

    def my_handler(message):
        message_data = json.loads(message)
        if 'data' in message_data.keys():
            data = message_data["data"][0]
            # print(data)
            # Timestamp = float(data[0]["timestamp"])
            Timestamp = time.time()
            value = datetime.datetime.fromtimestamp(Timestamp)
            time_value = f"{value:%Y-%m-%d %H:%M:%S}"
            content = data["content"]
            
            for content_obj in content:
                # print(content_obj)
                if "delayed" not in content_obj:
                    to_print = time_value
                    to_print = to_print + ", " + str(content_obj["key"])
                    # if "3" in content_obj:
                    for dict_key in content_obj:
                        if dict_key != "key" and represents_int(dict_key):
                            key_translation = translate["LEVELONE_EQUITIES"][int(dict_key)]
                            to_print = to_print + ", " + key_translation + ": " + str(content_obj[dict_key])
                    if "3" in content_obj and content_obj["key"] == "RR" and float(content_obj["3"]) >= 0.789:
                        to_print = 'ALERT TRIGGERED: ' + to_print
                        playsound()
                    print(to_print)

    streamer.start(my_handler)
    streamer.send(streamer.level_one_equities("RR,HIRU,EVTV", "0,3,9,28,29,30,33"))

if __name__ == '__main__':
    print("Streamer Started...\n")
    main()  # call the user code above