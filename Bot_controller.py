import socket 
import threading
import RPi.GPIO as GPIO
import time

HEADER = 64
PORT = 12345
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = ('192.168.0.107', PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT "

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

####  HAL  ###
in1 = 13
in2 = 19
en1 = 26

in3 = 22
in4 = 27
en2 = 17

speed1 = 0
speed2 = 0

def setup():
    global pwm1,pwm2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(en1,GPIO.OUT)
    pwm1 = GPIO.PWM(en1,80)
    GPIO.setup(in3,GPIO.OUT)
    GPIO.setup(in4,GPIO.OUT)
    GPIO.setup(en2,GPIO.OUT)
    pwm2 = GPIO.PWM(en2,50)
    pwm1.start(speed1)
    pwm2.start(speed2)

def bot_controls():
    if(msg != DISCONNECT_MESSAGE):
        to_array = [char for char in msg]
        print(to_array)
        speed1 = int(str(to_array[2]+to_array[3]+to_array[4]))
        speed2 = int(str(to_array[8]+to_array[9]+to_array[10]))
        pwm1.ChangeDutyCycle(speed1)
        pwm2.ChangeDutyCycle(speed2)
        if(to_array[1] == 'f'):
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
        elif (to_array[1] == 'r'):
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
        if(to_array[7] == 'f'):
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
        elif(to_array[7] == 'r'):
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)

            
    
def handle_client(conn, addr):
    print('NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        global msg
        msg = conn.recv(12).decode(FORMAT)
        global chars
        chars = (msg, 'utf-8')
        if len(msg) > 1 :
            #print(msg)
            conn.send(bytes('ACK', 'utf-8')) # ACK may be needed
            
        if (msg == DISCONNECT_MESSAGE) :
            print('Disconnected')
            connected = False
        bot_controls()
        msg = ''    

        
        #conn.send("Msg received".encode(FORMAT))

    conn.close()
        

def start():
    server.listen()
    print("[LISTENING] Server is listening on {SERVER}")
    GPIO.setwarnings(False)
    setup()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(threading.activeCount() - 1)


print("[STARTING] server is starting...")
start()
