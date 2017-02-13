# CAISO-ADS
Python Client to access CAISO's automated dispatch system

ADS.py(12-Jan-2017)<br />
  1) Stores most recent trajectory and disptach data as an xml file on your machine<br />
  2) Dispatch Operating Traget(DOT) is constantly updated in a csv file on your machine<br />


Modbus_ADS.py(12-Feb-2017)<br />
  Modbus:<br />
    1) Added a Modbus server.<br />
    2) DOT data will be served on Modbus addresses 40001, 40003 and so on.<br /> 
    3) Flag on register 10001 indicates quality of data<br />

  Multiple plants:<br />
    1) If a CAISO certificate has more then one plant associated with it, DOT data will be separated based on 'resource_id' <br />
  
  Better error handling:<br />
    1) Better use of 'try expect' for error handling<br />
    
    
To Do:<br />
 1) Port to Python3<br />
 2) Test on multiple python versions. Currently tested only on 2.6.1<br />
 3) Parse other relevant Dispatch and Trajectory data and store records in a database.<br />
