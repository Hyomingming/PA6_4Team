"""
We define IoT Protocol messages as Python dicts for example.
They are serialized as JSON format string, then encoded in utf-8.
Caution: because every messages are delimited by new line character (b'\n') in a TCP session,
avoid using LF character inside Python strings.

The POST request messages may be sent periodically for server
to inform the client to activate the actuators if needed.

<request message> ::= <request object in JSON format with UTF-8 encoding> <LF>

<request object> ::=
    {   'method': 'POST',
        'deviceid': <device id>,
        'msgid': <messge id>,
        'data': {'distance': 28.5 }
    }

<response message> ::= <response object in JSON format with UTF-8 encoding> <LF>

<response object> ::=
    {   'status': 'OK' | 'ERROR <error msg>',
        'deviceid': <device id>
        'msgid': <messge id>
      [ 'activate': {'red': 'ON', 'green': 'OFF',
                        'blue': 'OFF', 'buzzer': 'ON' } ]  # optional
    }

<LF> ::= b'\n'
"""

from socket import *
import json, time, sys
import selectors2 as selectors, uuid
import random, math
import logging
import serial
import RPi.GPIO as GPIO

RED = 16
GREEN = 17
BLUE = 18
BUZZER = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

GPIO.output(RED, GPIO.LOW)
GPIO.output(GREEN, GPIO.LOW)
GPIO.output(BLUE, GPIO.LOW)
GPIO.output(BUZZER, GPIO.LOW)

def sen_data():
    while True:
        ultradis = serialFromArduino.readline()
        ultradis = float(ultradis)

        if((ultradis < 10)):
            GPIO.output(BUZZER, GPIO.HIGH)
            GPIO.output(RED, GPIO.HIGH)
            GPIO.output(GREEN, GPIO.LOW)
            GPIO.output(BLUE, GPIO.LOW)
            yield ultradis

        elif(ultradis < 50):
            GPIO.output(BUZZER, GPIO.LOW)
            GPIO.output(RED, GPIO.LOW)
            GPIO.output(GREEN, GPIO.HIGH)
            GPIO.output(BLUE, GPIO.LOW)
            yield ultradis

        elif(ultradis > 50):
            GPIO.output(BUZZER, GPIO.LOW)
            GPIO.output(RED, GPIO.LOW)
            GPIO.output(GREEN, GPIO.LOW)
            GPIO.output(BLUE, GPIO.HIGH)
            yield ultradis
        time.sleep(0.1)

class IoTClient:
    def __init__(self, server_addr, deviceid):
        """IoT client with persistent connection
        Each message separated by b'\n'

        :param server_addr: (host, port)
        :param deviceid: id of this IoT
        """

        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(server_addr)  # connect to server process
        rfile = sock.makefile('rb')  # file-like obj
        sel = selectors.DefaultSelector()
        sel.register(sock, selectors.EVENT_READ)

        self.sock = sock
        self.rfile = rfile
        self.deviceid = deviceid
        self.sel = sel
        self.requests = {}      # messages sent but not yet received their responses
        self.time_to_expire = None

    def select_periodic(self, interval):
        now = time.time()
        if self.time_to_expire is None:
            self.time_to_expire = now + interval
        timeout_left = self.time_to_expire - now
        if timeout_left > 0:
            events = self.sel.select(timeout=timeout_left)
            if events:
                return events
        # time to expire elapsed or timeout event occurs
        self.time_to_expire += interval # set next time to expire
        return []

    def run(self):
        # Report sensors' data forever
        sensor = sen_data()

        while True:
            try:
                events = self.select_periodic(interval=0.1)
                if not events:      # timeout occurs
                    try:
                        data = next(sensor)
                    except StopIteration:
                        logging.info('No more sensor data to send')
                        break
                    request = dict(distance=data)
                    logging.debug(request)
                    request_bytes = json.dumps(reques).encode('utf-8') + b'\n'
                    self.sock.sendall(request_bytes)
                    self.requests[msgid] = request_bytes
                else:               # EVENT_READ
                    response_bytes = self.rfile.readline()
                    if not response_bytes:
                        self.sock.close()
                        raise OSError('Server abnormally terminated')
                    response = json.loads(response_bytes.decode('UTF-8'))
                    # logging.debug(response)

            except Exception as e:
                logging.error(e)
                break
        # end of while loop

        logging.info('client terminated')
        self.sock.close()

serial_port = "/dev/ttyACM0"
serialFromArduino = serial.Serial(serial_port,9600)
serialFromArduino.flushInput()
if __name__ == '__main__':
    if len(sys.argv) == 2:
        host, port = sys.argv[1].split(':')
        port = int(port)
    else:
        print('Usage: {} host:port'.format(sys.argv[0]))
        sys.exit(1)

    logging.basicConfig(level=logging.DEBUG,
                        format = '%(asctime)s:%(levelname)s:%(message)s')
    client = IoTClient((host, port))
    client.run()
GPIO.cleanup()
