  
          
#-----------------------LMP Pricing function------------------------#                               
def LMP_Price():
    import zipfile, requests,StringIO,os,time,datetime
    from xml.dom import minidom
    from __builtin__ import file
    from datetime import datetime

    while True:
        try:
            os.system('cls')
            
            #Change here, add your directory and PNodeId
            filedirectory="C:\ADS\LMP_Pricing"
            PNodeId= "T0304_7_N003"
            
            #Delete old files from the folder
            filelist = [ f for f in os.listdir(filedirectory) if f.endswith(".xml") ]
            for f in filelist:
                os.remove(os.path.join(filedirectory, f))
                
            # Get current LMP price for Pnode        
            URL='http://oasis.caiso.com/oasisapi/SingleZip?queryname=PRC_CURR_LMP&node='+PNodeId+'&startdatetime=20130919T07:00-0000&enddatetime=20130919T07:00-0000&version=1'
            r = requests.get(URL, stream=True)
            z = zipfile.ZipFile(StringIO.StringIO(r.content))
            
            #Extract zip file received from CAISO to a folder
            z.extractall(filedirectory)
            
            #Get path of the extracted file 
            for a,d,f in os.walk(filedirectory):
                for file in f:
                    if ".xml" in file:
                        filepath = (os.path.join(a,file))
            #print filepath
            
            #Parse xml file for LMP price
            mydoc = minidom.parse(filepath)
            #print mydoc
            LMP_Price= mydoc.getElementsByTagName("VALUE")[3]
            Price=LMP_Price.firstChild.data
            starttime=mydoc.getElementsByTagName("INTERVAL_START_GMT")[3]
            Pricing_interval = starttime.firstChild.data
            Price_interval = datetime.strptime(Pricing_interval,'%Y-%m-%dT%H:%M:%S-00:00')
            #print "Price interval=",Price_interval
            systemtimeutc = datetime.utcnow()
            #print "System time=",systemtimeutc
            if systemtimeutc>Price_interval:
                newLMPPrice=Price
                Mbus(newLMPPrice, 0x034)
            print "PNode_"+PNodeId+"_Published_LMP_Price=",Price + " $/MWh"
            Mbus(Price, 0x032)
            print "PNode_"+PNodeId+"_Active_LMP_Price=",newLMPPrice+ " $/MWh"
            time.sleep(30)
            context[0x02].setValues(2,0x05,[1])
             
        except:
            print "Error in getting data"
            time.sleep(30)
            context[0x02].setValues(2,0x05,[0])  
                        
#---------Modbus Server Definition----------#            
def Mod():
    import time
    from pymodbus.server.sync import StartTcpServer   
    from pymodbus.device import ModbusDeviceIdentification
    from pymodbus.datastore import ModbusSequentialDataBlock
    from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
    identity = ModbusDeviceIdentification()
    identity.VendorName  = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl   = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName   = 'Pymodbus Server'
    identity.MajorMinorRevision = '1.0'
    #Run Modbus server using shared variable 'context'
    StartTcpServer(context, identity=identity, address=("127.0.0.1", 502))
    
    
#---------Threading and Shared Variable Definition----------#        
import threading
import time
from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

dop = 0
store = ModbusSlaveContext(
            di = ModbusSequentialDataBlock(1, [1]*100),
            co = ModbusSequentialDataBlock(0, [0]*100),
            hr = ModbusSequentialDataBlock(1, [0]*200),
            ir = ModbusSequentialDataBlock(0, [0]*100))
context = ModbusServerContext(slaves=store, single=True)
from threading import Thread
    
if __name__ == '__main__':
    Thread(target = ADS).start()
    Thread(target = ADS_Dispatch).start()
    Thread(target = Mod).start()
    Thread(target = LMP_Price).start()


