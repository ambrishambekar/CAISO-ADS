'''
Created on Apr 24, 2018

@author: Ambrish.Ambekar
'''
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
    
def DispatchParse(resource_id, Dec_Disp):
    from xml.dom import minidom
    try:
        doc = minidom.parseString(Dec_Disp)
        DispatchBatch = doc.getElementsByTagName("DispatchBatch")
        for dispatchbatches in DispatchBatch:
            instructionsss=dispatchbatches.getElementsByTagName("instructions")
            #print instructionsss
            for instructionss in instructionsss:
                instructions=instructionss.getElementsByTagName("instruction")
                #print instructions
                for instruction in instructions:
                    resourceIDs=instruction.getElementsByTagName("resourceId")[0]
                    #print resourceIDs.firstChild.data
                    a=resourceIDs.firstChild.data
                    if a==resource_id:
                        detail=instruction.getElementsByTagName("detail")
                        #print detail
                        for details in detail:
                            instructiondetail=details.getElementsByTagName("instructionDetail")
                            for instructiondetails in instructiondetail:
                                servicetype=instructiondetails.getElementsByTagName("serviceType")[0]
                                #print servicetype.firstChild.data
                                if servicetype.firstChild.data=="SUPP":
                                    MW=instructiondetails.getElementsByTagName("mw")[0]
                                    return MW.firstChild.data
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
                    transport = HTTPSClientCertTransport('C:\Con_Ed_ADS\PCGkey.pem',
                                                         'C:\Con_Ed_ADS\PCGkey.pem'))
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
                    #with open("C:\\Con_Ed_ADS\\DispatchBatchResponse.xml", "w") as text_file:
                                #text_file.write(format(DecodedDispatch))
                    
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
                        
                        with open("C:\\Con_Ed_ADS\\TrajectoryResponse.xml", "w") as text_file:
                            text_file.write(format(DecodedTrajectory))
                        dopFresh = ResourceParse("FRESHW_1_SOLAR1", DecodedTrajectory)
                        dopOro1 = ResourceParse("OROLOM_1_SOLAR1", DecodedTrajectory)
                        dopOro2 = ResourceParse("OROLOM_1_SOLAR2", DecodedTrajectory)
                        dopAve1 = ResourceParse("AVENAL_6_AVSLR1", DecodedTrajectory)
                        dopAve2 = ResourceParse("AVENAL_6_AVSLR2", DecodedTrajectory)
                        dopAlp1 = ResourceParse("ALPSLR_1_NTHSLR", DecodedTrajectory)
                        dopAlp2 = ResourceParse("ALPSLR_1_SPSSLR", DecodedTrajectory)
                        
                        print "Freshwater DOP is: ", dopFresh
                        print "Oro Loma 1 DOP is: ", dopOro1
                        print "Oro Loma 2 DOP is: ", dopOro2
                        print "Avenal 1 DOP is: ", dopAve1
                        print "Avenal 2 DOP is: ", dopAve2
                        print "Alpough 1 DOP is", dopAlp1
                        print "Alpough 2 DOP is", dopAlp2
                        
                        Mbus(dopFresh, 0x00)
                        Mbus(dopOro1, 0x02)
                        Mbus(dopOro2, 0x04)
                        Mbus(dopAve1, 0x06)
                        Mbus(dopAve2, 0x08)
                        Mbus(dopAlp1, 0x0A)
                        Mbus(dopAlp2, 0x0C)
  
                        #with open("C:\\Con_Ed_ADS\\OutputResponse\\dop.csv", "w") as text_file:
                            #text_file.write(format(dop))
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
                        #print DecodedTrajectory
                        with open("C:\\Con_Ed_ADS\\TrajectoryResponse.xml", "w") as text_file:
                            text_file.write(format(DecodedTrajectory))
                        dopFresh = ResourceParse("FRESHW_1_SOLAR1", DecodedTrajectory)
                        dopOro1 = ResourceParse("OROLOM_1_SOLAR1", DecodedTrajectory)
                        dopOro2 = ResourceParse("OROLOM_1_SOLAR2", DecodedTrajectory)
                        dopAve1 = ResourceParse("AVENAL_6_AVSLR1", DecodedTrajectory)
                        dopAve2 = ResourceParse("AVENAL_6_AVSLR2", DecodedTrajectory)
                        dopAlp1 = ResourceParse("ALPSLR_1_NTHSLR", DecodedTrajectory)
                        dopAlp2 = ResourceParse("ALPSLR_1_SPSSLR", DecodedTrajectory)
                        
                        if(dopFresh==-1):
                            print 'no new values'
                        else:
                            Mbus(dopFresh, 0x00)
                            Mbus(dopOro1, 0x02)
                            Mbus(dopOro2, 0x04)
                            Mbus(dopAve1, 0x06)
                            Mbus(dopAve2, 0x08)
                            Mbus(dopAlp1, 0x0A)
                            Mbus(dopAlp2, 0x0C)
                            
                            print "Freshwater DOP is: ", dopFresh
                            print "Oro Loma 1 DOP is: ", dopOro1
                            print "Oro Loma 2 DOP is: ", dopOro2
                            print "Avenal 1 DOP is: ", dopAve1
                            print "Avenal 2 DOP is: ", dopAve2
                            print "Alpough 1 DOP is", dopAlp1
                            print "Alpough 2 DOP is", dopAlp2
                        #with open("C:\\Con_Ed_ADS\\OutputResponse\\dop.csv", "w") as text_file:
                            #text_file.write(format(dop))
                        root1 = ET.fromstring(DecodedTrajectory)
                        for child1 in root1:
                            #print child1.tag,child1.attrib
                            for grandchild1 in child1:
                                newTrajUID=grandchild1.get("batchUID")
                            lasttrajUID=newTrajUID
                            #print 'last Trajectory UID is: ',lasttrajUID
                    time.sleep(10)
                    context[0x00].setValues(2,0x00,[1])
                    Trajtime= os.path.getmtime('C:\Con_Ed_ADS\TrajectoryResponse.xml')
                    Systime=time.time()
                    Timediff=Systime-Trajtime
                    #print Trajtime,Systime,Timediff
                    context[0x00].setValues(2,0x02,[1])
                    if(Timediff>420):
                        lasttrajUID="-1"
                        #print DecodedTrajectory
                        context[0x00].setValues(2,0x02,[0])     
        except:
            print "error"            
            context[0x00].setValues(2,0x00,[0])
 
