# CAISO-ADS
Python Client to access CAISO's automated dispatch system

i) ADS.py(12-Jan-2017)<br />
  1) Stores most recent trajectory and disptach data as an xml file on your machine<br />
  2) Dispatch Operating Traget(DOT) is constantly updated in a csv file on your machine<br />


ii) Modbus_ADS.py(12-Feb-2017)<br />
  Modbus:<br />
    1) Added a Modbus server.<br />
    2) DOT data will be served on Modbus addresses 40001, 40003 and so on.<br /> 
    3) Flag on register 10001 indicates quality of data<br />

  Multiple plants:<br />
    1) If a CAISO certificate has more then one plant associated with it, DOT data will be separated based on 'resource_id' <br />
  
  Better error handling:<br />
    1) Better use of 'try expect' for error handling<br />
    
 iii) ADS_LMP.py(3-Sept-2018)<br />
  Integrated ADS with LMP pricing information. Real time locational marginal price for a particular node is scraped from CAISO OASIS. LMP Price served to SCADA on a Modbus register.LMP function definition uploaded to github. Integration with Modbus_ADS code is straightforward.[CAISO LMP MAP](http://www.caiso.com/PriceMap/Pages/default.aspx)<br /> 


To Do:<br />
 1) Port to Python3<br />
 2) Test on multiple python versions. Currently tested only on 2.6.1 & 2.7.13<br />
 3) Parse other relevant Dispatch and Trajectory data and store records in a database.<br />  
 
 
 Update (23-April-2018)
 1) Caiso discontinued support for TLS1 and TLS1.1 protocols. Support only for TLS1.2 Please upgrade Python to 2.7.9 or higher.

 Update(2-April-2019)<br/>
 1) Added file key_generator.py.  The file is used to create a .pem file from CAISO issued certificate. The .pem certificate file is transported in the ADS python main file for authentication. <br />
 2) Please make sure to add OpenSSL library to your Python installation before running key_generator.py <br />
 3) Please make sure CAISO_ROOT_CA and CAISO_ISSUING_CA are in the certificate store of the machine running your ADS python code
 
