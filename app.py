from flask import Flask, render_template, request
import requests
import datetime

app = Flask(__name__)

# Endpoint for controlling the local device
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    data = request.get_json()  # Get the JSON data sent from the HTML

    device = data['device']  # Extract the device value
    action = data['action']  # Extract the action value
    #print(device)
    #print(action)

    # Process the device and action values as needed
    # ...

    return 'Device: ' + device + ', Action: ' + action

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
    app.run(host='0.0.0.0')