def ADS_Dispatch():
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
                    transport = HTTPSClientCertTransport('C:\Con_Ed_ADS\PCGkey.pem',
                                                         'C:\Con_Ed_ADS\PCGkey.pem'))
                    #print client
            
            
                    #Dispatch Batch data
                    
                    LastBatchUIDString=client.service.getDispatchBatchesSinceUID(lastbatchUID)
                    #with open("C:\\Con_Ed_ADS\\LastBatchString.xml", "w") as text_file:
                                #text_file.write(format(LastBatchUIDString))
                    #print lastbatchUID,'\n \n'
                    #print LastBatchUIDString
                    from xml.dom import minidom
                    doc = minidom.parseString(LastBatchUIDString)
                    DispatchResponse = doc.getElementsByTagName("APIDispatchResponse")[0]
                    Test=DispatchResponse.getAttribute("xmlns")
                    dispatchbatchlist=doc.getElementsByTagName("dispatchBatchList")
                    #print dispatchbatchlist
                    for dispatchbatchlists in dispatchbatchlist:
                        dispatchbatch=dispatchbatchlists.getElementsByTagName("DispatchBatch")
                        for dispatchbatches in dispatchbatch:
                            dispatchBatchType=dispatchbatches.getElementsByTagName("batchType")[0]
                            if(dispatchBatchType.firstChild.data == '0'):
                                newbatchUID=dispatchbatches.getAttribute("batchUID")
                    lastbatchUID=newbatchUID 
                    #print 'last batch UID is: ',lastbatchUID    
                    DispatchBatch1= client.service.getDispatchBatch(lastbatchUID)
                    decode = base64.b64decode(DispatchBatch1)
                    stringread = StringIO.StringIO(decode)
                    decompress = gzip.GzipFile(fileobj=stringread)
                    DecodedDispatch = decompress.read()
                    #print DecodedDispatch
                    with open("C:\\Con_Ed_ADS\\DispatchBatchResponse.xml", "w") as text_file:
                                text_file.write(format(DecodedDispatch))
                    #Trajectory data
                    #print 'lasttrajUID is:',lasttrajUID
                    IsNewBatch=client.service.isNewTrajData(lastbatchUID)
                    #print IsNewTraj
                    IsNewBatch=False
                    if count==0:
                        IsNewBatch = False
                        print 'First Loop'
                        count = count + 1
                        
                        DispatchBatch1= client.service.getDispatchBatch(lastbatchUID)
                        decode = base64.b64decode(DispatchBatch1)
                        stringread = StringIO.StringIO(decode)
                        decompress = gzip.GzipFile(fileobj=stringread)
                        DecodedDispatch = decompress.read()
                        
                        suppFresh = DispatchParse("FRESHW_1_SOLAR1", DecodedDispatch)
                        suppOro1 = DispatchParse("OROLOM_1_SOLAR1", DecodedDispatch)
                        suppOro2 = DispatchParse("OROLOM_1_SOLAR2", DecodedDispatch)
                        suppAve1 = DispatchParse("AVENAL_6_AVSLR1", DecodedDispatch)
                        suppAve2 = DispatchParse("AVENAL_6_AVSLR2", DecodedDispatch)
                        suppAlp1 = DispatchParse("ALPSLR_1_NTHSLR", DecodedDispatch)
                        suppAlp2 = DispatchParse("ALPSLR_1_SPSSLR", DecodedDispatch)
                        
                        print "Freshwater SUPP is: ", suppFresh
                        print "Oro Loma 1 SUPP is: ", suppOro1
                        print "Oro Loma 2 SUPP is: ", suppOro2
                        print "Avenal 1 SUPP is: ", suppAve1
                        print "Avenal 2 SUPP is: ", suppAve2
                        print "Alpough 1 SUPP is:", suppAlp1
                        print "Alpough 2 SUPP is:", suppAlp2
                        
                        Mbus(suppFresh, 0x14)
                        Mbus(suppOro1, 0x16)
                        Mbus(suppOro2, 0x18)
                        Mbus(suppAve1, 0x1A)
                        Mbus(suppAve2, 0x1C)
                        Mbus(suppAlp1, 0x1E)
                        Mbus(suppAlp2, 0x21)
                        
                        lastSuppFresh = suppFresh
                        lastSuppOro1 = suppOro1
                        lastSuppOro2 = suppOro2
                        lastSuppAve1 = suppAve1
                        lastSuppAve2 = suppAve2
                        lastSuppAlp1 = suppAlp1
                        lastSuppAlp2 = suppAlp2
                        #with open("C:\\Con_Ed_ADS\\OutputResponse\\dop.csv", "w") as text_file:
                            #text_file.write(format(dop))
                        LastBatchUIDString=client.service.getDispatchBatchesSinceUID(lastbatchUID)
                        #print lastbatchUID,'\n \n'
                        #print LastBatchUIDString
                        from xml.dom import minidom
                        doc = minidom.parseString(LastBatchUIDString)
                        DispatchResponse = doc.getElementsByTagName("APIDispatchResponse")[0]
                        Test=DispatchResponse.getAttribute("xmlns")
                        dispatchbatchlist=doc.getElementsByTagName("dispatchBatchList")
                        #print dispatchbatchlist
                        for dispatchbatchlists in dispatchbatchlist:
                            dispatchbatch=dispatchbatchlists.getElementsByTagName("DispatchBatch")
                            for dispatchbatches in dispatchbatch:
                                dispatchBatchType=dispatchbatches.getElementsByTagName("batchType")[0]
                                if(dispatchBatchType.firstChild.data == '0'):
                                    newbatchUID=dispatchbatches.getAttribute("batchUID")
                        lastbatchUID=newbatchUID 
                        #print lasttrajUID
                        #context[0x00].setValues(2,0x00,[1])    
                    elif IsNewBatch==False:
                        print 'Infinite loop', lastbatchUID
                        DispatchBatch1= client.service.getDispatchBatch(lastbatchUID)
                        decode = base64.b64decode(DispatchBatch1)
                        stringread = StringIO.StringIO(decode)
                        decompress = gzip.GzipFile(fileobj=stringread)
                        DecodedDispatch = decompress.read()
                        #print DecodedTrajectory
                        #with open("C:\\Con_Ed_ADS\\DispatchBatchResponse.xml", "w") as text_file:
                            #text_file.write(format(DecodedDispatch))
                        suppFresh = DispatchParse("FRESHW_1_SOLAR1", DecodedDispatch)
                        suppOro1 = DispatchParse("OROLOM_1_SOLAR1", DecodedDispatch)
                        suppOro2 = DispatchParse("OROLOM_1_SOLAR2", DecodedDispatch)
                        suppAve1 = DispatchParse("AVENAL_6_AVSLR1", DecodedDispatch)
                        suppAve2 = DispatchParse("AVENAL_6_AVSLR2", DecodedDispatch)
                        suppAlp1 = DispatchParse("ALPSLR_1_NTHSLR", DecodedDispatch)
                        suppAlp2 = DispatchParse("ALPSLR_1_SPSSLR", DecodedDispatch)
                        if (suppFresh==lastSuppFresh and lastSuppOro1 == suppOro1 and lastSuppOro2 == suppOro2 and lastSuppAve1 == suppAve1 and lastSuppAve2 == suppAve2 and lastSuppAlp1 == suppAlp1 and lastSuppAlp2 == suppAlp2):
                            print 'no new SUPP values'
                        else:
                            print "Freshwater SUPP is: ", suppFresh
                            print "Oro Loma 1 SUPP is: ", suppOro1
                            print "Oro Loma 2 SUPP is: ", suppOro2
                            print "Avenal 1 SUPP is: ", suppAve1
                            print "Avenal 2 SUPP is: ", suppAve2
                            print "Alpough 1 SUPP is:", suppAlp1
                            print "Alpough 2 SUPP is:", suppAlp2
                            
                            Mbus(suppFresh, 0x14)
                            Mbus(suppOro1, 0x16)
                            Mbus(suppOro2, 0x18)
                            Mbus(suppAve1, 0x1A)
                            Mbus(suppAve2, 0x1C)
                            Mbus(suppAlp1, 0x1E)
                            Mbus(suppAlp2, 0x21)
                            
                            lastSuppFresh = suppFresh
                            lastSuppOro1 = suppOro1
                            lastSuppOro2 = suppOro2
                            lastSuppAve1 = suppAve1
                            lastSuppAve2 = suppAve2
                            lastSuppAlp1 = suppAlp1
                            lastSuppAlp2 = suppAlp2
                                                   
                        #with open("C:\\Con_Ed_ADS\\OutputResponse\\dop.csv", "w") as text_file:
                            #text_file.write(format(dop))
                        LastBatchUIDString=client.service.getDispatchBatchesSinceUID(lastbatchUID)
                        #print lastbatchUID,'\n \n'
                        #print LastBatchUIDString
                        from xml.dom import minidom
                        doc = minidom.parseString(LastBatchUIDString)
                        DispatchResponse = doc.getElementsByTagName("APIDispatchResponse")[0]
                        Test=DispatchResponse.getAttribute("xmlns")
                        dispatchbatchlist=doc.getElementsByTagName("dispatchBatchList")
                        #print dispatchbatchlist
                        for dispatchbatchlists in dispatchbatchlist:
                            dispatchbatch=dispatchbatchlists.getElementsByTagName("DispatchBatch")
                            for dispatchbatches in dispatchbatch:
                                dispatchBatchType=dispatchbatches.getElementsByTagName("batchType")[0]
                                if(dispatchBatchType.firstChild.data == '0'):
                                    newbatchUID=dispatchbatches.getAttribute("batchUID")
                        lastbatchUID=newbatchUID  
                            #print 'last Trajectory UID is: ',lasttrajUID
                    time.sleep(10)
                    context[0x02].setValues(2,0x01,[1])
                    Disptime= os.path.getmtime('C:\Con_Ed_ADS\DispatchBatchResponse.xml')
                    Systime=time.time()
                    Timediff=Systime-Disptime
                    #print Disptime,Systime,Timediff
                    context[0x00].setValues(2,0x03,[1])
                    if(Timediff>420):
                        lastbatchUID="-1"
                        context[0x00].setValues(2,0x03,[0])
        except:
            print "dispatch error"    
            
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
            filedirectory="C:\Con_Ed_ADS\LMP_Pricing"
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
dopFresh = 0.0
dopOro1 = 0.0
dopOro2 = 0.0
dopAve1 = 0.0
dopAve2 = 0.0
dopAlp1 = 0.0
dopAlp2 = 0.0
from threading import Thread
    
if __name__ == '__main__':
    Thread(target = ADS).start()
    Thread(target = ADS_Dispatch).start()
    Thread(target = Mod).start()
    Thread(target = LMP_Price).start()


