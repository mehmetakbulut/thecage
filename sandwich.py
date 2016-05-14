#Controls the Wall Modules on the Sandwich Mechanism along with processing all of the sensory data
#Author: Mehmet Akbulut and Zoe Dickert
#MIT License

import threading
import time
try:
    import analog
    import digital
except:
    print("Sandwich Mechanism can not access sensors")
    raise

class mechanism(object):
    def __init__(self):
        """Create new thread"""
        self.thread = threading.Thread(target=self.initialize, args=())
        self.thread.daemon=True
        self.thread.name = "Sandwich-"+self.thread.name
        self.thread.start()

    def initialize(self):
        """Initialize the sandwich mechanism"""
        self.Alive=True
        self.fsrThreshold=3.1
        self.fsrCritical=1.2
        self.fsrHit=[0,0,0,0]
        self.limitHit=[[0,0],[0,0],[0,0],[0,0]]
        self.pins=[0,0,0,0]     #GPIO Pin Numbers
        self.pins[0]=[40,11]
        self.pins[1]=[12,13]
        self.pins[2]=[15,16]
        self.pins[3]=[18,22]
        self.motor=[0,0,0,0]    #Motor State
        self.direction=0        #Neutral, Catch, Release
        self.fsr=[0,0,0,0]
        self.limit=[[0,0],[0,0],[0,0],[0,0]]
        self.speed=0.1          #Percent speed of the motors

        self.timeoutCatch=5     #How long to wait in seconds until timing out a catch operation?
        self.timeoutRelease=5   #How long to wait in seconds until timing out a release operation?
        
        self.setpins()
        self.mode(0)
        
        while self.Alive:
            self.loop()

        self.die()
        pass


    def loop(self):
        """Continous operation"""
        self.readFSR()
        self.readLimit()
        #self.report()
        #self.fsrHit=[0,0,0,0]

        #Check limit switches and stop motors that are at the end of their tracks
        for i in range(len(self.pins)):
            if self.limit[i][1]==1 and self.direction==1:
                self.command(i,0)
                #print(str(i)+" hit switch 1")
            if self.limit[i][0]==1 and self.direction==-1:
                self.command(i,0)
                #print(str(i)+" hit switch 0")
                #print("LIMIT"+str(i)+" is hit!")

        #Check FSRs and stop motors that are squeezing a drone
        if self.direction==1 and self.fsr[0]<self.fsrThreshold and self.fsr[3]<self.fsrThreshold:
            self.command(0,0)
            self.command(3,0)
            self.fsrHit[0]=1
            self.fsrHit[3]=1
            #print("FSR0 & FSR3 are hit!")
        else:
            self.fsrHit[0]=0
            self.fsrHit[3]=0

        if self.direction==1 and self.fsr[1]<self.fsrThreshold and self.fsr[2]<self.fsrThreshold:
            self.command(1,0)
            self.command(2,0)
            self.fsrHit[1]=1
            self.fsrHit[2]=1
            #print("FSR1 & FSR2 are hit!")
        else:
            self.fsrHit[1]=0
            self.fsrHit[2]=0            

        time.sleep(0.1)
        #print('t')

    def mode(self,direction):
        """Set the system wide mechanism operation. 0=Neutral, 1=Catch, -1=Release"""
        self.direction=direction
        print("Mode is set to "+str(direction))
        for i in range(len(self.pins)):
            self.command(i,direction)

    def command(self,motornum,direction):
        """Command individual motor"""
        try:
            self.motor[motornum]=direction
            if direction==1:        #Forward
                digital.writePWM(self.pins[motornum][0],self.speed)
                digital.writePWM(self.pins[motornum][1],0)
            elif direction==-1:     #Reverse
                digital.writePWM(self.pins[motornum][0],0)
                digital.writePWM(self.pins[motornum][1],self.speed)
            else:                   #Neutral
                digital.writePWM(self.pins[motornum][0],0)
                digital.writePWM(self.pins[motornum][1],0)
        except:
            print("Sandwich Mechanism had an issue commanding motors.")

    def readFSR(self):
        """Read FSR values in volts"""
        try:
            self.fsr[0] = analog.read(0)
            self.fsr[1] = analog.read(1)
            self.fsr[2] = analog.read(2)
            self.fsr[3] = analog.read(3)
            if -2 in self.fsr:
                time.sleep(0.5)
                self.fsr[0] = analog.read(0)
                self.fsr[1] = analog.read(1)
                self.fsr[2] = analog.read(2)
                self.fsr[3] = analog.read(3)
            if -2 in self.fsr:
                print("Sandwich Mechanism FSR reading failed.")
                self.die()
        except:
            print("Sandwich Mechanism had an issue reading FSRs.")

    def readLimit(self):
        """Read whether limit switchesh has been hit or not. 0=Not Hit, 1=Hit"""
        try:
            self.limit[0][0] = digital.read(29)
            self.limit[0][1] = digital.read(31)
            self.limit[1][0] = digital.read(32)
            self.limit[1][1] = digital.read(33)
            self.limit[2][0] = digital.read(35)
            self.limit[2][1] = digital.read(36)
            self.limit[3][0] = digital.read(37)
            self.limit[3][1] = digital.read(38)
        except:
            print("Sandwich Mechanism had an issue reading Limit Switches.")

    def setpins(self):
        """Set up pins for input and output"""
        digital.setpin(40,"OUTPUT")          #motor Q1 A: pin 7
        digital.setpin(11,"OUTPUT")         #motor Q1 B: pin 11
        
        digital.setpin(12,"OUTPUT")         #motor Q2 A: pin 12
        digital.setpin(13,"OUTPUT")         #motor Q2 B: pin 13

        digital.setpin(15,"OUTPUT")         #motor Q3 A: pin 15
        digital.setpin(16,"OUTPUT")         #motor Q3 B: pin 16

        digital.setpin(18,"OUTPUT")          #motor Q4 A: pin 18
        digital.setpin(22,"OUTPUT")         #motor Q4 B: pin 22

        digital.setPWM(40)                  #PWM objects for motor speed control
        digital.setPWM(11)
        digital.setPWM(12)
        digital.setPWM(13)
        digital.setPWM(15)
        digital.setPWM(16)
        digital.setPWM(18)
        digital.setPWM(22)
        
        digital.setpin(29,"INPUT")           #Limit Q1.1: pin 29
        digital.setpin(31,"INPUT")           #Limit Q1.2: pin 31

        digital.setpin(32,"INPUT")           #Limit Q2.1: pin 32
        digital.setpin(33,"INPUT")           #Limit Q2.2: pin 33

        digital.setpin(35,"INPUT")           #Limit Q3.1: pin 35
        digital.setpin(36,"INPUT")           #Limit Q3.2: pin 36

        digital.setpin(37,"INPUT")           #Limit Q4.1: pin 37
        digital.setpin(38,"INPUT")           #Limit Q4.2: pin 38

        analog.setpin(1,"INPUT")             #FSR Q1
        analog.setpin(2,"INPUT")             #FSR Q2
        analog.setpin(3,"INPUT")             #FSR Q3
        analog.setpin(4,"INPUT")             #FSR Q4

    def report(self):
        '''Print out mechanism variables'''
        print("DIRECTION "+str(self.direction))
        print("FSRTHRESHOLD "+str(self.fsrThreshold))
        print("FSR0 "+str(self.fsr[0]))
        print("FSR1 "+str(self.fsr[1]))
        print("FSR2 "+str(self.fsr[2]))
        print("FSR3 "+str(self.fsr[3]))
        print("LIMIT00 "+str(self.limit[0][0]))
        print("LIMIT01 "+str(self.limit[0][1]))
        print("LIMIT10 "+str(self.limit[1][0]))
        print("LIMIT11 "+str(self.limit[1][1]))
        print("LIMIT20 "+str(self.limit[2][0]))
        print("LIMIT21 "+str(self.limit[2][1]))
        print("LIMIT30 "+str(self.limit[3][0]))
        print("LIMIT31 "+str(self.limit[3][1]))
        

    def die(self):
        '''Kill the thread when no longer necessary'''
        self.Alive=False

    def catch(self):
        '''Initiate drone catching process'''
        self.mode(1)
        timeSpent=0
        while (0 in self.fsrHit) and (self.limit[0][1]==0 or self.limit[1][1]==0 or self.limit[2][1]==0 or self.limit[3][1]==0) and self.direction==1:
            if timeSpent >= self.timeoutCatch:
                self.mode(0)
                print("Sandwich Mechanism took too long trying to Catch.")
                return -1
            time.sleep(0.1)
            timeSpent=timeSpent+0.1
        #if (self.limit[0][1]==1 or self.limit[1][1]==1 or self.limit[2][1]==1 or self.limit[3][1]==1) and self.direction==1:
        #    return 0
        if not(0 in self.fsrHit) and self.direction==1:
            for i in range(len(self.fsrHit)):
                if self.fsrHit[i]>1:
                    print("Sandwich Mechanism reports that FSR Q"+str(i+1)+" is being crushed.")
                    return 2

            print("Sandwich Mechanism caught something.")
            return 1

        print("Sandwich Mechanism didn't catch anything.")
        return 0


    def release(self):
        '''Initiate drone releasing process'''
        self.mode(-1)
        timeSpent=0
        while (self.limit[0][0]==0 or self.limit[1][0]==0 or self.limit[2][0]==0 or self.limit[3][0]==0) and self.direction==-1:
            if timeSpent >= self.timeoutRelease:
                self.mode(0)
                print("Sandwich Mechanism took too long trying to Release.")
                return -1
            time.sleep(0.1)
            timeSpent=timeSpent+0.1

        print("Sandwich Mechanism released with success.")
        return 1
