#---------Modbus Data Manipulation Function Definition---------#
def Mbus(dop,register):
    import re
    from pymodbus.constants import Endian
    from pymodbus.payload import BinaryPayloadBuilder
    modDatatemp = re.sub('u''','',dop)
    modDataFloat = float(modDatatemp)
    #Convert floating point dop to Modbus 32-bit
    builder = BinaryPayloadBuilder(endian=Endian.Little)
    builder.add_32bit_float(modDataFloat)
    payload = builder.to_registers()
    #Write to Modbus register 40001
    context[0x00].setValues(3,register,payload)
    
    
#---------Parse Function Definition---------#
def ResourceParse(resource_id, Dec_Traj):
    
    try:
        from xml.dom import minidom
        doc = minidom.parseString(Dec_Traj)
        trajectoryBatchList = doc.getElementsByTagName("trajectoryBatchList")[0]
        trajectoryBatch = trajectoryBatchList.getElementsByTagName("trajectoryBatch")
        dop = trajectoryBatchList.getElementsByTagName("dop")[0]
        #print "dop",dop.firstChild.data
        for trajectoryBatchs in trajectoryBatch:
            batchUID=trajectoryBatchs.getAttribute("batchUID")
            batchreceived=trajectoryBatchs.getElementsByTagName("batchReceived")[0]
            doplist=trajectoryBatchs.getElementsByTagName("dopList")
            #print batchUID,batchreceived.firstChild.data
            for doplists in doplist:
                trajectorydop=doplists.getElementsByTagName("trajectoryDop")
                for trajectorydops in trajectorydop:
                    resourceid=trajectorydops.getElementsByTagName("resourceId")[0]
                    dop=trajectorydops.getElementsByTagName("dop")[0]
                    targettime=trajectorydops.getElementsByTagName("targetTime")[0]
                    seqnumber=trajectorydops.getElementsByTagName("sequenceNumber")[0]
                    #print batchUID,",",resourceid.firstChild.data,",",dop.firstChild.data,",",targettime.firstChild.data,",",seqnumber.firstChild.data
                    if resourceid.firstChild.data==resource_id:
                        x=[str(dop.firstChild.data),str(resourceid.firstChild.data),str(targettime.firstChild.data)]
        return x[0]
    except:
        return -1
    
    
#---------Main ADS Query Logic Definition----------#
def ADS():
    while True:
        try:
            lastbatchUID="-1"
            lasttrajUID="-1"
            #print 'last batch UID is: ',lastbatchUID
            #print 'last Trajectory UID is: ',lasttrajUID
            
            count = 0
            while (count <2):
                
                    import urllib2, httplib,socket,base64,gzip,StringIO
                    from suds.client import Client
                    from suds.transport.http import HttpTransport
                    import xml.etree.ElementTree as ET
                    import time,os
                    from xml.dom.minidom import parseString
                    
                    os.system('cls')    
                    #print 'The count is:', count
                    
                    class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
                        def __init__(self, key, cert):
                            urllib2.HTTPSHandler.__init__(self)
                            self.key = key
                            self.cert = cert
            
                        def https_open(self, req):
                        #Rather than pass in a reference to a connection class, we pass in
                        # a reference to a function which, for all intents and purposes,
                        # will behave as a constructor
                            return self.do_open(self.getConnection, req)
            
                        def getConnection(self, host, timeout=300):
                            return httplib.HTTPSConnection(host,
                                                       key_file=self.key,
                                                       cert_file=self.cert)
            
                    class HTTPSClientCertTransport(HttpTransport):
                        def __init__(self, key, cert, *args, **kwargs):
                            HttpTransport.__init__(self, *args, **kwargs)
                            self.key = key
                            self.cert = cert
            
                        def u2open(self, u2request):
                            """
                            Open a connection.
                            @param u2request: A urllib2 request.
                            @type u2request: urllib2.Request.
                            @return: The opened file-like urllib2 object.
                            @rtype: fp
                            """
                            tm = self.options.timeout
                            url = urllib2.build_opener(HTTPSClientAuthHandler(self.key, self.cert))
                            if self.u2ver() < 2.6:
                                socket.setdefaulttimeout(tm)
                                return url.open(u2request)
                            else:
                                return url.open(u2request, timeout=tm)
            
                #These lines enable debug logging; remove them once everything works.
                #import logging
                #logging.basicConfig(level=logging.INFO)
                #logging.getLogger('suds.client').setLevel(logging.DEBUG)
                #logging.getLogger('suds.transport').setLevel(logging.DEBUG)
            
                    client = Client('https://adssta.caiso.com:447/ADS/APIWebService/v7?WSDL',location='https://adssta.caiso.com:447/ADS/APIWebService/v7',
#-------Map your .pem file here
                    transport = HTTPSClientCertTransport('C:\PCGkey.pem',
                                                         'C:\PCGkey.pem'))
                    #print client
            
            
                    #Dispatch Batch data
                    
                    LastBatchUID=client.service.getDispatchBatchesSinceUID(lastbatchUID)
                    #print lastbatchUID,'\n \n'
                    #print LastBatchUID
                    root = ET.fromstring(LastBatchUID)
                    for child in root:
                        for grandchild in child:
                            newbatchUID= grandchild.get('batchUID')
                    #print 'batchUID is:',newbatchUID
                    lastbatchUID=newbatchUID 
                    #print 'last batch UID is: ',lastbatchUID    
                    DispatchBatch1= client.service.getDispatchBatch(lastbatchUID)
                    decode = base64.b64decode(DispatchBatch1)
                    stringread = StringIO.StringIO(decode)
                    decompress = gzip.GzipFile(fileobj=stringread)
                    DecodedDispatch = decompress.read()
                    #print DecodedDispatch
