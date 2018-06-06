import time
import Adafruit_MCP4725
import socket
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#initialize mode pin
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

zero_speed = 125
max_speed = 4000
current_speed = zero_speed

previous_error = 0
sum_of_errors = 0

#automation algorithm(PID Controller)
def altitude_hold(current_altitude):
	global current_speed
	global previous_error
	global sum_of_errors
	
	#constants to change the magnitute of the throttle input
	target_altitude = 80.0
	KP = 2.0
	KD = 1.8
	KI = 0.1

#if previous_error == 0 and current_speed == zero_speed:
#current_speed = max_speed/2
	
	#calculate the distance the helicopter has to travel until it 
	#reaches the specified height(error) and convert that to speed
	error = target_altitude - current_altitude
	current_speed += error * KP + previous_error * KD + sum_of_errors * KI
	current_speed = max(min(max_speed, current_speed), zero_speed)

	previous_error = error
	sum_of_errors += error

	dac.set_voltage(int(current_speed))
	print("speed: ", current_speed)

#initilize mode
def initialize_controller():
    dac.set_voltage(zero_speed)
    time.sleep(1)
    dac.set_voltage(max_speed)
    time.sleep(2)
    dac.set_voltage(zero_speed)
    print("close switch")
    time.sleep(2)

# Create a DAC instance(I2C address and bus number).
dac = Adafruit_MCP4725.MCP4725(address=0x60, busnum=1)

#setup server ip and port and size of data to await
TCP_IP = '192.168.43.249'
TCP_PORT = 5005
BUFFER_SIZE = 20

#initialize socket and listen for connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

#accept always connection
conn, addr = s.accept()
print('Connection address:', addr)

while 1:
    #get data and check if empty to re-open the connection
    data = conn.recv(BUFFER_SIZE)
    if not data:
        dac.set_voltage(zero_speed)
        conn.close()
        s.listen(1)
        conn, addr = s.accept()
        print('Connection address:', addr)
    
    #convert to distance
    #distance = float(str(data).split("'")[1])
    distance = data
    
#    if GPIO.input(17) == 1:
#        initialize_controller()
#     elif int(float(distance)) < 400 and int(float(distance)) > 0:
    if int(float(distance)) < 400 and int(float(distance)) > 0:
    	print(distance)
    	altitude_hold(int(float(distance)))
    
    #send ack
    conn.send("ok")

    #dac.set_voltage(data) #max = 4096
conn.close()

