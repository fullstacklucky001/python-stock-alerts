import schwabdev
import threading
from dotenv import load_dotenv
import os
from pymongo import MongoClient
# from quart import Quart, request, jsonify
# from flask import Flask, request, jsonify
import datetime
import time
import json
from stream_fields import translate
from utility_functions import represents_int, playsound, format_currency
import subprocess
import asyncio


# app = Quart(__name__)
# FLASK_TOKEN = os.getenv('FLASK_TOKEN')

# @app.route('/stock-endpoint', methods=['POST'])
# async def handle_stock_data():
#     auth_header = request.headers.get('Authorization')
 
#     if not auth_header:
#         return jsonify({"error": "Authorization header is required!"}), 400

#     # Assuming the token is provided as 'Bearer <token>'
#     token_type, token = auth_header.split() if ' ' in auth_header else (None, None)

#     if token_type != 'Bearer' or not token:
#         return jsonify({"error": "Invalid Authorization format. Use 'Bearer <token>'."}), 400

#     # Get the JSON data from the request body
#     data = await request.get_json()
#     if not data:
#         return jsonify({"error": "Request body must contain JSON data!"}), 400


#     # Process the data here (if needed)
#     print(f'Received stock data: {data}')
#     active_alerts = get_active_alerts(collection)
#     symbols_to_stream = list(active_alerts.keys())

#     # Add your logic to handle the token here
#     return jsonify({"message": f"Token received: {token}"}), 200




# def run_flask_app():
    # new_loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(new_loop)
    # new_loop.run_until_complete(app.run_async(port=5000))
    # app.run(port=5000)

def main():
    global active_alerts
    global symbols_to_stream

    def get_active_alerts(collection):
        alerts_obj = collection.find({ "status": "Active" })
        alerts_dict = {}
        for stock in alerts_obj:
            symbol = stock.pop('symbol') #remove and return the symbol key
            if symbol not in alerts_dict:
                alerts_dict[symbol] = []
            alerts_dict[symbol].append(stock)
        return alerts_dict

    def adjust_stream(old_symbols, new_symbols):
        if old_symbols != new_symbols:
            streamer.send(streamer.level_one_equities(','.join(new_symbols), "0,3,9,28,29,30,33",  command="SUBS"))

    def update_active_alerts(alerts):
        global symbols_to_stream
        old_symbols = sorted(symbols_to_stream)
        symbols_to_stream = []
        for key, value_list in active_alerts.items():
            if any(d.get("status") == "Active" for d in value_list):
                symbols_to_stream.append(key)
        adjust_stream(old_symbols, sorted(symbols_to_stream))

        alerts_to_mark_as_triggered = []
        for key, alert_list in active_alerts.items():
            for alert in alert_list:
                if alert["status"] == "Triggered":
                    alerts_to_mark_as_triggered.append(alert["_id"])
        print(f"mongoIds to update: {alerts_to_mark_as_triggered}")
            
        mongo_id_strs = [str(mongo_id) for mongo_id in alerts_to_mark_as_triggered]
        command = ['python', 'update_db.py'] + mongo_id_strs
        process = subprocess.Popen(command)
           

    def display_triggered_alerts(alerts):
        for alert in alerts:
            print(alert)

    def stream_message_handler(message):
        message_data = json.loads(message)
        if 'data' in message_data.keys():
            data = message_data["data"][0]         
            Timestamp = data["timestamp"]/1000
            value = datetime.datetime.fromtimestamp(Timestamp)
            time_value = f"{value:%Y-%m-%d %H:%M:%S}"
                
            content = data["content"]
            alerts_triggered = []

            for stock in content:
                symbol = stock["key"]
                if symbol in active_alerts and "3" in stock:
                    last_price = float(stock["3"])
                    alerts = active_alerts[symbol]          
                                       
                    for alert in alerts:
                        if (alert["status"] == 'Active'):
                            first_part = f"ALERT TRIGGERED ({time_value}) - {symbol} last price ({format_currency(last_price)})"       
                            if alert["alertType"] == "UPPER" and last_price >= alert["price"]:
                                alert["status"] = "Triggered"
                                alerts_triggered.append(f"{first_part} >= {format_currency(alert["price"])}")
                            elif alert["alertType"] == "LOWER" and last_price <= alert["price"]:
                                alert["status"] = "Triggered"
                                alerts_triggered.append(f"{first_part} <= {format_currency(alert["price"])}")
                        
            if alerts_triggered:
                update_active_alerts(alerts)
                display_triggered_alerts(alerts_triggered)    
                playsound()
                   
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client["stockalerts"]
    collection = db["stocks"]    
    active_alerts = get_active_alerts(collection)
    
    symbols_to_stream = list(active_alerts.keys())
    client = schwabdev.Client(os.getenv('app_key'), os.getenv('app_secret'), os.getenv('callback_url'), tokens_file="./tmp/tokens.json", verbose=True)
    streamer = client.stream
    streamer.start(stream_message_handler)

    streamer.send(streamer.level_one_equities(','.join(symbols_to_stream), "0,3,9,28,29,30,33"))
    time.sleep(10)

if __name__ == '__main__':
    load_dotenv()
    symbols_to_stream = []
    active_alerts = {}
    # flask_thread = threading.Thread(target=run_flask_app)
    # flask_thread.start()
    # flask_thread.join()
    main()