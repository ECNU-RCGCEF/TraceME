# TraceME_SCRIPTS
### Analytic scripts are essential part of TraceME node package.        
You could find the file `/config/src/main/resources/baseResources/config.properties`       
The paremeter `ScriptFolder` defines the path of analytic scripts.       
You have to place the `scripts` under the `ScriptFolder`      
we have now absorbed five representative analytic functions as follows.        
Some functions can set the map projection to North Hemisphere(NH), South Hemisphere(SH) or a specific area.
#### 1. Annual Traceability Analysis Tool.
Computes temporal tracability analysis (specific area).  
'AnnualTAT.py'  
#### 2. Regional Traceability Analysis Tool.  
Computes Regional (global) tracability analysis (specific area).  
'RegionalTAT.py'  

## python  3.7.2 or higher version ([https://www.python.org/](https://www.python.org/))  
  ```shell
  wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
  tar -zxvf Python-3.7.2.tgz
  cd Python-3.7.2
  ./configure
  make
  ```
+ Check Python：
  ```shell
  python3 --version
  ```

The modules of python that TraceME needs
|module|description|version|
|:----|----|----|
|numpy|The fundamental package for array computing with Python|1.18.3|
|netCDF4|Provides an object-oriented python interface to the netCDF version 4 library|1.5.3|
|scipy|Scientific library for Python|1.4.1|
|matplotlib|Python plotting package|3.2.1|
|basemap|Plot data on map projections with matplotlib|1.2.1|