#-------Saves Dispatch Response to file - change path if needed.
                    with open("C:\\DispatchBatchResponse.xml", "w") as text_file:
                                text_file.write(format(DecodedDispatch))
                    #Trajectory data
                    #print 'lasttrajUID is:',lasttrajUID
                    IsNewTraj=client.service.isNewTrajData(lasttrajUID)
                    #print IsNewTraj
                    IsNewTraj=False
                    if count==0:
                        IsNewTraj = False
                        print 'First Loop'
                        count = count + 1
                        Trajectory= client.service.getTrajectoryData(lasttrajUID)
                        decode_1 = base64.b64decode(Trajectory)
                        stringread_1 = StringIO.StringIO(decode_1)
                        decompress_1 = gzip.GzipFile(fileobj=stringread_1)
                        DecodedTrajectory = decompress_1.read()
#--------Can create multiples of this section if you would like to check multiple sites
#--------
#--------Replace "" with Resource ID that you would like to poll
                        dopMod = ResourceParse("", DecodedTrajectory)
                        print "DOP is: ", dopMod
#-------Writes 32-bit floating point value for DOP to Modbus register 40001 (0x00)
                        Mbus(dopMod, 0x00)
                        root1 = ET.fromstring(DecodedTrajectory)
                        #Convert dop string to floating point
                        #print root1.tag,root1.attrib
                        for child1 in root1:
                            #print child1.tag,child1.attrib
                                for grandchild1 in child1:
                                    newTrajUID=grandchild1.get("batchUID")
                        lasttrajUID=newTrajUID
                        #print lasttrajUID
                        context[0x00].setValues(2,0x00,[1])    
                    elif IsNewTraj==False:
                        print 'Infinite loop', lasttrajUID
                        Trajectory= client.service.getTrajectoryData(lasttrajUID)
                        decode_1 = base64.b64decode(Trajectory)
                        stringread_1 = StringIO.StringIO(decode_1)
                        decompress_1 = gzip.GzipFile(fileobj=stringread_1)
                        DecodedTrajectory = decompress_1.read()
#--------Replace "" with Resource ID that you would like to poll                        
                        dopMod = ResourceParse("", DecodedTrajectory)
#--------If no new values, retain old values in Modbus                        
                        if(dopMod==-1):
                            print 'no new values'
                        else:
                            Mbus(dopMod, 0x00)
                            print "DOP is: ", dopMod
                        root1 = ET.fromstring(DecodedTrajectory)
                        for child1 in root1:
                            #print child1.tag,child1.attrib
                            for grandchild1 in child1:
                                newTrajUID=grandchild1.get("batchUID")
                            lasttrajUID=newTrajUID
                            #print 'last Trajectory UID is: ',lasttrajUID
                    time.sleep(10)
#--------Modbus register 10001 set to '1' for good data                    
                    context[0x00].setValues(2,0x00,[1])
        except:
            print "error"
#--------Modbus register 10001 set to '0' for bad data            
            context[0x00].setValues(2,0x00,[0])
            
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
    
#--------Set your Server IP Address here
    StartTcpServer(context, identity=identity, address=("192.168.57.77", 502))
    
    
#---------Threading and Shared Variable Definition----------#        
import threading
import time
from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

#--------Initialize Modbus Values Here, change if desired
store = ModbusSlaveContext(
            di = ModbusSequentialDataBlock(1, [1]*100),
            co = ModbusSequentialDataBlock(0, [0]*100),
            hr = ModbusSequentialDataBlock(1, [0]*10),
            ir = ModbusSequentialDataBlock(0, [0]*100))
context = ModbusServerContext(slaves=store, single=True)

from threading import Thread
    
if __name__ == '__main__':
    Thread(target = ADS).start()
    Thread(target = Mod).start()