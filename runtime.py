#Runtime handling for the GUI
#Author: Mehmet Akbulut
#MIT License

import sys
#import main
import time
import threading
from PySide import QtCore, QtGui
from gui import Ui_MainWindow
#from datetime import date
#from datetime import datetime
#from datetime import timedelta

class MyMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.master = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #Initialize Buttons
        self.ui.push_autostart.clicked.connect(self.buttonAutostart)
        self.ui.push_stop.clicked.connect(self.buttonStop)
        self.ui.push_charge.clicked.connect(self.buttonCharge)
        self.ui.push_discharge.clicked.connect(self.buttonDischarge)
        self.ui.push_catch.clicked.connect(self.buttonCatch)
        self.ui.push_release.clicked.connect(self.buttonRelease)
        #self.ui.push_reboot.clicked.connect(self.buttonReboot)
        #self.ui.push_shutdown.clicked.connect(self.buttonShutdown)
        
        #Rest
        self.set_process()
        self.timer = QtCore.QTimer()
        self.i = 0
        self.timer.timeout.connect(self.update)
        self.timer.start(500)
        
    def set_process(self):
        print('UI has started up.')
        self.color={'RGBwarning':"(255,0,0)",'RGBcaution':"(255,255,0)",'RGBok':"(0,255,0)",'RGBinfo':"(0,255,255)",'RGBwhite':"(255,255,255)",
                    'HEXwarning':"#ff0000",'HEXcaution':"#ffff00",'HEXok':"#00ff00",'HEXinfo':"#00ffff",'HEXwhite':"#ffffff"}
        
    def update(self):
        """Update the interface every so often as defined by self.timer.start(x)"""
        if self.i < 3:
            #self.ui.lineKerberos.setText(QtGui.QApplication.translate("MainWindow", str(""), None, QtGui.QApplication.UnicodeUTF8))
            #main.card()
            STATUS = "BOOTING UP"
        elif self.master.operation != None:
            STATUS = self.master.operation
        else:
            STATUS = "SYSTEM ERROR"
        
        #Acquire values from the subsystems
        HOST=self.master.HOST
        MAC=self.master.MAC
        IP=self.master.IP
        ROSMASTER=str(self.master.ROSMASTER)
        ROSTHREAD=str(self.master.ROSTHREAD)
        if self.master.drone == "None":
            DRONE="Cylon Raider 46F01Z1"
        else:
            DRONE=self.master.drone
        #print(HOST)
        if self.master.charger!=None and self.master.charger.Alive == True:
            CHARGERDEVICEcolor = self.color['RGBok']
            CHARGERDEVICE=str(self.master.charger.status)
            ELAPSEDTIME=self.master.charger.elapsed
            DRONEBATTERY=str('{0:.2f}'.format(self.master.charger.voltage))+"V "+str('{0:.2f}'.format(self.master.charger.current/1000))+"A "+str(self.master.charger.resistance)+"ohm "+str(self.master.charger.percentage)+"%"
            DRONECELL1=str('{0:.2f}'.format(self.master.charger.cell1))
            DRONECELL2=str('{0:.2f}'.format(self.master.charger.cell2))
            DRONECELL3=str('{0:.2f}'.format(self.master.charger.cell3))
            
        else:
            CHARGERDEVICEcolor = self.color['RGBwarning']
            CHARGERDEVICE="Disabled"
            ELAPSEDTIME=0
            DRONEBATTERY=None
            DRONECELL1=0
            DRONECELL2=0
            DRONECELL3=0

        if self.master.mechanism!=None and self.master.mechanism.Alive == True:
            SANDWICHMECHANISMcolor=self.color['RGBok']
            if self.master.mechanism.direction == 1:
                SANDWICHMECHANISM="Catch"
            elif self.master.mechanism.direction ==-1:
                SANDWICHMECHANISM="Release"
            else:
                SANDWICHMECHANISM="Neutral"

            q1fsr = self.master.mechanism.fsr[0]
            q2fsr = self.master.mechanism.fsr[1]
            q3fsr = self.master.mechanism.fsr[2]
            q4fsr = self.master.mechanism.fsr[3]

            q1limit0 = self.master.mechanism.limit[0][0]
            q1limit1 = self.master.mechanism.limit[0][1]
            q2limit0 = self.master.mechanism.limit[1][0]
            q2limit1 = self.master.mechanism.limit[1][1]
            q3limit0 = self.master.mechanism.limit[2][0]
            q3limit1 = self.master.mechanism.limit[2][1]
            q4limit0 = self.master.mechanism.limit[3][0]
            q4limit1 = self.master.mechanism.limit[3][1]

            if q1fsr>=self.master.mechanism.fsrThreshold:
                q1fsr="___ "+str(q1fsr)[:5]
                q1fsr_color=self.color['HEXcaution']
            elif q1fsr>=self.master.mechanism.fsrCritical:
                q1fsr="HIT "+str(q1fsr)[:5]
                q1fsr_color=self.color['HEXok']
            else:
                q1fsr="HIT "+str(q1fsr)[:5]
                q1fsr_color=self.color['HEXwarning']

            if q2fsr>=self.master.mechanism.fsrThreshold:
                q2fsr="___ "+str(q2fsr)[:5]
                q2fsr_color=self.color['HEXcaution']
            elif q2fsr>=self.master.mechanism.fsrCritical:
                q2fsr="HIT "+str(q2fsr)[:5]
                q2fsr_color=self.color['HEXok']
            else:
                q2fsr="HIT "+str(q2fsr)[:5]
                q2fsr_color=self.color['HEXwarning']

            if q3fsr>=self.master.mechanism.fsrThreshold:
                q3fsr="___ "+str(q3fsr)[:5]
                q3fsr_color=self.color['HEXcaution']
            elif q3fsr>=self.master.mechanism.fsrCritical:
                q3fsr="HIT "+str(q3fsr)[:5]
                q3fsr_color=self.color['HEXok']
            else:
                q3fsr="HIT "+str(q3fsr)[:5]
                q3fsr_color=self.color['HEXwarning']

            if q4fsr>=self.master.mechanism.fsrThreshold:
                q4fsr="___ "+str(q4fsr)[:5]
                q4fsr_color=self.color['HEXcaution']
            elif q4fsr>=self.master.mechanism.fsrCritical:
                q4fsr="HIT "+str(q4fsr)[:5]
                q4fsr_color=self.color['HEXok']
            else:
                q4fsr="HIT "+str(q4fsr)[:5]
                q4fsr_color=self.color['HEXwarning']

            if q1limit0==1:
                q1limit0="HIT"
                q1limit0color=self.color['HEXwarning']
            else:
                q1limit0="___"
                q1limit0color=self.color['HEXcaution']

            if q1limit1==1:
                q1limit1="HIT"
                q1limit1color=self.color['HEXwarning']
            else:
                q1limit1="___"
                q1limit1color=self.color['HEXcaution']

            if q2limit0==1:
                q2limit0="HIT"
                q2limit0color=self.color['HEXwarning']
            else:
                q2limit0="___"
                q2limit0color=self.color['HEXcaution']

            if q2limit1==1:
                q2limit1="HIT"
                q2limit1color=self.color['HEXwarning']
            else:
                q2limit1="___"
                q2limit1color=self.color['HEXcaution']

            if q3limit0==1:
                q3limit0="HIT"
                q3limit0color=self.color['HEXwarning']
            else:
                q3limit0="___"
                q3limit0color=self.color['HEXcaution']

            if q3limit1==1:
                q3limit1="HIT"
                q3limit1color=self.color['HEXwarning']
            else:
                q3limit1="___"
                q3limit1color=self.color['HEXcaution']

            if q4limit0==1:
                q4limit0="HIT"
                q4limit0color=self.color['HEXwarning']
            else:
                q4limit0="___"
                q4limit0color=self.color['HEXcaution']

            if q4limit1==1:
                q4limit1="HIT"
                q4limit1color=self.color['HEXwarning']
            else:
                q4limit1="___"
                q4limit1color=self.color['HEXcaution']
            
        else:
            SANDWICHMECHANISMcolor = self.color['RGBwarning']
            SANDWICHMECHANISM="Disabled"
            q1fsr_color=self.color['HEXwarning']
            q2fsr_color=self.color['HEXwarning']
            q3fsr_color=self.color['HEXwarning']
            q4fsr_color=self.color['HEXwarning']
            q1limit0color=self.color['HEXwarning']
            q2limit0color=self.color['HEXwarning']
            q3limit0color=self.color['HEXwarning']
            q4limit0color=self.color['HEXwarning']
            q1limit1color=self.color['HEXwarning']
            q2limit1color=self.color['HEXwarning']
            q3limit1color=self.color['HEXwarning']
            q4limit1color=self.color['HEXwarning']
            q1fsr=""
            q2fsr=""
            q3fsr=""
            q4fsr=""
            q1limit0=""
            q2limit0=""
            q3limit0=""
            q4limit0=""
            q1limit1=""
            q2limit1=""
            q3limit1=""
            q4limit1=""

        UPTIME=int(time.time() - self.master.bootupTime)

        IPcolor = self.color['RGBwarning']
        ROScolor = self.color['RGBwarning']
        DRONEcolor = self.color['RGBinfo']
        DRONEBATTERYcolor = self.color['RGBcaution']
        DRONECELL1color = self.color['RGBcaution']
        DRONECELL2color = self.color['RGBcaution']
        DRONECELL3color = self.color['RGBcaution']
        ELAPSEDTIMEcolor = self.color['RGBinfo']
        UPTIMEcolor = self.color['RGBinfo']
        STATUScolor = self.color['RGBwhite']
        NETWORKcolor = self.color['RGBinfo']
        
        if str(IP)!="None":
            IPcolor = self.color['RGBok']
        else:
            IP="Disconnected"

        if str(ROSMASTER)=="None":
            ROSMASTER="Master:None"
        if str(ROSTHREAD)=="None":
            ROSTHREAD="Topics:None"
        if str(CHARGERDEVICE)=="Enabled":
            CHARGERDEVICEcolor=self.color['RGBok']            

        #Update Color and Style
        self.ui.label_internetO.setStyleSheet("color: rgb"+IPcolor+";")
        self.ui.label_rosO.setStyleSheet("color: rgb"+ROScolor+";")
        self.ui.label_chargerO.setStyleSheet("color: rgb"+CHARGERDEVICEcolor+";")
        self.ui.label_mechanismO.setStyleSheet("color: rgb"+SANDWICHMECHANISMcolor+";")
        self.ui.label_droneO.setStyleSheet("color: rgb"+DRONEcolor+";")
        self.ui.label_dronebatteryO.setStyleSheet("color: rgb"+DRONEBATTERYcolor+";")
        self.ui.label_dronecell1O.setStyleSheet("color: rgb"+DRONECELL1color+";")
        self.ui.label_dronecell2O.setStyleSheet("color: rgb"+DRONECELL2color+";")
        self.ui.label_dronecell3O.setStyleSheet("color: rgb"+DRONECELL3color+";")
        self.ui.label_elapsedO.setStyleSheet("color: rgb"+ELAPSEDTIMEcolor+";")
        self.ui.label_uptimeO.setStyleSheet("color: rgb"+UPTIMEcolor+";")
        self.ui.label_status.setStyleSheet("color: rgb"+STATUScolor+";")
        self.ui.label_network.setStyleSheet("color: rgb"+NETWORKcolor+";")
        #Update Text
        self.ui.label_Q1.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Q1</span></p><p align=\"center\"><span style=\" font-weight:600;\">FSR: </span><span style=\" color:"+q1fsr_color+";\">"+str(q1fsr)+"v</span></p><p align=\"center\"><span style=\" font-weight:600;\">LSO: </span><span style=\" color:"+q1limit0color+";\">"+str(q1limit0)+"  </span><span style=\" font-weight:600;\">LSI: </span><span style=\" color:"+q1limit1color+";\">"+str(q1limit1)+"</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_Q2.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Q2</span></p><p align=\"center\"><span style=\" font-weight:600;\">FSR: </span><span style=\" color:"+q2fsr_color+";\">"+str(q2fsr)+"v</span></p><p align=\"center\"><span style=\" font-weight:600;\">LSO: </span><span style=\" color:"+q2limit0color+";\">"+str(q2limit0)+"  </span><span style=\" font-weight:600;\">LSI: </span><span style=\" color:"+q2limit1color+";\">"+str(q2limit1)+"</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_Q3.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Q3</span></p><p align=\"center\"><span style=\" font-weight:600;\">FSR: </span><span style=\" color:"+q3fsr_color+";\">"+str(q3fsr)+"v</span></p><p align=\"center\"><span style=\" font-weight:600;\">LSO: </span><span style=\" color:"+q3limit0color+";\">"+str(q3limit0)+"  </span><span style=\" font-weight:600;\">LSI: </span><span style=\" color:"+q3limit1color+";\">"+str(q3limit1)+"</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_Q4.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Q4</span></p><p align=\"center\"><span style=\" font-weight:600;\">FSR: </span><span style=\" color:"+q4fsr_color+";\">"+str(q4fsr)+"v</span></p><p align=\"center\"><span style=\" font-weight:600;\">LSO: </span><span style=\" color:"+q4limit0color+";\">"+str(q4limit0)+"  </span><span style=\" font-weight:600;\">LSI: </span><span style=\" color:"+q4limit1color+";\">"+str(q4limit1)+"</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        
        #self.ui.label_Q1.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Q1</span></p><p align=\"center\"><span style=\" font-weight:600;\">FSR: </span><span style=\" color:"+q1fsr_color+";\">"+str(q1fsr)+"v</span></p><p align=\"center\"><span style=\" font-weight:600;\">Limit Switch Outside: </span><span style=\" color:"+q1limit0color+";\">"+str(q1limit0)+"</span></p><p align=\"center\"><span style=\" font-weight:600;\">Limit Switch Inside: </span><span style=\" color:"+q1limit1color+";\">"+str(q1limit1)+"</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        #self.ui.label_Q2.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Q2</span></p><p align=\"center\"><span style=\" font-weight:600;\">FSR: </span><span style=\" color:"+q2fsr_color+";\">"+str(q2fsr)+"v</span></p><p align=\"center\"><span style=\" font-weight:600;\">Limit Switch Outside: </span><span style=\" color:"+q2limit0color+";\">"+str(q2limit0)+"</span></p><p align=\"center\"><span style=\" font-weight:600;\">Limit Switch Inside: </span><span style=\" color:"+q2limit1color+";\">"+str(q2limit1)+"</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        #self.ui.label_Q3.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Q3</span></p><p align=\"center\"><span style=\" font-weight:600;\">FSR: </span><span style=\" color:"+q3fsr_color+";\">"+str(q3fsr)+"v</span></p><p align=\"center\"><span style=\" font-weight:600;\">Limit Switch Outside: </span><span style=\" color:"+q3limit0color+";\">"+str(q3limit0)+"</span></p><p align=\"center\"><span style=\" font-weight:600;\">Limit Switch Inside: </span><span style=\" color:"+q3limit1color+";\">"+str(q3limit1)+"</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        #self.ui.label_Q4.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Q4</span></p><p align=\"center\"><span style=\" font-weight:600;\">FSR: </span><span style=\" color:"+q4fsr_color+";\">"+str(q4fsr)+"v</span></p><p align=\"center\"><span style=\" font-weight:600;\">Limit Switch Outside: </span><span style=\" color:"+q4limit0color+";\">"+str(q4limit0)+"</span></p><p align=\"center\"><span style=\" font-weight:600;\">Limit Switch Inside: </span><span style=\" color:"+q4limit1color+";\">"+str(q4limit1)+"</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_internetO.setText(QtGui.QApplication.translate("MainWindow", str(IP), None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_rosO.setText(QtGui.QApplication.translate("MainWindow", str(ROSMASTER) + " " + str(ROSTHREAD), None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_chargerO.setText(QtGui.QApplication.translate("MainWindow", str(CHARGERDEVICE), None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_mechanismO.setText(QtGui.QApplication.translate("MainWindow", str(SANDWICHMECHANISM), None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_droneO.setText(QtGui.QApplication.translate("MainWindow", str(DRONE), None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_dronebatteryO.setText(QtGui.QApplication.translate("MainWindow", str(DRONEBATTERY), None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_dronecell1O.setText(QtGui.QApplication.translate("MainWindow", "C1: "+str(DRONECELL1)+"v", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_dronecell2O.setText(QtGui.QApplication.translate("MainWindow", "C2: "+str(DRONECELL2)+"v", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_dronecell3O.setText(QtGui.QApplication.translate("MainWindow", "C3: "+str(DRONECELL3)+"v", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_elapsedO.setText(QtGui.QApplication.translate("MainWindow", str(ELAPSEDTIME)+"s", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_uptimeO.setText(QtGui.QApplication.translate("MainWindow", str(UPTIME)+"s", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_status.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p align=\"center\">"+str(STATUS)+"</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_network.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p align=\"center\">"+str(HOST)+"</p><p align=\"center\">"+str(MAC)+"</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

        self.i += 1
         
    def reset(self):
        self.i=-1
        pass

    def buttonAutostart(self):
        """Wrapper for Autostart"""
        thread = threading.Thread(target=self.master.runAutostart, args=())
        thread.daemon = True
        thread.name = "UI-Autostart-"+thread.name
        thread.start()
        
    def buttonStop(self):
        """Wrapper for Stop"""
        thread = threading.Thread(target=self.master.runStop, args=())
        thread.daemon = True
        thread.name = "UI-Stop-"+thread.name
        thread.start()
        
    def buttonCharge(self):
        """Wrapper for Charge"""
        thread = threading.Thread(target=self.master.runCharge, args=())
        thread.daemon = True
        thread.name = "UI-Charge-"+thread.name
        thread.start()

    def buttonDischarge(self):
        """Wrapper for Discharge"""
        #Unimplemented currently. You can use buttonCharge as a template. Check the Instructions dictionary in the battery.py file for implementation.
        #Must create runDischarge() in main.py and discharge() battery.py if implemented.
        pass

    def buttonCatch(self):
        """Wrapper for Catch"""
        thread = threading.Thread(target=self.master.runCatch, args=())
        thread.daemon = True
        thread.name = "UI-Catch-"+thread.name
        thread.start()

    def buttonRelease(self):
        """Wrapper for Release"""
        thread = threading.Thread(target=self.master.runRelease, args=())
        thread.daemon = True
        thread.name = "UI-Release-"+thread.name
        thread.start()

    def buttonReboot(self):
        """Wrapper for Reboot"""
        self.master.reboot()

    def buttonShutdown(self):
        """Wrapper for Shutdown"""
        self.master.shutdown()

    def instance(self):
        """Return the GUI object"""
        return self

#if __name__ == "__main__":
def begin(master=None):
    """Constructor for the GUI object"""
    try:
        app = QtGui.QApplication(sys.argv)
    except:
        print("UI can not be restarted. The Cage must reboot first.")
        return False
    myapp = MyMainWindow()
    myapp.master = master
    myapp.show()
    myapp.raise_()
    myapp.activateWindow()
    myapp.showMaximized()
    sys.exit(app.exec_())