LDMS Quick Start
###########################

Installation
*****************

Ubuntu 16.04 
------------

Prerequisites
=============
* Ubuntu 16.04 (LDMS runs on any *nix OS; Ubuntu was used in this demonstration)
* openssl-dev
* gnu compiler
* swig
* autoconf
* libtool
* libreadline6
* libreadline6-dev
* libevent
* libevent-dev
* autogen
* python-yams
* doxygen
* gettext
* python-2.7-dev
* libglib2.0-dev

Getting the Source
-----------------------
* This example shows cloning into ~/Source/ovis-4 and putting the build in ~/Build/OVIS-4

.. code-block:: RST
 
 mkdir $HOME/Source
 mkdir $HOME/Build
 cd $HOME/Source
 git clone https://github.com/ovis-hpc/ovis.git ovis-4
 
Building the Source
-----------------------
* Go to your source directory


cd $HOME/Source/ovis-4
git checkout OVIS-4

* Run autogen.sh

.. code-block:: RST
 
 ./autogen.sh

* Configure and Build (Builds default linux samplers. Build installation directory is prefix):

.. code-block:: RST
 
 mkdir build
 cd build
 ../configure --prefix=$HOME/Build/OVIS-4.x
 make
 make install

RHEL 9  
------------

Prerequisites
=============
* RHEL 9
* openssl-devel
* pkg-config
* automake
* libtool
* python3 (or higher)
* python3-devel.x86_64 (or higher)
* bison
* flex

Prerequisite Installation
---------------------------
The following steps were ran on a basic RHEL 9 instance via AWS. 

.. code-block:: RST

 sudo yum update -y
 sudo yum install automake -y
 sudo yum install openssl-devel -y 
 sudo yum install pkg-config -y
 sudo yum install hdf5-tools libhdf5-openmpi-dev openmpi-bin -y
 sudo yum install libtool -y
 sudo yum install python3 -y
 sudo yum install python3-devel.x86_64 -y
 
 sudo yum install make -y 
 sudo yum install bison -y 
 sudo yum install flex -y
 

LDMS Build and Install
--------------------------
* This example shows cloning into ~/ovis and putting the build in ~/ovis/build

.. code-block:: RST
 
 git clone https://github.com/ovis-hpc/ovis.git
 cd ovis && mkdir build/

* Run autogen.sh

.. code-block:: RST
 
 ./autogen.sh

* Configure and Build (Builds default linux samplers. Build installation directory is prefix):

.. code-block:: RST
 
 cd build
 ../configure --prefix=$HOME/ovis/build/
 make
 make install

Basic Configuration and Running
*******************************
* Set up environment:

.. code-block:: RST

 export LDMS_INSTALL_PATH=$HOME/ovis/build/
 export LD_LIBRARY_PATH=$LDMS_INSTALL_PATH/lib/:$LD_LIBRARY_PATH
 export LDMSD_PLUGIN_LIBPATH=$LDMS_INSTALL_PATH/lib/ovis-ldms
 export ZAP_LIBPATH=$LDMS_INSTALL_PATH/lib/ovis-ldms
 export PATH=$LDMS_INSTALL_PATH/sbin:$LDMS_INSTALL_PATH/bin:$PATH
 export PYTHONPATH=$LDMS_INSTALL_PATH/lib/python3.6/site-packages

Sampler
***********************
* Make a configuration file (called sampler.conf) to load the meminfo and vmstat samplers with the following contents:

.. code-block:: RST

  load name=meminfo
  config name=meminfo producer=${HOSTNAME} instance=${HOSTNAME}/meminfo component_id=${COMPONENT_ID} schema=meminfo job_set=${HOSTNAME}/jobinfo uid=12345 gid=12345 perm=0755
  start name=meminfo interval=${SAMPLE_INTERVAL} offset=${SAMPLE_OFFSET}
  #
  load name=vmstat
  config name=vmstat producer=${HOSTNAME} instance=${HOSTNAME}/vmstat component_id=${COMPONENT_ID} schema=vmstat job_set=${HOSTNAME}/jobinfo uid=0 gid=0 perm=0755
  start name=vmstat interval=${SAMPLE_INTERVAL} offset=${SAMPLE_OFFSET}
 
Note that munge is optional, although we do have the specification of munge-based permissions in the above example.
 
* Set up additional environmental variables for configuration file:

.. code-block:: RST

 export COMPONENT_ID=1
 export SAMPLE_INTERVAL=1000000
 export SAMPLE_OFFSET=50000
 
