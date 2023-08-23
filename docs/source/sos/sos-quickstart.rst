SOS Quick Start
###########################

Introduction
*****************
SOS (pronuounced "sôs"), standing for Scalable Object Store, is a high-performance, indexed, object-oriented database designed to efficiently manage structured data on persistent media.

SOS was created to solve performance and scalability problems found with other time series databases such as InfluxDB, OpenTSDB, and Graphite.

SOS is strictly typed and uses schema to define the objects stored in the database. The schema specifies the attributes that comprise the object and which attributes are indexed.

SOS implements its own back-end storage model. This allows SOS to support:

* Very high insert rates
* Superior query performance
* Flexible storage management

Configuration Options
**********************

* --disable-python
       * The python commands for managing and querying SOS will not be build
* --enable-doc
       * Man pages will be generated for SOS commands and API
* --enable-html
       * HTML documenation will be generated for SOS commands and API

Compile Dependencies
********************

* If --disable-python is not specified
        * Cython >= .29 (Cython 3.0)
        * Python >= 3.6

* If --enable-doc or --enable-html is specified
        * Doxygen

Installation
****************
The following will build SOS and numsos into the directory /home/XXX/BuildSos

cd into the top level sos checkout directory

.. code-block:: console

    ./autogen.sh # this will call autoreconf to generate `configure` script
    mkdir build
    cd build
    ../configure --prefix=/home/XXX/BuildSos [--disable-python] [--enable-debug] \
        [--enable-doc] [--enable-html]
    # add 'PYTHON=/PYTHON/EXECUTABLE/PATH' if PYTHON environment variable not set
    # add `--enable-debug` to turn on debugging logic inside the SOS libraries
    # add `--disable-python` to disable the Python commands and interface libraries
    make && make install


The build will result in /home/XXX/BuildSos/lib/python3.X/site-packages with sosdb and numsos modules. The sosdb module includes the DataSet class and also the Array and Sos modules, which are written in C for efficiency. The numsos module includes the DataSource, DataSink, Stack, and Transform classes.

Set the environment variables appropriately using: 

.. code-block:: console

  export PATH=/home/XXX/BuildSos/bin:$PATH
  export PYTHONPATH=/home/XXX/BuildSos/lib/python3.X/site-packages:$PYTHONPATH

Importing a CSV file and using the command line tools
*********************************

.. list-table:: CSV and Formatting Files

    * - File
      - Use With
      - Description
    * - meminfo_E5-2698.schema.json
      - sos-schema --add
      - A schema definition file
    * - meminfo_E5-2698.map.json
      - sos-import-csv --map 	
      - A file that tells the import tool which CSV columns go to which schema attributes
    * - meminfo_E5-2698.1000 	
      - sos-import-csv --csv 	
      - 1000 lines of CSV data

These files can be obtained from a clone of the wiki under the directory: files/meminfoCSV2SOS

.. code-block:: console

    > more meminfo_E5-2698.schema.json
     { "name" : "meminfo_E5-2698", "attrs" : [
        { "name" : "timestamp", "type" : "timestamp", "index" : {} },
        { "name" : "component_id", "type" : "uint64", "index" : {} },
        { "name" : "job_id", "type" : "uint64", "index" : {} },
        { "name" : "app_id", "type" : "uint64" },
        { "name" : "MemTotal", "type" : "uint64" },
        { "name" : "MemFree", "type" : "uint64" },
        ...
        { "name" : "DirectMap2M", "type" : "uint64" },
        { "name" : "DirectMap1G", "type" : "uint64" },
        { "name" : "comp_time", "type" : "join", "join_attrs" : [ "component_id", "timestamp" ],
          "index" : {} },
        { "name" : "job_comp_time", "type" : "join", "join_attrs" : [ "job_id", "component_id", "timestamp" ],
          "index" : {} },
        { "name" : "job_time_comp", "type" : "join", "join_attrs" : [ "job_id", "timestamp", "component_id" ],
          "index" : {} }
     ]
     }
     > more meminfo_E5-2698.map.json
     [
        { "target" : "timestamp", "source" : { "column" : 0 } },
        { "target" : "component_id", "source" : { "column" : 3 } },
        { "target" : "job_id", "source" : { "column" : 4 } },
        { "target" : "app_id", "source" : { "column" :  5 } },
        { "target" : "MemTotal", "source" : { "column" : 6 } },
        { "target" : "MemFree", "source" : { "column" : 7 } },
        ...
        { "target" : "DirectMap2M", "source" : { "column" : 47 } },
        { "target" : "DirectMap1G", "source" : { "column" : 48 } }
     ] ]
     >  more meminfo_E5-2698.1000
     1518803953.003055,3055,nid00012,12,5078835....1957888,134217728
     1518803953.003319,3319,nid00013,13,5078835....1957888,134217728

