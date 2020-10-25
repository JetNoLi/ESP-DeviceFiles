from machine import Pin
from machine import Timer
from machine import SPI
import APIUtils as Utils

#Note all functions will be called from main, i.e will be able to input the function in the
#callback thus no need to map to a function
#Callback statement can only have 1 param = to pin it is triggered on
def listen(pin, edge, callback):
    edge = int(edge)
    
    #edge = 0 -> trigger on falling edge
    if edge == 0:
        pin.irq(trigger = Pin.IRQ_FALLING, handler = callback)

    #edge = 1 -> trigger on rising edge
    elif edge == 1:                                          
        pin.irq(trigger = Pin.IRQ_RISING, handler = callback)

    #edge = 10 -> trigger on either a rising or falling edge
    elif edge == 10:
        pin.irq(trigger = Pin.IRQ_FALLING | Pin.IRQ_RISING, handler = callback) 

    else:
        print("Error: Incorrect input paramaters, edge must = 0, 1, 10")
    


#toggles the value of the pin
def switch(pin):

    if pin.value():
        pin.off()
    
    else:
        pin.on()



#schedule device to do function every x amount of milliseconds
#time is in milliseconds 
#params is params to pass into function
def timedInterrupt(pinNum, function, time, timerFunction):
    timer = Timer(-1)           #initialize with ID of -1 as in docs
    timer.init(mode = Timer.PERIODIC, period = int(time), callback = timerFunction)

    return timer, pinNum, function



#end the timer i.e. deinitialize it
def endTimedInterrupt(timer):
    timer.deinit()
    timer = None
    #handle in main, update IOlist, timerFunction, pins final index stores timer Pin Number



#returns an ADC read of 
def ADC(pin):
    
    bitRead = pin.read()            #0-1024, 10 bit ADC 2^10 -1 = max = 1023, max = 1V
    
    voltage = (bitRead/1023.0)      #convert to analog reading 
    
    return voltage



def digitalRead(pin):
    return pin.value()


#default pins MISO - GPIO12, MOSI - GPIO13, SCLK - GPIO14
#Returns an instance of the SPI class which will be loaded in the main
def SetupSPI(baudRate, CPOL, CPHA): 
    return SPI(1, baudrate = baudRate, polarity = CPOL, phase = CPHA)



#Byte size is the number of bytes to read
#SPISetup is loaded in from main, and will store an instance of the machine.SPI
def SPIReadValue(byteSize, SPISetup):
    buffer = bytearray(byteSize)    #stores bits read in as they have to be in bytes format
    SPISetup.readinto(buffer)

    return Utils.formatSPIBytes(buffer)


#Create SPIRead if necessary, write to scheduled SPI pins in pin File
#To just read use format (0,0,0, byteSize, SPISetup)
#cannot set SPI from callback, only read from it 
def SPIRead(baudRate, CPOL, CPHA, byteSize, SPISetup):
    if SPISetup == None:
        SPISetup = SetupSPI(baudRate,CPOL,CPHA)
    
    return SPIReadValue(int(byteSize),SPISetup)
