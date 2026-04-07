import datetime
import time 

alarma = datetime.time(11,11,45)

while True: 
    hora_actual = datetime.datetime.now().time().replace(microsecond=0)
    if alarma >= hora_actual:
        print("Llegó la hora!")
        break
    time.sleep(1)