Creating a SOS container

1. Create a container if you don't already have one:

.. code-block:: console

 > sos-db --path /dir/my-container --create

Adding a schema to a container

2. Create the schema in the container:

.. code-block:: console

 > sos-schema --path /dir/my-container --add meminfo_E5-2698.schema.json

Querying for schema information

3. Query the schema to see what's in it:

a. Using sos-schema:

.. code-block:: console

 > sos-schema --path /dir/my-container --query meminfo_E5-2698 --verbose
 meminfo_E5-2698
 Id   Type             Indexed      Name                            
 ---- ---------------- ------------ --------------------------------
   0 TIMESTAMP        True         timestamp
   1 UINT64           True         component_id
   2 UINT64           True         job_id
   3 UINT64                        app_id
   4 UINT64                        MemTotal
   5 UINT64                        MemFree
  ...
  45 UINT64                        DirectMap2M
  46 UINT64                        DirectMap1G
  47 JOIN             True         comp_time [component_id+timestamp]
  48 JOIN             True         job_comp_time [job_id+component_id+timestamp]
  49 JOIN             True         job_time_comp [job_id+timestamp+component_id]

b. OR using sos_cmd:

.. code-block:: console

 > sos_cmd -C /dir/my-container -l
 schema :
    name      : meminfo_E5-2698
    schema_sz : 4904
    obj_sz    : 384
    id        : 129
    -attribute : timestamp
        type          : TIMESTAMP
        idx           : 0
        indexed       : 1
        offset        : 8
    -attribute : component_id
        type          : UINT64
        idx           : 1
        indexed       : 1
        offset        : 16
    -attribute : job_id
        type          : UINT64
        idx           : 2
        indexed       : 1
        offset        : 24
    ...
    -attribute : DirectMap2M
        type          : UINT64
        idx           : 45
        indexed       : 0
        offset        : 368
    -attribute : DirectMap1G
        type          : UINT64
        idx           : 46
        indexed       : 0
        offset        : 376
    -attribute : comp_time
        type          : JOIN
        idx           : 47
        indexed       : 1
        offset        : 384
    -attribute : job_comp_time
        type          : JOIN
        idx           : 48
        indexed       : 1
        offset        : 384
    -attribute : job_time_comp
        type          : JOIN
        idx           : 49
        indexed       : 1
        offset        : 384

Note that there is no data yet in the container (using sos_cmd):

.. code-block:: console

 > sos_cmd -C /dir/my-container -q -S meminfo_E5-2698 -X comp_time
 timestamp                        component_id       job_id             ...      comp_time                        job_comp_time                    job_time_comp                    
 -------------------------------- ------------------  ... -------------------------------- 
 Records 0/0.

Importing CSV data into a container

4. Import the CSV data into the container:

.. code-block:: console

 > sos-import-csv --path /dir/my-container --schema meminfo_E5-2698 --map meminfo_E5-2698.map.json --csv meminfo_E5-2698.1000
 Importing from CSV file meminfo_E5-2698.1000 into /home/gentile/Source/numsos/csvimport/test using map meminfo_E5-2698.map.json
 Created 1000 records

