# TraceME_PORTAL
To see detailed information about TraceME, please check the [wiki page](https://github.com/THU-EarthInformationScienceLab/TraceME_NODE/wiki).
## Before Installing TraceME PORTAL
`Notice`: This package can be installed in any web server. You can deploy this package either on Windows paltform or on Linux platform. To ensure the application work correctly, following procedures have to be conducted before your installation:
#### 1.	Installing MySQL Server and Client (http://www.mysql.com/downloads/ )     
```Bash 
sudo apt-get install mysql-server mysql-client  #For Ubuntu 12.04
sudo service mysql start #open mysql service
``` 
`Note`: To ensure the correct connection to the database, you may have to modify the file `/etc/mysql/my.cnf` ( or `/etc/mysql/mysql.conf.d/mysqld.cnf` in newer version ) and annotate the row starts with bind-address
#### 2.	Installing Apache 2 HTTP Server (http://httpd.apache.org/)   
```Bash 
sudo apt-get install apache2     #For Ubuntu 12.04
``` 
`Note`:For windows users,please choose binary installer (http://archive.apache.org/dist/httpd/binaries/win32/), version 2.2.22 is recommeded.        
`Note`:If you want to compile Apache2 by yourself, you need to install apr, apr-util, prce and zlib before you installation.
#### 3.	Installing php5 with extensions (http://php.net/downloads.php)
```Bash 
sudo apt-get install php5 php5-mysql php5-gd php5-tidy php5-curl     #For Ubuntu 12.04
``` 
`Note`:If you want to compile php5 by yourself, you should install libpng(v1.6.2), libxpm,jpeg,freetype,libgd,tidy,curl,mysql first. 
`Note`:For windows users,please choose binary installer (http://windows.php.net/downloads/releases/archives/), version 5.3.10 is recommended. We also recommend you install all the enxtensions while running the php installer. Curl,mysql,gd2,tidy extensions are required.

## Installation procedures
#### 1.	Database preparation.     
You have to create a user name of your database system, obtain the ip address,access port,username and password
```Bash 
e.g. CREATE USER 'username'@'%' IDENTIFIED BY 'password'; 
```
#### 2.	Create a database.      
Create a database. Grand privileges to the user created in step 1.  
```Bash 
e.g. # if the name of your database called userdb
     # you can enter mySQL using command line 'mysql -u guest -p', then use following codes.
     GRANT all privileges ON userdb.* TO 'username'@'%'
     FLUSH PRIVILEGES;
```
#### 3.	Create database tables.      
The path of initiation script is: `TraceME_PORTAL/init.sql`     
You have to enter mySQL, use the database in step2 and run this script.      
You should first enter the directory `TraceME_PORTAL/init.sql` of the TraceME-PORTAL source code folder.
Then You have to enter mySQL using command line `mysql -u {username} -p`, use the database created in `step2` and run the following script.
```Bash 
use {jdbc.database}
source init.sql;
``` 
#### 4.	Grant write permission. [For Linux]     
Grant write permission to `ts_search/assets` and `ts_search/protected/runtime`       
#### 5. Database access configuration.     
Find the file `TraceME_PORTAL/ts_search/protected/config/main.php` and replace the database information from line `57` to line `64`. For example:
```php		
'db'=>array(
			'connectionString' => 'mysql:host=localhost;dbname=userdb',
			'emulatePrepare' => true,
			'username' => 'guest',
			'password' => '123456',
			'charset' => 'utf8',
            'tablePrefix'=>'ts_',
		 ),
``` 
#### 6. Server access configuration.       
find the file `TraceME_PORTAL/ts_search/protected/models/TSInterface.php` and modify the NODE server root address in line2, for example, if you want to connect the web appication to the TraceME node configured on 100.101.100.111:8088, the root path in the tomcat server of that node is  `/worker-node`, you can use following code:
```php
define('TSInterfaceROOT','http://100.101.100.111:8088/worker-node/');   
``` 
#### 7. Modify the virtual directory.     
```Bash 
sudo vi /etc/apache2/sites-enabled/000-default  
# Then Configure the virtual directory `/TraceME_PORTAL/ts_search` after "DocumentRoot" keyword
# OR you can use symlink
sudo /etc/init.d/apache2 restart    #restart Apache
``` 

#### 8. A brief how-to-use guide
- After setting up the portal, open the index page and create an account.
- Login with that account, then click search to find the wanted data (filtered by Institute, Model, Experiment, etc.)
- Choose a set of data and specify start/end year and the ncl functions you want to use.
- Spatial Ranger specification: South/North from -90 to 90, and West/East from 0 to 360.
- Submit task and view status/result in the redirected window, you can also download the result after task finished.

#### 9. Some problems you may encounter
- 403 forbidden, Permission denied: access to / denied

  check access permission in /etc/httpd/conf/httpd.conf, and check if the /, root directory have +x privileges (every level of the parent directories should have that priviledge).

