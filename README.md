# CAISO-ADS
Python Client to access CAISO's automated dispatch system

ADS.py
  1) Stores most recent trajectory and disptach data as an xml file on your machine
  2) Dispatch Operational Traget(DOT) is constantly updated in a csv file on your machine


Modbus_ADS.py
  Modbus:
    1) Added a Modbus server. 
    2) DOT data will be served on Modbus addresses 40001, 40003 and so on. 
    3) Flag on register 10001 indicates quality of data

  Multiple plants:
    1) Added functionality to separate data for multiple power plants, if one CAISO certificate has more then one plant associated with it.
  
  Better error handling:
    1) Better use of 'try expect' for error handling
    
    
To Do:
 1) Port to Python3
 2) Test on multiple python versions. Currently tested only on 2.6.1
 3) Parse other relevant Dispatch and Trajectory data and store records in a database.
