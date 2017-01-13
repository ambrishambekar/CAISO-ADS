lastbatchUID="-1"
lasttrajUID="-1"
print 'last batch UID is: ',lastbatchUID
print 'last Trajectory UID is: ',lasttrajUID

count = 0
while (count <2):
    import urllib2, httplib,socket,base64,gzip,StringIO
    from suds.client import Client
    from suds.transport.http import HttpTransport
    import xml.etree.ElementTree as ET
    import time
    from xml.dom.minidom import parseString
    import os   
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
    transport = HTTPSClientCertTransport('C:\Robert Lopezx5937_1.pem',
                                         'C:\Robert Lopezx5937_1.pem'))
    #print client


    #Dispatch Batch data
    
    LastBatchUID=client.service.getDispatchBatchesSinceUID(lastbatchUID)
    #print lastbatchUID,'\n \n'
    #print LastBatchUID
    root = ET.fromstring(LastBatchUID)
    for child in root:
        for grandchild in child:
            newbatchUID= grandchild.get('batchUID')
    print 'BatchUID is:',newbatchUID
    lastbatchUID=newbatchUID 
    #print 'last batch UID is: ',lastbatchUID    
    DispatchBatch1= client.service.getDispatchBatch(lastbatchUID)
    decode = base64.b64decode(DispatchBatch1)
    stringread = StringIO.StringIO(decode)
    decompress = gzip.GzipFile(fileobj=stringread)
    DecodedDispatch = decompress.read()
    #print DecodedDispatch
    with open("C:\\Users\\Ambrish Ambekar\\Desktop\\ADS_Out\\OutputResponse\\DispatchBatchResponse.xml", "w") as text_file:
                text_file.write(format(DecodedDispatch))
    
    
    #Trajectory data
    print 'TrajUID is:',lasttrajUID
    IsNewTraj=client.service.isNewTrajData(lasttrajUID)
    print IsNewTraj
    if count==0:
        IsNewTraj = False
        print 'initial loop'
        count = count + 1
        Trajectory= client.service.getTrajectoryData(lasttrajUID)
        decode_1 = base64.b64decode(Trajectory)
        stringread_1 = StringIO.StringIO(decode_1)
        decompress_1 = gzip.GzipFile(fileobj=stringread_1)
        DecodedTrajectory = decompress_1.read()
        #print DecodedTrajectory
        with open("C:\\Users\\Ambrish Ambekar\\Desktop\\ADS_Out\\OutputResponse\\TrajectoryResponse.xml", "w") as text_file:
            text_file.write(format(DecodedTrajectory))
        dom=parseString(DecodedTrajectory)
        xmlTags = dom.getElementsByTagName('dop')
        #print xmlTags
        xmlData = []
        for tag in xmlTags:
            xmlData.append(tag.firstChild.data)
            dop= xmlData[-1:][0]
        print 'DOP is:',dop
        dop1=float(dop)*1000
        with open("C:\\Users\\Ambrish Ambekar\\Desktop\\ADS_Out\\OutputResponse\\dop.csv", "w") as text_file:
            text_file.write(format(dop))
        #with open("S:\\dop.csv", "w") as text_file:
            #text_file.write(format(int(dop1)))
        root1 = ET.fromstring(DecodedTrajectory)
        #print root1.tag,root1.attrib
        for child1 in root1:
            #print child1.tag,child1.attrib
                for grandchild1 in child1:
                    newTrajUID=grandchild1.get("batchUID")
                    """#print grandchild1.tag 
                    for greatgrandchild1 in grandchild1:
                        #print greatgrandchild1.tag
                        for greatgreatgrandchild1 in greatgrandchild1:
                            #print greatgreatgrandchild1.get("dopUID")
                            for ggchild in greatgreatgrandchild1:
                                print ggchild.text"""
                                                                 
                            
                  
        lasttrajUID=newTrajUID
            
    elif IsNewTraj==True:
        print 'infinite loop'
        Trajectory= client.service.getTrajectoryData(lasttrajUID)
        decode_1 = base64.b64decode(Trajectory)
        stringread_1 = StringIO.StringIO(decode_1)
        decompress_1 = gzip.GzipFile(fileobj=stringread_1)
        DecodedTrajectory = decompress_1.read()
        #print DecodedTrajectory
        with open("C:\\Users\\Ambrish Ambekar\\Desktop\\ADS_Out\\OutputResponse\\TrajectoryResponse.xml", "w") as text_file:
            text_file.write(format(DecodedTrajectory))
        dom=parseString(DecodedTrajectory)
        xmlTags = dom.getElementsByTagName('dop')
            #print xmlTags
        xmlData = []
        for tag in xmlTags:
            xmlData.append(tag.firstChild.data)
            dop= xmlData[-1:][0]
        print 'DOP is:',dop
        with open("C:\\Users\\Ambrish Ambekar\\Desktop\\ADS_Out\\OutputResponse\\dop.csv", "w") as text_file:
            text_file.write(format(dop))
        #with open("S:\\dop.csv", "w") as text_file:
            #dop1=float(dop)*1000
            #text_file.write(format(int(dop1)))
        root1 = ET.fromstring(DecodedTrajectory)
        #print root1.tag,root1.attrib
        for child1 in root1:
            #print child1.tag,child1.attrib
            for grandchild1 in child1:
                newTrajUID=grandchild1.get("batchUID")
                """#print grandchild1.tag 
                    for greatgrandchild1 in grandchild1:
                        #print greatgrandchild1.tag
                        for greatgreatgrandchild1 in greatgrandchild1:
                            #print greatgreatgrandchild1.get("dopUID")
                            for ggchild in greatgreatgrandchild1:
                                print ggchild.text"""
                                                                 
                            
                  
            lasttrajUID=newTrajUID
            #print 'last Trajectory UID is: ',lasttrajUID
           

    time.sleep(5)
	
print count

