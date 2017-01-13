# CAISO-ADS
Python Client to access CAISO's automated dispatch system



##### PYTHON ADS CLIENT ####

1)Download openssl https://slproweb.com/products/Win32OpenSSL.html
2)Run OpenSSL.exe 
3)Convert the .p12 file provided by CAISO to a .pem file using command: OpenSSL> pkcs12 -in C:\Users\Admin\Desktop\PCG2.p12 -out C:\Users\Admin\Desktop\PCG2.pem -nodes
4)Remove passphrase associated with your key using command: OpenSSL> rsa -in C:\Users\Admin\Desktop\PCG2.pem -out C:\Users\Admin\Desktop\PCGkey.pem  
5)Copy first certificate from the file generated at step3 to the key file generated at step5. PEM files can be opened in Notepad. Just append certificate to key
6)Download python 2.6.1
      https://www.python.org/download/releases/2.6.1/
7)Download suds0.4
      https://pypi.python.org/pypi/suds
8)Unzip the suds '.egg' file using a software like 7-zip
9)Place the suds file in your python libraries location. Default should be 'C:\Python26\Lib' 
10)Copy the ADS script to 'C:\Python26'
11)Open the ADS script using a Text Editor like Notepad++
12)In the ADS script pass key.pem,cert.pem files and specify locations to store the DispatchResponse/Trajectory Response and DOP ouput. (additional cues are in the script) 
13)Open Command Prompt (cmd)
14)Navigate to the Python directory. C:\Python26
15)Run command python.exe ADS.py
16)The script will start storing updated DispatchResponse/TrajectoryResponse files in the XML format. Latest DOP MW value will also stored as a .csv file. 
17)SCADA systems are expected to read the csv file for MW setpoint. For additional batch information SCADA should parse the XML files 










##### NOT REQUIRED
Download:
1)http://www.eclipse.org/downloads/packages/release/Luna/R
2)https://java.com/en/download/
3)https://www.python.org/download/releases/2.6.1/
         https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/eclipsepython.html
4)Create new python project
5)download suds0.4
6)add suds to new egg/zip files in eclipse
    https://pypi.python.org/pypi/suds
	
