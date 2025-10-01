from machine import Pin, PWM

from time import sleep

import math

class servo:

    def __init__ ( self, pin ):
        
        self.pwm = PWM( Pin(pin), freq=50, duty=0 )
        
    def rotate( self, angle ):
        
        self.pwm.duty(int(((angle)/180 * 2 + 0.5) / 20 * 1023))

def main():
    
    gates = servo(23)
    
    while True:
        
        gates.rotate(90)
        sleep(2)
        
        gates.rotate(0)
        sleep(2)

if __name__ == "__main__":
    
    main()
