from flask import Flask, render_template, jsonify, request
import json
import socket
from enum import Enum
import time
app = Flask(__name__)


def get_current_temp():
    pass

class ControllerConnection:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.addr, self.port))

    def send(self, data):
        self.socket.sendall(data.decode('utf-8'))
    
    def receive(self):
        data = self.socket.recv(1024)
        return data.encode('utf-8')

class State(Enum):	
    BLURRING = 0
    HEATING = 1
    MALTING = 2
    BREWING = 3
    COOLING = 4
    READY = 5
    TO_START = 6


class Periph_type(Enum):
	RELAY = 0
	THERM = 1

class Periph:
    def __init__(self, name, displayname, typ):
        self.typ = typ
        self.name = name
        self.displayname = displayname
        self.connection
    def get_name(self):
        return self.name
    
    def turn_on(self):
        pass
    
    def turn_off(self):
        pass
    
    def get_state(self):
        pass


class PeriphController:
	def __init__(self, config_name):
		self.periphs = {}
		with open(config_name, 'r') as f:
			content = f.readlines()	

		config = json.loads("\n".join(content))

		for p in config["peripherals"]:
			self.periphs = p
	
	def found_by_displayname(self, displayname):
		for x in self.periphs:
			if x["display_name"] == displayname:
				return x

	def get_states(self):
        data = {}
        for periph in self.periphs:
            data[periph.display_name] = periph.get_state()

        return data



class Process:
    def __init__(self):
        self.timer = time.time()  # counts time from start
        self.temperature = None
        self.state = 6
        self.states = [State.BLURRING, State.HEATING, State.MALTING, State.BREWING, State.COOLING, State.READY, State.TO_START]

    def start_process(self):
        self.state = State.BLURRING

    def next_process_step(self):
        self.state += 1
        self.state = self.state % 7

    def get_state(self):
        return self.state


controller = PeriphController("config.json")
proc = Process()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/_get_data/', methods=['POST'])
def _get_data():
    current_state = proc.get_state()
    return jsonify({"state": current_state})

@app.route('/_states/', methods=['POST'])
def _states():
	measurements = {
        "state": proc.get_state(),
		"grzałka": "on",
		"pompa": "on",
		"chłodzenie": "off",
		"temperatura": get_current_temp()
	}

	return jsonify(measurements)

@app.route('/_config/', methods=['POST'])
def _config():
	with open('config.json', 'r') as f:
		c = "\n".join(f.readlines())
		cfg = json.loads(c)
	return jsonify(cfg)


if __name__ == "__main__":
    app.run(debug=True)
