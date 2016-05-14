#Wrapper code for interfacing with ADC
#Author: Mehmet Akbulut
#MIT License

import Adafruit_ADS1x15

#Create adc object. Optional parameters: address=0x49, bus=1
adc = Adafruit_ADS1x15.ADS1015()
GAIN = 1

NDMAX = -2048	#Negative Digitzed Maximum (i.e. the lowest ADC output)
PDMAX = 2047	#Positive Digitazed Maximum (i.e. the highest ADC output)
NVMAX = -4.096	#Negative Voltage Maximum in Volts (i.e. the lowest input potential)
PVMAX = 4.096	#Positive Voltage Maximum in Volts (i.e. the highest input potential)

def setpin(pin,mode):
    '''Sets pin to INPUT or OUTPUT mode'''
    #print("Analog is always set to INPUT")
    if mode=="INPUT":
        return 0
    else:
        return -1

def read(pin):
    '''Returns the pin value'''
    if pin > 3 or pin < 0:
        return -1
    else:
        try:
            return adc2volts(adc.read_adc(pin, gain=GAIN))
        except:
            print("Analog reading failed.")
            return -2
#        return 1

def write(pin,value):
    '''Writes to the pin'''
    #print("Can't write to pin over ADC")
    return -1

def adc2volts(value):
    '''Converts ADC reading to Voltage'''
    return(value*(PVMAX-NVMAX)/(PDMAX-NDMAX))