This will set the samplers to collect at 1 second intervals.

* Run a daemon using munge authentication: 

.. code-block:: RST
 
  ldmsd -x sock:10444 -c sampler.conf -l /tmp/demo_ldmsd_log -v DEBUG -a munge  -r $(pwd)/ldmsd.pid
 
Or in non-cluster environments where munge is unavailable:

.. code-block:: RST
 
  ldmsd -x sock:10444 -c sampler.conf -l /tmp/demo_ldmsd_log -v DEBUG -r $(pwd)/ldmsd.pid
  
For the rest of these instructions, omit the "-a munge" if you do not have munge running. This will also write out DEBUG-level information to the specified (-l) log.

* Run ldms_ls on that node to see set, meta-data, and contents:

.. code-block:: RST

 ldms_ls -h localhost -x sock -p 10444 -a munge
 ldms_ls -h localhost -x sock -p 10444 -v -a munge
 ldms_ls -h localhost -x sock -p 10444 -l -a munge
 
Note the use of munge. Users will not be able to query a daemon launched with munge if not querying with munge. Users will only be able to see sets as allowed by the permissions in response to ldms_ls.

Example (note permissions and update hint):

.. code-block:: RST

 ldms_ls -h localhost -x sock -p 10444 -l -v -a munge
 
Output:

.. code-block:: RST

 host1/vmstat: consistent, last update: Mon Oct 22 16:58:15 2018 -0600 [1385us] 
   APPLICATION SET INFORMATION ------
              updt_hint_us : 5000000:0
   METADATA --------
     Producer Name : host1
     Instance Name : host1/vmstat
       Schema Name : vmstat
              Size : 5008
      Metric Count : 110
                GN : 2
              User : root(0)
             Group : root(0)
       Permissions : -rwxr-xr-x
   DATA ------------
         Timestamp : Mon Oct 22 16:58:15 2018 -0600 [1385us]
          Duration : [0.000106s]
        Consistent : TRUE
              Size : 928
                GN : 110
   -----------------
  M u64        component_id                               1
  D u64        job_id                                     0
  D u64        app_id                                     0
  D u64        nr_free_pages                              32522123
  ...
  D u64        pglazyfree                                 1082699829 
  host1/meminfo: consistent, last update: Mon Oct 22 16:58:15 2018 -0600 [1278us] 
   APPLICATION SET INFORMATION ------
              updt_hint_us : 5000000:0
   METADATA --------
     Producer Name : host1
     Instance Name : host1/meminfo
       Schema Name : meminfo
              Size : 1952
      Metric Count : 46
                GN : 2
              User : myuser(12345)
             Group : myuser(12345)
       Permissions : -rwx------
   DATA ------------
         Timestamp : Mon Oct 22 16:58:15 2018 -0600 [1278us]
          Duration : [0.000032s]
        Consistent : TRUE
              Size : 416
                GN : 46
   -----------------
  M u64        component_id                               1
  D u64        job_id                                     0
  D u64        app_id                                     0
  D u64        MemTotal                                   131899616
  D u64        MemFree                                    130088492
  D u64        MemAvailable                               129556912
  ...
  D u64        DirectMap1G                                134217728
  
Aggregator Using Data Pull
***********************
* Start another sampler daemon with a similar configuration on host2 using component_id=2, as above.
* Make a configuration file (called agg11.conf) to aggregate from the two samplers at different intervals with the following contents:

.. code-block:: RST

 prdcr_add name=host1 host=host1 type=active xprt=sock port=10444 interval=20000000
 prdcr_start name=host1
 updtr_add name=policy_h1 interval=1000000 offset=100000
 updtr_prdcr_add name=policy_h1 regex=host1
 updtr_start name=policy_h1
 prdcr_add name=host2 host=host2 type=active xprt=sock port=10444 interval=20000000
 prdcr_start name=host2
 updtr_add name=policy_h2 interval=2000000 offset=100000
 updtr_prdcr_add name=policy_h2 regex=host2
 updtr_start name=policy_h2
 
* On host3, set up the environment as above and run a daemon:

.. code-block:: RST

 ldmsd -x sock:10445 -c agg11.conf -l /tmp/demo_ldmsd_log -v ERROR -a munge
 
* Run ldms_ls on the aggregator node to see set listing:

.. code-block:: RST

 ldms_ls -h localhost -x sock -p 10445 -a munge
 
Output:

.. code-block:: RST

 host1/meminfo
 host1/vmstat
 host2/meminfo
 host2/vmstat
 
 
