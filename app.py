import json
import socket
from flask import Flask, render_template, jsonify, request
from .libs import load_config_file, get_heater_name, create_socket, create_command, send_data
app = Flask(__name__)
print("I AM ABOUT TO BEGIN")
print("I SET U THE HOST")

class Heater:
    def __init__(self):
        self.name = ""
        self.active = False
        self.socket = None


heater = Heater()

HOST_PORT = 5050
global_socket = None


print("DEBUG: LOADING CONFG")
cfg = load_config_file("config.json")
heater.active = False
get_heater_name(heater, cfg)
print("Heater: {}".format(heater))

COMMAND_SET = "SET"
COMMAND_GET = "GET"
COMMAND_QUIT = "QUIT"


@app.route('/')
def index():
    print("LOADED FROM JSON: {} {}".format(heater.name, heater.active))
    return render_template('index.html')


@app.route('/_get_data/', methods=['POST'])
def _get_data():
    myList = ['Element1', 'Element2', 'Element3']
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('0.0.0.0', HOST_PORT))
    if heater.active:
        heater.active = False
        data = create_command(COMMAND_SET, heater.name, "OFF")
        send_data(s, data)
    else:
        heater.active = True
        data = create_command(COMMAND_SET, heater.name, "ON")
        send_data(s, data)
    s.close()
    return jsonify({'data': render_template('response.html', myList=myList)})


if __name__ == "__main__":

    app.run(host='0.0.0.0')
    app.run(debug=True)
