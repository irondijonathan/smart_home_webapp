from flask import Flask, render_template, request, current_app, jsonify
import requests
import datetime
from datetime import datetime, date, time
import time
import threading
from threading import Lock

render_lock = Lock()

app = Flask(__name__)
data = []




# Endpoint for controlling the local device
@app.route('/')
def home():
    return render_template('index.html')

app_data = [ ]

@app.route('/control', methods=['POST', 'GET'])
def control():
    global app_data
    data = request.get_json()
    app_data.append(data)  # Append the received dictionary to the list
    app_data = app_data[-4:]  # Keep only the last 4 elements in the list
    #data = request.get_json()
    device = data['device']
    action = data['action']
    turn_on_time_str = data['turn_on_time']
    turn_off_time_str = data['turn_off_time']
    #print(app_data)
    


    # Get the current date
    current_date = date.today()

    # Convert turn-on and turn-off times to time objects
    turn_on_time = datetime.strptime(turn_on_time_str, "%I:%M %p").time()
    turn_off_time = datetime.strptime(turn_off_time_str, "%I:%M %p").time()

    # Combine the time with the current date to get the datetime objects
    turn_on_time = datetime.combine(current_date, turn_on_time)
    turn_off_time = datetime.combine(current_date, turn_off_time)


    #print(turn_on_time)
    #print(turn_off_time)

    # Schedule the notifications for turn-on and turn-off times
    schedule_notification(device, 'on', turn_on_time)
    schedule_notification(device, 'off', turn_off_time)

    # Other code to handle the action and perform desired tasks

    return 'Device: ' + device + ', Action: ' + action



def call_javascript_function(device, action):
    # Call the JavaScript function to display the notification
    js_code = "displayNotification('" + device + "', '" + action + "')"
    script_tag = "<script>" + js_code + "</script>"
    response = script_tag
    print(script_tag)
    #print(True)


    # Set the necessary Flask configuration to build URLs
    app.config['SERVER_NAME'] = '127.0.0.1:8080'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'

    print(app.config['SERVER_NAME'])

    # Get the current Flask application context
    with app.app_context():
        # Render the template within the application context
        return render_template('index.html', js_code=js_code)

def schedule_notification(device, action, scheduled_time):
    
    time_difference = scheduled_time - current_time
    #print(time_difference)

    if time_difference.total_seconds() > 0:
        # Create a thread to call the JavaScript function at the scheduled time
        timer_thread = threading.Timer(time_difference.total_seconds(), call_javascript_function, args=[device, action])
        timer_thread.start()
        



# Endpoint for forwarding the device and action information to the provided IP
@app.route('/forward', methods=['POST'])
def forward():
    data = request.get_json()  # Get the JSON data sent from the HTML

    device = data['device']  # Extract the device value
    action = data['action']  # Extract the action value
    print(device)
    print(action)
   

    # Forward the device and action information to the provided IP
    ip_address = 'http://172.20.10.2:5000/control-device'  # Replace with the appropriate IP address
    forward_data = {'device': device, 'action': action}
    #forward_data = {'device':'fan'}
    response = requests.post(ip_address, json=forward_data)
    print(forward_data)

    # Process the response if needed
    # ...

    log_data(device, action)
    #return response.text
    return 'Device: ' + device + ', Action: ' + action





@app.route('/notification', methods=['POST'])
def receive_notification():
    try:
        data_received = request.get_json()
        # Process the received data as needed
        device = data_received.get('device')
        effect = data_received.get('action')
        action = effect.split()[-1]
        
        
        # Forward the device and action information to the provided IP
        ip_address = 'http://172.20.10.2:5000/control-device'  # Replace with the appropriate IP address
        forward_data = {'device': device, 'action': action}
        print(forward_data)
        response = requests.post(ip_address, json=forward_data)
        # Return a response if necessary
        
        return 'Device: ' + device + ', Action: ' + action
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def log_data(device, action):
    # Get the current date and time
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    # Log the data to a file or database
    log_entry = f"Date: {date_str}, Time: {time_str}, Device: {device}, Action: {action}"
    with open("log.txt", "a") as file:
        file.write(log_entry + "\n")



#created a temporal endpoint to send the data because the control endpoint only prints the the data in terminal and doesnt send the data to the frontend 
#but this endpoint also only sends the last device which is heater instead of all devices 

@app.route('/hello', methods=['GET'])
def hello():
    global app_data
    print(app_data)
    return app_data

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)