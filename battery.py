#Communicates with and streams data from the Battery Charger over Serial/USB
#Author: Mehmet Akbulut and Zoe Dickert
#MIT License
#Hex Values are from Boston University Robotics Lab

import serial
import threading
import time

#Name of the charger device
DeviceName = "USB"

#Instruction set to command the battery charger over serial
Instruction = {
"Select01":     "\x0C\x30\x30\x30\x41\x30\x43\x30\x30\x30\x31\x30\x32\x30\x35\x0D",
"Select01R":    "\x0C\x30\x30\x30\x41\x38\x31\x30\x30\x30\x31\x30\x31\x46\x42\x0D",
"Select02":     "\x0C\x30\x30\x30\x41\x30\x43\x30\x30\x30\x32\x30\x32\x30\x36\x0D",
"Select02R":    "\x0C\x30\x30\x30\x41\x38\x31\x30\x30\x30\x32\x30\x31\x46\x43\x0D",
"Select03":     "\x0C\x30\x30\x30\x41\x30\x43\x30\x30\x30\x33\x30\x32\x30\x37\x0D",
"Select03R":    "\x0C\x30\x30\x30\x41\x38\x31\x30\x30\x30\x33\x30\x31\x46\x44\x0D",
"Select04":     "\x0C\x30\x30\x30\x41\x30\x43\x30\x30\x30\x34\x30\x32\x30\x38\x0D",
"Select04R":    "\x0C\x30\x30\x30\x41\x38\x31\x30\x30\x30\x34\x30\x31\x46\x45\x0D",
"ChargeSolo01": "\x0C\x30\x30\x30\x45\x30\x35\x30\x30\x30\x31\x30\x30\x30\x33\x30\x32\x42\x45\x0D",
"ChargeSolo02": "\x0C\x30\x30\x30\x45\x30\x35\x30\x30\x30\x32\x30\x30\x30\x33\x30\x32\x42\x46\x0D",
"ChargeSolo03": "\x0C\x30\x30\x30\x45\x30\x35\x30\x30\x30\x33\x30\x30\x30\x33\x30\x32\x43\x30\x0D",
"ChargeSolo04": "\x0C\x30\x30\x30\x45\x30\x35\x30\x30\x30\x34\x30\x30\x30\x33\x30\x32\x43\x31\x0D",
"ChargeQuick01":"\x0C\x30\x30\x30\x45\x30\x35\x30\x30\x30\x31\x30\x30\x30\x36\x30\x32\x43\x31\x0D",
"ChargeQuick02":"\x0C\x30\x30\x30\x45\x30\x35\x30\x30\x30\x32\x30\x30\x30\x36\x30\x32\x43\x32\x0D",
"ChargeQuick03":"\x0C\x30\x30\x30\x45\x30\x35\x30\x30\x30\x33\x30\x30\x30\x36\x30\x32\x43\x33\x0D",
"ChargeQuick04":"\x0C\x30\x30\x30\x45\x30\x35\x30\x30\x30\x34\x30\x30\x30\x36\x30\x32\x43\x34\x0D",
"Discharge01":  "\x0C\x30\x30\x30\x45\x30\x36\x30\x30\x30\x31\x30\x30\x30\x33\x30\x32\x42\x46\x0D",
"Discharge02":  "\x0C\x30\x30\x30\x45\x30\x36\x30\x30\x30\x32\x30\x30\x30\x33\x30\x32\x43\x30\x0D",
"Discharge03":  "\x0C\x30\x30\x30\x45\x30\x36\x30\x30\x30\x33\x30\x30\x30\x33\x30\x32\x43\x31\x0D",
"Discharge04":  "\x0C\x30\x30\x30\x45\x30\x36\x30\x30\x30\x34\x30\x30\x30\x33\x30\x32\x43\x32\x0D",
"Balance01":    "\x0C\x30\x30\x30\x45\x31\x31\x30\x30\x30\x31\x30\x30\x30\x33\x30\x32\x42\x42\x0D",
"Balance02":    "\x0C\x30\x30\x30\x45\x31\x31\x30\x30\x30\x32\x30\x30\x30\x33\x30\x32\x42\x43\x0D",
"Balance03":    "\x0C\x30\x30\x30\x45\x31\x31\x30\x30\x30\x33\x30\x30\x30\x33\x30\x32\x42\x44\x0D",
"Balance04":    "\x0C\x30\x30\x30\x45\x31\x31\x30\x30\x30\x34\x30\x30\x30\x33\x30\x32\x42\x45\x0D",
"Store01":      "\x0C\x30\x30\x30\x45\x30\x37\x30\x30\x30\x31\x30\x30\x30\x33\x30\x32\x43\x30\x0D",
"Store02":      "\x0C\x30\x30\x30\x45\x30\x37\x30\x30\x30\x32\x30\x30\x30\x33\x30\x32\x43\x31\x0D",
"Store03":      "\x0C\x30\x30\x30\x45\x30\x37\x30\x30\x30\x33\x30\x30\x30\x33\x30\x32\x43\x32\x0D",
"Store04":      "\x0C\x30\x30\x30\x45\x30\x37\x30\x30\x30\x34\x30\x30\x30\x33\x30\x32\x43\x33\x0D",
"Stop":         "\x0C\x30\x30\x30\x41\x30\x39\x30\x30\x30\x30\x30\x31\x46\x41\x0D",
"ReadStatus":   "\x0C\x30\x30\x30\x41\x38\x41\x30\x30\x30\x30\x30\x32\x30\x41\x0D",
"Confirmcellnum":"\x0C\x30\x30\x30\x41\x30\x45\x30\x30\x30\x30\x30\x32\x30\x36\x0D"
    }