5. You can monitor the progress from another window like this:

.. code-block:: console

 > sos-monitor --path /dir/my-container --schema meminfo_E5-2698

It will take less than a second for 1000 lines, but you can see progress during larger file loads.
Querying data in a container

6. Query for the data in a container:

 a. Query all the data, using comp_time as an index, which will determine the output order
.. code-block:: console

 > sos_cmd -C /dir/my-container -q -S meminfo_E5-2698 -X comp_time
 timestamp                        component_id       job_id            ...   DirectMap1G        comp_time                        job_comp_time                    job_time_comp                    
 -------------------------------- ------------------ ------------------ ... -------------------------------- 
               1518803953.003055                 12            5078835    ... 1957888          134217728  05:00:0C:00:00:00:00:00:00:00:0  05:00:33:7F:4D:00:00:00:00:00:0  05:00:33:7F:4D:00:00:00:00:00:0 
               1518803954.002904                 12            5078835    ... 1957888          134217728  05:00:0C:00:00:00:00:00:00:00:0  05:00:33:7F:4D:00:00:00:00:00:0  05:00:33:7F:4D:00:00:00:00:00:0 
 ...
               1518803961.002805                179                  0                  0   ...        1957888          134217728  05:00:B3:00:00:00:00:00:00:00:0  05:00:00:00:00:00:00:00:00:00:0  05:00:00:00:00:00:00:00:00:00:0 
               1518803962.002661                179                  0                  0    ...       1957888          134217728  05:00:B3:00:00:00:00:00:00:00:0  05:00:00:00:00:00:00:00:00:00:0  05:00:00:00:00:00:00:00:00:00:0 
 -------------------------------- ------------------ ... -------------------------------- 
 Records 1000/1000.

b. Query only for certain variables (also using an index):

.. code-block:: console

 > sos_cmd -C /dir/my-container -q -S meminfo_E5-2698 -X comp_time -f table -V timestamp -V component_id -V Active
 timestamp                        component_id       Active             
 -------------------------------- ------------------ ------------------ 
               1518803953.003055                 12              82672 
               1518803954.002904                 12              82672 
               1518803955.002760                 12              82672 
 ...
               1518803960.001899                179             209712 
               1518803961.002805                179             209712 
               1518803962.002661                179             209712 
 -------------------------------- ------------------ ------------------ 
 Records 1000/1000.

c. Querying with a filter:

.. code-block:: console

 > sos_cmd -C /home/gentile/Source/numsos/csvimport/test -q -S meminfo_E5-2698 -X comp_time -f table -V timestamp -V component_id -V Active -F "timestamp:gt:1518803957" -X comp_time
 timestamp                        component_id       Active             
 -------------------------------- ------------------ ------------------ 
               1518803957.003462                 12              82672 
               1518803958.003315                 12              82672 
               1518803959.001410                 12              82672 
               1518803960.002299                 12              82672 
               1518803961.002159                 12              82672 
   ...
               1518803957.003083                179             209712 
               1518803958.002909                179             209712 
               1518803959.001032                179             209712 
               1518803960.001899                179             209712 
               1518803961.002805                179             209712 
               1518803962.002661                179             209712 
 -------------------------------- ------------------ ------------------ 
 Records 600/600.

d. Querying with multiple filters:

.. code-block:: console

 > sos_cmd -C /dir/my-container -q -S meminfo_E5-2698 -X comp_time -f table -V timestamp -V component_id -V Active -F "timestamp:gt:1518803960" -X comp_time -F "component_id:gt:177"
 timestamp                        component_id       Active             
 -------------------------------- ------------------ ------------------ 
               1518803960.002343                178             682756 
               1518803961.002104                178             682756 
               1518803962.001890                178             682756 
               1518803960.001899                179             209712 
               1518803961.002805                179             209712 
               1518803962.002661                179             209712 
 -------------------------------- ------------------ ------------------ 
 Records 6/6.

