from flask import Flask, render_template, request, current_app
import requests
#import datetime
from datetime import datetime, date, time
import time
import threading
from threading import Lock

render_lock = Lock()

app = Flask(__name__)





# Endpoint for controlling the local device
@app.route('/')
def home():
    return render_template('index.html')

'''@app.route('/control', methods=['POST'])
def control():
    data = request.get_json()
    device = data['device']
    action = data['action']
    turn_on_time_str = data['turn_on_time']
    turn_off_time_str = data['turn_off_time']
    print(data)
    


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
    current_time = datetime.now()
    time_difference = scheduled_time - current_time
    #print(time_difference)

    if time_difference.total_seconds() > 0:
        # Create a thread to call the JavaScript function at the scheduled time
        timer_thread = threading.Timer(time_difference.total_seconds(), call_javascript_function, args=[device, action])
        timer_thread.start()
        print("testing")
'''


# Endpoint for forwarding the device and action information to the provided IP
@app.route('/forward', methods=['POST'])
def forward():
    data = request.get_json()  # Get the JSON data sent from the HTML

    device = data['device']  # Extract the device value
    action = data['action']  # Extract the action value
    #print(device)
    #print(action)

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


def log_data(device, action):
    # Get the current date and time
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    # Log the data to a file or database
    log_entry = f"Date: {date_str}, Time: {time_str}, Device: {device}, Action: {action}"
    with open("log.txt", "a") as file:
        file.write(log_entry + "\n")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)