class charger(object):
    """Charger Unit"""
    def __init__(self):
        """Create new thread"""
        self.thread = threading.Thread(target=self.initialize, args=())
        self.thread.daemon=True
        self.thread.name = "Charger-"+self.thread.name
        self.thread.start()

    def initialize(self):
        """Initialize the charger"""
        self.Alive=True
        self.COM=None
        self.RATE=9600
        self.DEV=None
        self.TIMEOUT=1
        self.status="Booting"
        
        self.ser = serial.Serial()
        self.DEV = self.findDevice()
        
        #if(self.DEV==None):
        #    print("Charger not found, exiting process.")
        #    exit()
        self.ser.port = self.COM
        self.ser.baudrate = self.RATE
        self.ser.timeout = self.TIMEOUT

        #Open Serial Port
        self.ser.open()

        self.receivedData=""

        self.docking=0
        self.elapsed=0
        self.voltage=0
        self.current=0
        self.cell1=0
        self.cell2=0
        self.cell3=0
        self.percentage=0
        self.resistance=0
        
        self.StreamData=True
        self.status="Enabled"

        self.loop()

    def loop(self):
        """Continous operation as long as the battery thread is alive"""
        while self.Alive:
            #Try to communicate with charger
            try:
                #Stream data if told to do so
                if self.StreamData==True:
                    time.sleep(1)
                    [self.docking,self.elapsed,self.voltage,self.current,self.cell1,self.cell2,self.cell3,self.percentage,self.resistance]=self.chargingstatus()
                    #self.die()
            #If it fails, wait a little bit
            except:
                time.sleep(0.1)

    def report(self):
        """Report charging variables"""
        print("Charger Report\n"
+"Status: "+str(self.status)+"\n"
+"Elapsed:"+str(self.elapsed)+"\n"
+"Voltage: "+str(self.voltage)+"\n"
+"Current: "+str(self.current)+"\n"
+"Cells: "+str(self.cell1)+" | "+str(self.cell2)+" | "+str(self.cell3)+"\n"
+"Percentage: "+str(self.percentage)+"\n"
+"Resistance: "+str(self.resistance)+"\n")

    def findDevice(self):
        """Find serial interface for a charger connected to the USB ports"""
        ports = self.getPorts()
        for p in ports:
            for i in p:
                if i[:len(DeviceName)] == DeviceName:
                    self.COM = p[0]
                    self.DEV = p
                    return self.DEV
        return None

    def getPorts(self):
        '''Acquire the list of devices connected through the USB ports'''
        import serial.tools.list_ports
        return list(serial.tools.list_ports.comports())

    def die(self):
        '''Kill the thread when needed'''
        self.Alive=False
        self.ser.close()
        #break
        
    def chargingstatus(self):
        #Returns 0 if not docked (No Vehicle on pads)
        #1 if docked and OK
        #2 if docked and error
        data = self.mainData()
        bat_voltage = data[12]      #battery Voltage
        cell1_voltage = data[19]    #Cell 1 Voltage
        cell2_voltage = data[20]    #Cell 2 Voltage
        cell3_voltage = data[21]    #Cell 3 Voltage

        elapsedtime = data[11]
        current = data[13]
        chargelevel = data[33]
        resistance = data[34]
        
        #Check the battery voltages to see if the battery is healthy
        docking = 0
        if cell1_voltage+cell2_voltage+cell3_voltage <= bat_voltage+0.4 and cell1_voltage+cell2_voltage+cell3_voltage >= bat_voltage-0.4 :
            docking = 1
        if bat_voltage == 0:
            docking = 2
        return [docking,elapsedtime,bat_voltage,current,cell1_voltage,cell2_voltage,cell3_voltage,chargelevel,resistance]

    def sendCommand_return(self, command):
        '''Command the battery charger and expect a message in response'''
        ###txdata_dec = int(command)                #MATLAB relic for reference
        ####Write using the UINT8 data format       #MATLAB relic for reference
        self.write(command)

        #read back data in ASCII format 
        rxdata = self.read()

        #remove non-hex characters
        hexvalues = ["0","1","2","3","4","5","6","7","8","9", "A", "B", "C", "D", "E", "F"]
        rxdata = self.ismember(rxdata, hexvalues)
        return rxdata

    def sendCommand(self, command):
        '''Command the battery charger and carry on'''
        ###txdata_dec = int(command)                #MATLAB relic
        ####Write using the UINT8 data format       #MATLAB relic
        self.write(command)
        #return rxdata
        
    def ismember(self,A,B):
        #Takes 2 lists, A and B, checks if each element in A is found anywhere in element B.
        #Creates an array(boolarray) of 1 (True) and 0 (False) values if the elements in A are found in B (True) or are not found in B (False) 
        boolarray= list()
        for i in range(len(A)):
            if A[i] in B:
                pass
            else:
                A = A[:i] + "~" + A[i+1:]
        A=A.replace("~","")
        return A
    
    def mainData(self):
        #input: Self=Charger Device
        #output: a column of the data monitor with processed values

        #Wait until correct data has been received
        while True:
            rxdata = self.sendCommand_return(Instruction["ReadStatus"])
            if rxdata and int(rxdata[:4],16) == 278:
                break

        #Store received data
        self.receivedData = rxdata

        #Parse through the received data
        temp_data = list()
        temp_data.append(int(rxdata[:4],16))     #0, Packet Length
        temp_data.append(int(rxdata[4:6],16))     #1, Command Num
        temp_data.append(int(rxdata[6:10],16))     #2, wRes
        temp_data.append(int(rxdata[10:14],16)/10)   #3, Firmware
        temp_data.append(int(rxdata[14:18],16))   #4, Model
        temp_data.append(int(rxdata[18:22],16))   #5, Res2
        temp_data.append(float(int(rxdata[22:26],16))/1000)   #6, Supply Voltage (Input to the charger)
        temp_data.append(int(rxdata[26:30],16))   #7, res3
        temp_data.append(int(rxdata[30:34],16))   #8, CC = eChargeControl (3=discharge, 5=complete, 1=charge, 7=balance, 8=store)9]
        temp_data.append(int(rxdata[34:38],16))   #9, Status = 1 (dec) (status detail of CC)
        temp_data.append(int(rxdata[38:42],16))   #10, Cycle = 1 (dec)
        temp_data.append(int(rxdata[42:46],16))   #11, Seconds (from beginning till end of a process)
        temp_data.append(float(int(rxdata[46:50],16))/1000)      #12, battery volts ex. 12019 (dec) = 12.019 Volts
        temp_data.append(float(int(rxdata[50:54],16)))   #13, Current
        temp_data.append(int(rxdata[54:58],16))   #14, Cap = 57 (dec) (cycle charge capacity in mAh)
        temp_data.append(int(rxdata[58:62],16))   #15, Unkwn
        temp_data.append(int(rxdata[62:66],16))   #16, Peak time ?
        temp_data.append(int(rxdata[66:70],16))   #17, Probe detect ?
        temp_data.append(int(rxdata[70:74],16))   #18, Temperature select F/C ?
        temp_data.append(float(int(rxdata[74:78],16))/1000)      #19, c1v = 4011 (DEC) = 4.011v
        temp_data.append(float(int(rxdata[78:82],16))/1000)      #20, c2v = 4013 (DEC)
        temp_data.append(float(int(rxdata[82:86],16))/1000)      #21, c3v
        temp_data.append(float(int(rxdata[86:90],16))/1000)      #22, c4v
        temp_data.append(float(int(rxdata[90:94],16))/1000)      #23, c5v
        temp_data.append(float(int(rxdata[94:98],16))/1000)      #24, c6v
        temp_data.append(float(int(rxdata[98:102],16))/1000)      #25, c7v
        temp_data.append(float(int(rxdata[102:106],16))/10)      #26, c1Ir = 30 (DEC) = 3.0 mOhm (OK)
        temp_data.append(float(int(rxdata[106:110],16))/10)      #27, c2Ir = 32 (DEC) = 3.2 mOhm (OK)
        temp_data.append(float(int(rxdata[110:114],16))/10)      #28, c3Ir = 53 (DEC) = 5.3 mOhm (OK)
        temp_data.append(float(int(rxdata[114:118],16))/10)      #29, c4Ir = 0
        temp_data.append(float(int(rxdata[118:122],16))/10)      #30, c5Ir = 0
        temp_data.append(float(int(rxdata[122:126],16))/10)      #31, c6Ir = 0
        temp_data.append(float(int(rxdata[126:130],16))/10)      #32, c7Ir = 0
        temp_data.append(int(rxdata[130:134],16))      #33, Charge level = 79 (dec) = 79%
        temp_data.append(int(rxdata[134:138],16)/10)      #34, Internal Resistance in mOhm
        temp_data.append(int(rxdata[138:142],16))      #35, Temperature ?
        temp_data.append(int(rxdata[142:146],16))      #36, Peak Temp ?
        temp_data.append(float(int(rxdata[146:150],16))/1000)      #37, Peak Volts ?
        temp_data.append(int(rxdata[150:],16))      #38, The rest of the 32 16-bit entries are probably a second channel.
        return temp_data

    def read(self):
        #Read message from charger
        return self.ser.readline()

    def write(self,x):
        #Send message to charger
        try:
            self.ser.write(x)
            return True
        except:
            return False
    
    def memoryData(self,memory_num):
        #input: serial port object | commands struct
        #output: Current memory data, see below for cells explaination

        #Wait until proper data has been received
        rxdata=None
        while True:
            if rxdata and int(rxdata[:4],16) == 78:
                break
            elif memory_num == 1:
                #print("1")
                rxdata = self.sendCommand_return(Instruction["Select01R"])
            elif memory_num == 2:
                rxdata = self.sendCommand_return(Instruction["Select02R"])
            elif memory_num == 3:
                rxdata = self.sendCommand_return(Instruction["Select03R"])
            elif memory_num == 4:
                rxdata = self.sendCommand_return(Instruction["Select04R"])

        #Parse received message
        memory_data = list()
        memory_data.append(int(rxdata[:4],16))     #0, Packet Length
        memory_data.append(int(rxdata[4:6],16) )    #1, Command Num
        memory_data.append(int(rxdata[6:10],16)  )   #2, Memory Number
        memory_data.append(int(rxdata[10:14],16) )  #3, Battery Typer (ex. 3 is LiPo)
        memory_data.append(int(rxdata[14:18],16)  ) #4, Number of Cells
        memory_data.append(int(rxdata[18:22],16)*10)   #5, Battery Capacity: 800 mAh
        memory_data.append(int(rxdata[22:26],16))   #6, Charge mAmps
        memory_data.append(int(rxdata[26:30],16))   #7, Discharge mAmps
        memory_data.append(int(rxdata[30:34],16)/1000)   #8, discharge volts: 3.8 volt/cell
        memory_data.append(int(rxdata[34:38],16))   #9, Peak sens mV/C (useless)
        memory_data.append(int(rxdata[38:42],16))   #10, (Cutoff temp)
        memory_data.append(int(rxdata[42:46],16))   #11, TCS Capacity %
        memory_data.append(int(rxdata[46:50],16))   #12, safety timer: 300 min
        memory_data.append(int(rxdata[50:54],16))   #13, 0
        memory_data.append(int(rxdata[54:58],16))   #14, 0
        memory_data.append(int(rxdata[58:62],16))   #15, 0
        memory_data.append(int(rxdata[62:66],16))   #16, 1000
        memory_data.append(int(rxdata[66:70],16))   #17, 0
        memory_data.append(int(rxdata[70:74],16))   #18, 0
        memory_data.append(int(rxdata[74:78],16))   #19, 60 (set store: 60%)
        memory_data.append(int(rxdata[78:],16))   #20, Checksum
        return memory_data

    def charge(self):
        '''Automated charge process'''
        self.StreamData=False
        self.status="Initiating Charge"
        #Try selecting Memory Setting 01
        try:
            self.status="Selecting Memory 01"
            self.sendCommand(Instruction["Select01"])
            #print(resp)
        except:
            print("Battery Charger failed to Select Memory 01 during Charge Command")
            pass
        time.sleep(0.25)
        #Try solo charging with Memory Setting 01
        try:
            self.status="Starting Solo Charge"
            self.sendCommand(Instruction["ChargeSolo01"])
            #print(resp)
        except:
            print("Battery Charger failed to Solo Charge 01 during Charge Command")
            pass
        time.sleep(0.25)
        #Try confirm the number of cells prompt manually instead of waiting for it to confirm itself
        try:
            self.status="Confirming Number of Cells"
            self.sendCommand(Instruction["Confirmcellnum"])
            #print(resp)
        except:
            print("Battery Charger failed to Confirm Cell Number during Charge Command")
            try:
                print("Battery Charger is retrying to Confirm Cell Number")
                time.sleep(1)
                self.sendCommand(Instruction["Confirmcellnum"])
            except:
                print("Battery Charger failed to Confirm Cell Number")
            pass
        time.sleep(0.25)
        #Try checking if the charging is underway
        try:
            self.status="Verifying"
            resp=self.mainData()
        except:
            try:
                resp=self.mainData()
            except:
                pass
        #Confirm whether charging failed or not    
        try:
            if resp[8]==6 and resp[9]==1:
                self.stop()
                self.status="Failed Charging"
                print("Battery Charger failed to start charging. Possibly no battery connected.")
                return False
        except:
            pass
        self.status="Charge"
        self.StreamData=True
        return True

    def stop(self):
        '''Send the stop command to the charger'''
        self.StreamData=False
        try:
            resp=self.sendCommand_return(Instruction["Stop"])
            print(resp)
        except:
            try:
                resp=self.sendCommand_return(Instruction["Stop"])
                print(resp)
            except:
                pass
        self.status="Enabled"
        self.StreamData=True
        return True

    
    

        
    
            
    
        
        











    
