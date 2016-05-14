#Handles all of the ROS/WiFi communications and controls
#Author: Mehmet Akbulut
#MIT License

#try:
import sys
#sys.path.append('/home/pi/ros_catkin_ws/devel_isolated/rosbag/lib/python2.7/dist-packages')
#sys.path.append('/opt/ros/indigo/lib/python2.7/dist-packages')

import threading
import rospy
from std_msgs.msg import String
#except:
#    print("ROS Packages failed to import.")

Types = ['MAIN','BATTERY','SANDWICH']
Messages = ['Associate','Disassociate','Autostart','Stop','Charge','Discharge','Catch','Release','Reboot','Shutdown','VPN','Report']
kid = None
class ros(object):
    def __init__(self,master=None):
        """Initialize the Robot Operating System"""
        print('init')
        if master!=None:
       #     print('master is not none')
            self.master=master
            print(self.master)
            print('ROS Master is assigned')
        else:
            print('ROS Master is not assigned')
#        while self.master==None:
#            pass
        self.Alive = True
        self.nodename = self.master.HOST
        self.topicname = self.master.HOST
        self.node=rospy.init_node(self.nodename, anonymous=False, disable_signals=True)
        self.sub=rospy.Subscriber(self.topicname+"_RX", String, self.callback)
        self.pub=rospy.Publisher(self.topicname+"_TX", String, queue_size=10)

        self.rate=rospy.Rate(2) #Battery Charger and Sandwich Mechanism data broadcasting rate
        
        self.rosprint("MAIN:Booting Up")

        #Start up an independent loop to broadcast information
        thread = threading.Thread(target=self.loop, args=())
        thread.daemon = True
        thread.name = "ROSKid-"+thread.name
        thread.start()

        #Keep the ros object running
        rospy.spin()

    def loop(self):
        while self.Alive==True:
            #Publish Battery Charger Data
            try:
                self.rosprint("BATTERY:"+self.master.charger.receivedData)
            except:
                print("ROSKid failed to publish Battery Charger data.")
            #Publish Sandwich Mechanism Data
            try:
                self.rosprint("SANDWICH:"+"Mode "+str(self.master.mechanism.direction)
                    +"|Q1|Motor "+str(self.master.mechanism.motor[0])+"|FSR "+str(self.master.mechanism.fsr[0])+"|LSO "+str(self.master.mechanism.limit[0][0])+"|LSI "+str(self.master.mechanism.limit[0][1])
                    +"|Q2|Motor "+str(self.master.mechanism.motor[1])+"|FSR "+str(self.master.mechanism.fsr[1])+"|LSO "+str(self.master.mechanism.limit[1][0])+"|LSI "+str(self.master.mechanism.limit[1][1])
                    +"|Q3|Motor "+str(self.master.mechanism.motor[2])+"|FSR "+str(self.master.mechanism.fsr[2])+"|LSO "+str(self.master.mechanism.limit[2][0])+"|LSI "+str(self.master.mechanism.limit[2][1])
                    +"|Q4|Motor "+str(self.master.mechanism.motor[3])+"|FSR "+str(self.master.mechanism.fsr[3])+"|LSO "+str(self.master.mechanism.limit[3][0])+"|LSI "+str(self.master.mechanism.limit[3][1]))
            except:
                print("ROSKid failed to publish Sandwich Mechanism data.")

            self.rate.sleep()

    def rosprint(self,message):
        """Broadcasts the given message on the ROS topic"""
        self.pub.publish(message)
#        print("rosprinting")

    def callback(self,data):
        """Handles messages received"""
#       print("ROSKid received a message.")

        #Process message in a new thread so we don't halt operations
        thread = threading.Thread(target=self.processMessage, args=([data]))
        thread.daemon = True
        thread.name = "ROSKid-"+thread.name
        thread.start()

    def processMessage(self,data):
        """Process received messages"""
        message=str(data)[6:]
        print("ROS > "+message)
        try:
            for i in Messages:
                if message[:len(i)]==i:
                    resp=False
                    if i=="Associate":
                        self.master.drone=message[len(i)+1:]
                        self.rosprint("MAIN:Drone "+self.master.drone+" Acquired")
                    elif i=="Disassociate":
                        self.rosprint("MAIN:Drone "+self.master.drone+" Left")
                        self.master.drone="None"
                    elif i=="Autostart":
                        self.rosprint("MAIN:Initaiting Autostart")
                        resp=self.master.runAutostart()
                        if resp==1:
                            self.rosprint("MAIN:Finished Autostart|Success")
                        elif resp==0:
                            self.rosprint("MAIN:Finished Autostart|Charge Failed")
                        elif resp==-1:
                            self.rosprint("MAIN:Finished Autostart|Catch Failed")
                        else:
                            self.rosprint("MAIN:Finished Autostart|Failure")
                    elif i=="Stop":
                        self.rosprint("MAIN:Initaiting Stop")
                        self.master.runStop()
                    elif i=="Charge":
                        self.rosprint("MAIN:Initaiting Charge")
                        resp=self.master.runCharge()
                        if resp==True:
                            self.rosprint("MAIN:Started Charge")
                        else:
                            self.rosprint("MAIN:Failed Charge")
                    elif i=="Discharge":
                        self.rosprint("MAIN:Initaiting Discharge")
                        resp=self.master.runDischarge()
                    elif i=="Catch":
                        self.rosprint("MAIN:Initaiting Catch")
                        resp=self.master.runCatch()
                        if resp==1:
                            self.rosprint("MAIN:Finished Catch|Success")
                        elif resp==0:
                            self.rosprint("MAIN:Finished Catch|Nothing")
                        elif resp==-1:
                            self.rosprint("MAIN:Finished Catch|Timeout")
                        elif resp==2:
                            self.rosprint("MAIN:Finished Catch|FSR Error")
                    elif i=="Release":
                        self.rosprint("MAIN:Initaiting Release")
                        resp=self.master.runRelease()
                        if resp==1:
                            self.rosprint("MAIN:Finished Release|Success")
                        elif resp==-1:
                            self.rosprint("MAIN:Finished Release|Timeout")
                    elif i=="Reboot":
                        self.rosprint("MAIN:Rebooting")
                        self.master.reboot()
                    elif i=="Shutdown":
                        self.rosprint("MAIN:Shutting Down")
                        self.master.shutdown()
                    elif i=="VPN":
                        self.master.VPN()
                    elif i=="Report":
                        self.master.report()
                    else:
                        print("ROSKid received unknown message.")
                    break
            raise
        except:
            print("ROSKid couldn't process message.")

    def instance(self):
        return self

def begin(master=None):
    """Constructor for the ROS object"""
    global kid
    kid = ros(master)
