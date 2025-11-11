from machine import Pin, PWM

from neopixel import NeoPixel

from time import sleep_ms

import math

MAIN_LOOP_DELAY     = 100
LIGHTS_SWITCH_DELAY = 300

STATE_CLOSED = 0
STATE_OPENED = 1

LOCK_BUTTON_PIN  = 6
OPEN_BUTTON_PIN  = 7
LOCK_SENSOR_PIN  = 5
OPEN_SENSOR_PIN  = 2
LIGHTS_PIN       = 4
GATES_PIN        = 0

class Gates:

    def __init__ ( self, pin ):
        
        self.pwm = PWM( Pin(pin), freq = 50, duty = 0 )
        
    def rotate( self, angle ):
        
        self.pwm.duty( int((angle / 180 * 2 + 0.5) / 20 * 1023) )

    def lock( self ):

        self.rotate( 0 )

    def open( self ):

        self.rotate( 90 )
        
class Lights:
    
    def __init__ ( self, pin, interval ):
        
        self.np = NeoPixel( Pin(pin, Pin.OUT), 2)

        self.RED = ( 255, 0, 0 )
        self.NON = ( 0, 0, 0 )
        
        self.np[0] = self.NON
        self.np[1] = self.NON
        self.np.write()
        
        self.CNT_MAX = int( interval / MAIN_LOOP_DELAY )
        
        self.counter = self.CNT_MAX
        
    def reset( self ):
        
        self.np[0] = self.NON
        self.np[1] = self.NON
        self.np.write()
        
        self.counter = self.CNT_MAX
        
    def update( self ):
        
        self.counter = self.counter - 1
        
        if self.np[0] == self.NON and self.np[1] == self.NON:
            
            self.np[0] = self.RED
            self.np[1] = self.NON
            self.np.write()
            
        if self.counter != 0: return

        tmp = self.np[0]
        self.np[0] = self.np[1]
        self.np[1] = tmp
        self.np.write()

        self.counter = self.CNT_MAX

class Control:

    def __init__( self, open_pin, lock_pin ):

        self.open = Pin(open_pin, Pin.IN, Pin.PULL_UP)
        self.lock = Pin(lock_pin, Pin.IN, Pin.PULL_UP)

    def is_open_clicked( self ):

        return not bool(self.open.value())

    def is_lock_clicked( self ):

        return not bool(self.lock.value())


class Sensors:

    def __init__( self, open_pin, lock_pin ):

        self.open = Pin(open_pin, Pin.IN)
        self.lock = Pin(lock_pin, Pin.IN)

    def is_open_triggered( self ):

        return not bool(self.open.value())

    def is_lock_triggered( self ):

        return not bool(self.lock.value())

def main():

    sensors = Sensors( OPEN_SENSOR_PIN, LOCK_SENSOR_PIN )

    control = Control( OPEN_BUTTON_PIN, LOCK_BUTTON_PIN )

    lights = Lights(LIGHTS_PIN, LIGHTS_SWITCH_DELAY)

    gates = Gates( GATES_PIN )

    state = STATE_OPENED

    lights.reset()
    
    gates.open()

    while True:
            
        if (sensors.is_open_triggered() or control.is_open_clicked()) and state != STATE_OPENED:
            
            gates.open()
            lights.reset()
            state = STATE_OPENED

        if (sensors.is_lock_triggered() or control.is_lock_clicked())  and state != STATE_CLOSED:

            gates.lock()
            lights.reset()
            state = STATE_CLOSED

        if state == STATE_CLOSED: lights.update()
        
        sleep_ms( MAIN_LOOP_DELAY )

if __name__ == "__main__":
    
    main()
