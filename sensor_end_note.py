import RPI.GPIO as GPIO
import time
import socket
import struct
import json

def setup_ultrasonic(trig_pin,echo_pin):
    GPIO.setup(trig_pin,GPIO.OUT)
    GPIO.setup(trig_pin,GPIO.IN)

def mesure_distance(trig_pin,echo_pin):
    GPIO.output(trig_pin,False)
    print("waiting for sensor to setle")
    #time.sleep(2)
    GPIO.output(trig_pin,True)
    time.sleep(0.00001)

    GPIO(trig_pin,False)

    pulse_start =time.time()
    while GPIO.input(echo_pin) ==1:
        pulse_end =time.time()
    
    pulse_duration = pulse_end - pulse_start
    print("pulse_duration",pulse_duration)

    distance = pulse_duration * 17150
    distance_2 = round(distance,2)

    return distance_2,pulse_duration

def send_data_receiver(distance_data,time_mesurement,movement,receiver_ip,receveir_port):
    try:
        #creation dune soccket
        sender_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #server adrress and port
        server_address =(receiver_ip,receveir_port)

        # connnexion a la socket du raspberry pi recepteur
        #sender_socket.connect((receiver_ip,receveir_port))

        # envoi de donnes 
        data_to_send = [time_mesurement,distance_data,movement]
        print(f'view data to send:{data_to_send}')
        json_data =json.dumps(data_to_send)
        sender_socket.sendto(json_data.encode("utf-8"),server_address)
        time.sleep(0.1)# time before sendig the nex serie of data
    except Exception as e:
        print(f" an error occured while sending data {e}")


def main():
    TRIG_PIN=23
    ECHO_PIN=24
    tres = 182
    notice =0
    GPIO.setmode(GPIO.BCM)
    try:
        setup_ultrasonic(TRIG_PIN,ECHO_PIN)
        mesurement =[]
        while True:
            distance_mesurement = mesure_distance(TRIG_PIN,ECHO_PIN)
            print(distance_mesurement)
            distance1,time_calcul = distance_mesurement
            mesurement.append({"distance":distance1,"time":time_calcul})
            RECEIVER_IP="192.168.222.123"
            RECEIVER_PORT = 1234
            if distance1<tres:
                notice=1
            else:
                notice=0
            print(notice)
            send_data_receiver(distance1,time_calcul,notice,RECEIVER_IP,RECEIVER_PORT)
            time.sleep(0.1)


    except KeyboardInterrupt:
        # ddans le cas ou on touche le clavier(ctl+c),cela va arreter le programme et 
        #le nettoyer
        print("cleaniing")
        GPIO.cleanup()
        print("all mesure",mesurement)
    
    except Exception as e :
        print(f" an error occured while sending data {e}")
        GPIO.cleanup()
    

if __name__ == "__main__":
    main()