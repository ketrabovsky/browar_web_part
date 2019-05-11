import json
import socket
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

class Heater:
    name = ""
    active = False


heater = Heater()

HOST_PORT = 5050
global_socket = None


def load_config_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content

def get_heater_name(h, json_config):
    cfg = json.loads(json_config)
    try:
        h.name = cfg["peripherals"][0]["name"]
    except:
        pass

def create_socket(port):
    global_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global_socket.connect(('0.0.0.0', port))

def create_command(command, periph=None, state=None):
    data = "{}".format(command)
    if periph is not None:
        data += " {}".format(periph)
        if state is not None:
            data += " {}".format(state)

    return data

def send_data(data):
    global_socket.sendall("{}\n".format(data))
    received = socket.recv(1024)
    print(received)


cfg = load_config_file("config.json")
heater.active = False
get_heater_name(heater, cfg)
print("Heater: {}".format(heater))
create_socket(HOST_PORT)

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
    if heater.active:
        heater.active = False
        data = create_command(COMAND_SET, heater.name, "OFF")
        send_data(data)
    else:
        heater.active = True
        data = create_command(COMAND_SET, heater.name, "ON")
        send_data(data)
    return jsonify({'data': render_template('response.html', myList=myList)})


if __name__ == "__main__":

    app.run(debug=True)