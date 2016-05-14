#The Cage main code block executed by bashbash.sh
#Author: Mehmet Akbulut
#MIT License

#Standard Packages
import os
import sys
import time
import socket
import netifaces
#The Cage Scripts
import threading
import sandwich
import battery

#Should GUI run at start up?
gui_at_startup = True

#Which internet device (wifi, eth etc..) to sue?
internet_interface = 'wlan0'

#Should we print the network details at start-up?
ShouldPrintNetwork = True

class cage(object):
    def __init__(self):
        """Initialize the Cage"""
        self.HOST="None"
        self.IP="None"
        self.MAC="None"
        self.ROSMASTER="None"
        self.ROSTHREAD="None"
        self.operation="Booting Up"
        self.drone="None"
        self.Alive=False
        self.bootupTime=time.time()

        #Verify network connection
        self.checkNetwork()
        if ShouldPrintNetwork==True:
            print("Hostname: "+self.HOST+" | IP Address: "+self.IP+" | MAC Address: "+self.MAC)

        time.sleep(1)
        
        #Sandwich Mechanism
        try:
            self.mechanism=self.initSandwichMechanism()
        except:
            self.mechanism=None
            print("Sandwich Mechanism failed to initialize.")

        #Battery Charger
        try:
            self.charger=self.initBatteryCharger()
        except:
            self.charger=None
            print("Battery Charger failed to initialize.")

        self.Alive=True

        #Robot Operating System
        self.initROS()

        #Touchscreen GUI
        try:
            if gui_at_startup == True:
                self.initUI()
        except:
            print("GUI thread failed to start.")

        self.operation="Ready"
        #while self.Alive==True:
        #    self.loop()
        #    time.sleep(0)

    def loop(self):
        pass
    
    #Initializers
    def checkNetwork(self):
        self.operation="Checking Network"
        try:
            self.HOST=socket.gethostname()
            self.NET=netifaces.ifaddresses(internet_interface)
            self.IP=self.NET[netifaces.AF_INET][0]['addr']
            self.MAC=self.NET[netifaces.AF_LINK][0]['addr']
        except:
            print("Couldn't verify network.")
        self.operation="Checking Network"
            

    def initSandwichMechanism(self):
        """Creates an instance of the Sandwich Mechanism controller object"""
        return sandwich.mechanism()
        #pass

    def initBatteryCharger(self):
        """Creates an instance of the Battery Charger controller object"""
        return battery.charger()
        #pass

    def initROS(self):
        """Starts the ROS"""
        self.operation="Initiating ROS"
        import roskid
        thread = threading.Thread(target=roskid.begin, args=([self]))
        thread.daemon = True
        thread.name = "ROSKid-"+thread.name
        thread.start()
#        time.sleep(5)            
#        self.ros = roskid.kid
#        self.ros.master = self        
        self.operation="Ready"
#        except:
#            print("ROSKid failed to initialize.")
#            self.operation="Ready"

    def initUI(self):
        """Start the User Interface"""
        self.operation="Initiating UI"
        import runtime
        thread = threading.Thread(target=runtime.begin, args=([self]))
        thread.daemon = True
        thread.name = "UI-"+thread.name
        thread.start()
        self.operation="Ready"

    def instance(self):
        return self

    def runAutostart(self):
        self.operation="Autostart in Progress"
        self.operation="Autostart: Catching"
        state=0
        resp=self.runCatch()
        if resp==1:
            self.operation="Autostart: Charging"
            resp=self.runCharge()
            if resp==1:
                state=1
            else:
                self.operation="Autostart: Failed to Charge"
                state=0
        else:
            state=-1
            self.operation="Autostart: Failed to Catch"
        time.sleep(1)
        self.operation="Ready"
        return state

    def runStop(self):
        self.operation="Stopping"
        if self.mechanism!=None and self.mechanism.Alive==True:
            self.mechanism.mode(0)
        if self.charger!=None and self.charger.Alive==True:
            self.charger.stop()
        self.operation="Ready"
            

    def runCharge(self):
        self.operation="Initating Charge"
        if self.charger==None:
            print("Battery Charger is disabled.")
            return False
        resp=self.charger.charge()
        self.operation="Ready"
        return resp

    def runCatch(self):
        self.operation="Initating Catch"
        if self.mechanism==None:
            print("Battery Charger is disabled.")
            return False
        resp=self.mechanism.catch()
        self.operation="Ready"
        return resp

    def runRelease(self):
        self.operation="Initiating Release"
        if self.mechanism==None:
            print("Sandwich Mechanism is disabled.")
            return False
        resp = self.mechanism.release()
        self.operation="Ready"
        return resp

    def restart(self):
        #os.execl('runme.sh','')
        pass

    def reboot(self):
        command = "/usr/bin/sudo /sbin/shutdown -r now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print(output)

    def shutdown(self):
        command = "/usr/bin/sudo /sbin/shutdown now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output        
        
#Main Routine
if __name__ == '__main__':
    c=cage()
    
