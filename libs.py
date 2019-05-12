import socket
import json

def load_config_file(filename):
    print("DEBUG: I AM READING CONFIG")
    with open(filename, 'r') as f:
        content = f.read()
    return content

def get_heater_name(h, json_config):
    print("DEBG: getiign heater name")
    cfg = json.loads(json_config)
    try:
        h.name = cfg["peripherals"][0]["name"]
    except:
        pass

def create_socket(s, port):
    print("DEBUG CREATING SOCKET")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('0.0.0.0', port))
    print("DEBUG: creating socket succeeded")

def create_command(command, periph=None, state=None):
    data = "{}".format(command)
    if periph is not None:
        data += " {}".format(periph)
        if state is not None:
            data += " {}".format(state)

    return data

def send_data(s, data):
    print("DEBUG: I am in sending data functiion")
    to_send = "{}\n".format(data)
    s.sendall(to_send.encode())
    #received = socket.recv(1024)
    #print(received)

if __name__ == "__main__":
	print("DOSNT WORK")