You can also run ldms_ls to query the ldms daemon on the remote node:

.. code-block:: RST

 ldms_ls -h host1 -x sock -p 10444 -a munge 


Output:

.. code-block:: RST

 host1/meminfo
 host1/vmstat
 

ldms_ls -l shows the detailed output, including timestamps. This can be used to verify that the aggregator is aggregating the two hosts' sets at different intervals.

Aggregator Using Data Push
***********************
* Use same sampler configurations as above.
* Make a configuration file (called agg11_push.conf) to cause the two samplers to push their data to the aggregator as they update.

  * Note that the prdcr configs remain the same as above but the updater_add includes the additional options: push=onchange auto_interval=false.
  
  * Note that the updtr_add interval has no effect in this case but is currently required due to syntax checking

.. code-block:: RST

 prdcr_add name=host1 host=host1 type=active xprt=sock port=10444 interval=20000000
 prdcr_start name=host1
 prdcr_add name=host2 host=host2 type=active xprt=sock port=10444 interval=20000000
 prdcr_start name=host2
 updtr_add name=policy_all interval=5000000 push=onchange auto_interval=false
 updtr_prdcr_add name=policy_all regex=.*
 updtr_start name=policy_all
 
 
* On host3, set up the environment as above and run a daemon: 

.. code-block:: RST

 ldmsd -x sock:10445 -c agg11_push.conf -l /tmp/demo_ldmsd_log -v DEBUG -a munge
 
* Run ldms_ls on the aggregator node to see set listing:

.. code-block:: RST

 ldms_ls -h localhost -x sock -p 10445 -a munge 
 
Output:

.. code-block:: RST

 host1/meminfo
 host1/vmstat
 host2/meminfo
 host2/vmstat
 

Two Aggregators Configured as Failover Pairs 
***********************
* Use same sampler configurations as above
* Make a configuration file (called agg11.conf) to aggregate from one sampler with the following contents:

.. code-block:: RST

 prdcr_add name=host1 host=host1 type=active xprt=sock port=10444 interval=20000000
 prdcr_start name=host1
 updtr_add name=policy_all interval=1000000 offset=100000
 updtr_prdcr_add name=policy_all regex=.*
 updtr_start name=policy_all
 failover_config host=host3 port=10446 xprt=sock type=active interval=1000000 peer_name=agg12 timeout_factor=2
 failover_start
 
* On host3, set up the environment as above and run two daemons as follows:

.. code-block:: RST

 ldmsd -x sock:10445 -c agg11.conf -l /tmp/demo_ldmsd_log -v ERROR -n agg11 -a munge
 ldmsd -x sock:10446 -c agg12.conf -l /tmp/demo_ldmsd_log -v ERROR -n agg12 -a munge
 
* Run ldms_ls on each aggregator node to see set listing:

.. code-block:: RST

 ldms_ls -h localhost -x sock -p 10445 -a munge 
 host1/meminfo
 host1/vmstat
 ldms_ls -h localhost -x sock -p 10446 -a munge
 host2/meminfo
 host2/vmstat
 
* Kill one daemon:

.. code-block:: RST

 kill -SIGTERM <pid of daemon listening on 10445>
 
* Make sure it died
* Run ldms_ls on the remaining aggregator to see set listing:

.. code-block:: RST

 ldms_ls -h localhost -x sock -p 10446 -a munge 
 
Output:

.. code-block:: RST

 host1/meminfo
 host1/vmstat
 host2/meminfo
 host2/vmstat

Set Groups
***********************
A set group is an LDMS set with special information to represent a group of sets inside ldmsd. A set group would appear as a regular LDMS set to other LDMS applications, but ldmsd and ldms_ls will treat it as a collection of LDMS sets. If ldmsd updtr updates a set group, it also subsequently updates all the member sets. Performing ldms_ls -l on a set group will also subsequently perform a long-query all the sets in the group.

To illustrate how a set group works, we will configure 2 sampler daemons with set groups and 1 aggregator daemon that updates and stores the groups in the following subsections. 

Creating a set group and inserting sets into it
***********************
The following is a configuration file for our s0 LDMS daemon (sampler #0) that collects sda disk stats in the s0/sda set and lo network usage in the s0/lo set. The s0/grp set group is created to contain both s0/sda and s0/lo. 

.. code-block:: RST

 ### s0.conf
 load name=procdiskstats                                         
 config name=procdiskstats device=sda producer=s0 instance=s0/sda
 start name=procdiskstats interval=1000000 offset=0              
                                                                 
 load name=procnetdev                                            
 config name=procnetdev ifaces=lo producer=s0 instance=s0/lo     
 start name=procnetdev interval=1000000 offset=0                 
                                                                 
 setgroup_add name=s0/grp producer=s0 interval=1000000 offset=0  
 setgroup_ins name=s0/grp instance=s0/sda,s0/lo    

The following is the same for s1 sampler daemon, but with different devices (sdb and eno1). 

.. code-block:: RST

 ### s1.conf
 load name=procdiskstats                                         
 config name=procdiskstats device=sdb producer=s1 instance=s1/sdb
 start name=procdiskstats interval=1000000 offset=0              
                                                                 
 load name=procnetdev                                            
 config name=procnetdev ifaces=eno1 producer=s1 instance=s1/eno1 
 start name=procnetdev interval=1000000 offset=0                 
                                                                 
 setgroup_add name=s1/grp producer=s1 interval=1000000 offset=0  
 setgroup_ins name=s1/grp instance=s1/sdb,s1/eno1  
 
The s0 LDMS daemon is listening on port 10000 and the s1 LDMS daemon is listening on port 10001. 

Perform ldms_ls on a group
***********************
Performing ldms_ls -v or ldms_ls -l on a LDMS daemon hosting a group will perform the query on the set representing the group itself as well as iteratively querying the group's members. Example: 

.. code-block:: RST

 ldms_ls -h localhost -x sock -p 10000
 
Output:

.. code-block:: RST

 ldms_ls -h localhost -x sock -p 10000 -v s0/grp | grep consistent
 
Output:

.. code-block:: RST

 s0/grp: consistent, last update: Mon May 20 15:44:30 2019 -0500 [511879us]
 s0/lo: consistent, last update: Mon May 20 16:13:16 2019 -0500 [1126us]
 s0/sda: consistent, last update: Mon May 20 16:13:17 2019 -0500 [1176us]
 
.. code-block:: RST

  ldms_ls -h localhost -x sock -p 10000 -v s0/lo | grep consistent # only query lo set from set group s0
  

NOTE: The update time of the group set is the time that the last set was inserted into the group. 

Update / store with set group
***********************
The following is an example of an aggregator configuration to match-update only the set groups, and their members, with storage policies: 

.. code-block:: RST

 # Stores                                                                                    
 load name=store_csv                                                                         
 config name=store_csv path=csv
 # strgp for netdev, csv file: "./csv/net/procnetdev"
 strgp_add name=store_net plugin=store_csv container=net schema=procnetdev                   
 strgp_prdcr_add name=store_net regex=.*                                                     
 strgp_start name=store_net                                                                  
 # strgp for diskstats, csv file: "./csv/disk/procdiskstats"
 strgp_add name=store_disk plugin=store_csv container=disk schema=procdiskstats              
 strgp_prdcr_add name=store_disk regex=.*                                                    
 strgp_start name=store_disk                                                                 
                                                                                             
 # Updater that updates only groups                                  
 updtr_add name=u interval=1000000 offset=500000                                             
 updtr_match_add name=u regex=ldmsd_grp_schema match=schema                                  
 updtr_prdcr_add name=u regex=.*                                                             
 updtr_start name=u   
 
Performing ldms_ls on the LDMS aggregator daemon exposes all the sets (including groups)

.. code-block:: RST

 ldms_ls -h localhost -x sock -p 9000
 
Output:

.. code-block:: RST

 s1/sdb
 s1/grp
 s1/eno1
 s0/sda
 s0/lo
 s0/grp
 
Performing ldms_ls -v on a LDMS daemon hosting a group again but only querying the group and its members: 

.. code-block:: RST

 ldms_ls -h localhost -x sock -p 9000 -v s1/grp | grep consistent
 
Output:

.. code-block:: RST

 s1/grp: consistent, last update: Mon May 20 15:42:34 2019 -0500 [891643us]
 s1/sdb: consistent, last update: Mon May 20 16:38:38 2019 -0500 [1805us]
 s1/eno1: consistent, last update: Mon May 20 16:38:38 2019 -0500 [1791us]
 
 
The following is an example of the CSV output: 

.. code-block:: RST
 
  > head csv/*/*

.. code-block:: RST

 #Time,Time_usec,ProducerName,component_id,job_id,app_id,reads_comp#sda,reads_comp.rate#sda,reads_merg#sda,reads_merg.rate#sda,sect_read#sda,sect_read.rate#sda,time_read#sda,time_read.rate#sda,writes_comp#sda,writes_comp.rate#sda,writes_merg#sda,writes_merg.rate#sda,sect_written#sda,sect_written.rate#sda,time_write#sda,time_write.rate#sda,ios_in_progress#sda,ios_in_progress.rate#sda,time_ios#sda,time_ios.rate#sda,weighted_time#sda,weighted_time.rate#sda,disk.byte_read#sda,disk.byte_read.rate#sda,disk.byte_written#sda,disk.byte_written.rate#sda
 1558387831.001731,1731,s0,0,0,0,197797,0,9132,0,5382606,0,69312,0,522561,0,446083,0,418086168,0,966856,0,0,0,213096,0,1036080,0,1327776668,0,1380408297,0
 1558387832.001943,1943,s1,0,0,0,108887,0,32214,0,1143802,0,439216,0,1,0,0,0,8,0,44,0,0,0,54012,0,439240,0,1309384656,0,1166016512,0
 1558387832.001923,1923,s0,0,0,0,197797,0,9132,0,5382606,0,69312,0,522561,0,446083,0,418086168,0,966856,0,0,0,213096,0,1036080,0,1327776668,0,1380408297,0
 1558387833.001968,1968,s1,0,0,0,108887,0,32214,0,1143802,0,439216,0,1,0,0,0,8,0,44,0,0,0,54012,0,439240,0,1309384656,0,1166016512,0
 1558387833.001955,1955,s0,0,0,0,197797,0,9132,0,5382606,0,69312,0,522561,0,446083,0,418086168,0,966856,0,0,0,213096,0,1036080,0,1327776668,0,1380408297,0
 1558387834.001144,1144,s1,0,0,0,108887,0,32214,0,1143802,0,439216,0,1,0,0,0,8,0,44,0,0,0,54012,0,439240,0,1309384656,0,1166016512,0
 1558387834.001121,1121,s0,0,0,0,197797,0,9132,0,5382606,0,69312,0,522561,0,446083,0,418086168,0,966856,0,0,0,213096,0,1036080,0,1327776668,0,1380408297,0
 1558387835.001179,1179,s0,0,0,0,197797,0,9132,0,5382606,0,69312,0,522561,0,446083,0,418086168,0,966856,0,0,0,213096,0,1036080,0,1327776668,0,1380408297,0
 1558387835.001193,1193,s1,0,0,0,108887,0,32214,0,1143802,0,439216,0,1,0,0,0,8,0,44,0,0,0,54012,0,439240,0,1309384656,0,1166016512,0
 
 ==> csv/net/procnetdev <==
 #Time,Time_usec,ProducerName,component_id,job_id,app_id,rx_bytes#lo,rx_packets#lo,rx_errs#lo,rx_drop#lo,rx_fifo#lo,rx_frame#lo,rx_compressed#lo,rx_multicast#lo,tx_bytes#lo,tx_packets#lo,tx_errs#lo,tx_drop#lo,tx_fifo#lo,tx_colls#lo,tx_carrier#lo,tx_compressed#lo
 1558387831.001798,1798,s0,0,0,0,12328527,100865,0,0,0,0,0,0,12328527,100865,0,0,0,0,0,0
 1558387832.001906,1906,s0,0,0,0,12342153,100925,0,0,0,0,0,0,12342153,100925,0,0,0,0,0,0
 1558387832.001929,1929,s1,0,0,0,3323644475,2865919,0,0,0,0,0,12898,342874081,1336419,0,0,0,0,0,0
 1558387833.002001,2001,s0,0,0,0,12346841,100939,0,0,0,0,0,0,12346841,100939,0,0,0,0,0,0
 1558387833.002025,2025,s1,0,0,0,3323644475,2865919,0,0,0,0,0,12898,342874081,1336419,0,0,0,0,0,0
 1558387834.001106,1106,s0,0,0,0,12349089,100953,0,0,0,0,0,0,12349089,100953,0,0,0,0,0,0
 1558387834.001130,1130,s1,0,0,0,3323647234,2865923,0,0,0,0,0,12898,342875727,1336423,0,0,0,0,0,0
 1558387835.001247,1247,s0,0,0,0,12351337,100967,0,0,0,0,0,0,12351337,100967,0,0,0,0,0,0
 1558387835.001274,1274,s1,0,0,0,3323647298,2865924,0,0,0,0,0,12898,342875727,1336423,0,0,0,0,0,0


