Streams-enabled Application Data Collectors
###########################

Caliper
***********************

DARSHAN
***********************
This section covers basics steps on how to compile, build and use the Darshan-LDMS Integration code (i.e. darshanConnector). The following application tests are part of the Darshan program and can be found under <darshan-prefix>/darshan/darshan-test/regression/test-cases/src/. 

.. note::
  
  LDMS must already be installed on the system or locally. If it is not, then please following the ``Getting The Source`` and ``Building The Source`` in the `LDMS Quickstart Guide <ldms-quickstart.rst>`_.

Compile and Build with LDMS
---------------------------
* Run the following to build Darshan and link against an existing LDMS library on the system.
  
.. code-block:: RST
  
  git clone https://github.com/darshan-hpc/darshan.git
  module swap PrgEnv-intel/6.0.9 PrgEnv-gnu # depending on the system. 
  cd <darshan-prefix>/darshan/ && mkdir build/
  ./prepare.sh && cd build/
  ../configure --with-log-path=<darshan-prefix>/darshan/build/logs --prefix=<darshan-prefix>/darshan/build/install --with-jobid-env=PBS_JOBID CC=cc --with-ldms=<path_to_ldms_install> && make && make install
  
* To build HDF5 module for darshan, you must first load the module with ``module load cray-hdf5-parallel`` then run configure as follows: 
.. code-block:: RST

  ../configure --with-log-path=<darshan-prefix>/darshan/build/logs --prefix=<darshan-prefix>/darshan/build/install --with-jobid-env=PBS_JOBID CC=cc --with-ldms=/projects/ovis/darshanConnector/ovis/LDMS_install --enable-hdf5-mod --with-hdf5=/opt/cray/pe/hdf5-parallel/1.12.0.0/gnu/8.2  && make && make install

.. note::
  
  This configuration is specific to a CRAY machine (i.e. compile with cc instead of mpicc). For more information on how to install and build the code across various platforms, please visit the `Darshan's Runtime Installation Page <https://www.mcs.anl.gov/research/projects/darshan/docs/darshan-runtime.html>`_ 
  
Configuration For Darshan DXT Test Case(s)  
------------------------------------------
Below are the instructions to configure your system for running a darshan test (mpi-io-test.c) for the darshanConnector code. All Darshan application test scripts are located in ``<darshan-prefix>/darshan/darshan-test/regression/test-cases/``.

* Double Check Test Scripts
Double check the test scripts are modified appropriately in order to run a successful test. Make sure the following file contains the desired partition name for the sbatch command.
Darshan has various test setups and module loads specific to the system. In this example, we will be running Darshan on a CRAY machine so we will need to edit the test scripts within ``darshan-test/regression/cray-module-nersc``.

.. note::

  A list of other darshan test setups can be found in the ``darshan-test/regression`` directory. 

.. code-block:: RST
  
  cd <darshan-prefix>/darshan/darshan-test/regression
  vi cray-module-nersc/runjob.sh
  
  # inside "runjob.sh"
  sbatch --wait -N 1 -t 10 -p <name-of-partition> $NODE_CONSTRAINTS --output $DARSHAN_TMP/$$-tmp.out --error $DARSHAN_TMP/$$-tmp.err    $DARSHAN_TESTDIR/$DARSHAN_PLATFORM/slurm-submit.sl "$@"
  

Run An LDMS Streams Daemon
--------------------------
This section will go over how to start and configure a simple LDMS Streams deamon to collect the Darshan data and store to a CSV file. 
If an LDMS Streams daemon is already running on the system then please skip to the next section `Execute The Test Script(s)`_.

* First, initialize an ldms streams daemon on a compute node as follows:
.. code-block:: RST

  salloc -N 1 --time=2:00:00 -p <partition-name>
  *ssh to node*

* Once on the compute node (interactive session), create a file called **"hello\_stream\_store.conf"** and add the following content to it:

.. code-block:: RST
  
  load name=hello_sampler
  config name=hello_sampler producer=${HOSTNAME} instance=${HOSTNAME}/hello_sampler stream=darshanConnector component_id=${COMPONENT_ID}
  start name=hello_sampler interval=${SAMPLE_INTERVAL} offset=${SAMPLE_OFFSET}
  
  load name=stream_csv_store
  config name=stream_csv_store path=./streams/store container=csv stream=darshanConnector

* Set up the environment for starting an LDMS daemon:
.. code-block:: RST

  TOP=<path-to-ldms-install> 
  export LD_LIBRARY_PATH="$TOP/lib/:$TOP/lib:$LD_LIBRARY_PATH"
  export LDMSD_PLUGIN_LIBPATH="$TOP/lib/ovis-ldms/"
  export ZAP_LIBPATH="$TOP/lib/ovis-ldms"
  export PATH="$TOP/sbin:$TOP/bin:$PATH"
  export PYTHONPATH="$TOP/lib/python2.7/site-packages/"
  export COMPONENT_ID="1"
  export SAMPLE_INTERVAL="1000000"
  export SAMPLE_OFFSET="0"
  export HOSTNAME="localhost"

.. note::
  
  LDMS must already be installed on the system or locally. If it is not, then please following the ``Getting The Source`` and ``Building The Source`` in the `LDMS Quickstart Guide <ldms-quickstart.rst>`_.   

*   Next, run the LDSM Streams daemon with the following command:
.. code-block:: RST

  ldmsd -x sock:10444 -c hello_stream_store.conf -l /tmp/hello_stream_store.log -v DEBUG -r ldmsd.pid

.. note::
  
  To check that the ldmsd daemon is connected running please run ``ps auwx | grep ldmsd | grep -v grep``, ``ldms_ls -h <host-name> -x sock -p <port-number> -a none -v`` or ``cat /tmp/hello_stream_store.log``. Where <host-name> is the node where the LDMS daemon exists and <port-number> is the port it is listening on.

Execute The Test Script(s)
--------------------------
This section gives a step by step on executing a simple Darshan test script with the LDMS Darshan Integration code.

* Once the test scripts have been checked and the LDMS daemon is running and connected, open another terminal window (login node) and make sure the environment variables listed and set the following environment variables before running an application test with the darshanConnector code:
.. code-block:: RST

  export LD_PRELOAD=<darshan-prefix>/darshan/build/install/lib/libdarshan.so
  export LD_LIBRARY_PATH=<darshan-prefix>/darshan/build/install/lib/
  
  #set env variables for ldms streams daemon testing
  export DARSHAN_LDMS_STREAM=darshanConnector
  export DARSHAN_LDMS_XPRT=sock
  export DARSHAN_LDMS_HOST=<host-name>
  export DARSHAN_LDMS_PORT=10444
  export DARSHAN_LDMS_AUTH=none
  
  # determine which modules we want to publish to ldms streams 
  #export DXT_ENABLE_LDMS= # posix and mpiio data will be collected
  #export MPIIO_ENABLE_LDMS= 
  #export POSIX_ENABLE_LDMS=  
  #export STDIO_ENABLE_LDMS=
  #export HDF5_ENABLE_LDMS= 

.. note:: 
  
  The <host-name> is set to the LDMS Streams daemon currently running (e.g. in this case it would be node1).
  
Single Test
///////////
* Run Darshan's example "mpi-io-test" program within ``/test-cases/src/`` by setting the following environment variables, go to ``darshan/darshan-test/regression/test-cases`` and execute this script.
.. code-block:: RST
  
  export DARSHAN_PATH=<darshan-prefix>/darshan/build/install
  export DARSHAN_TMP=darshan-ldms-output/
  export DARSHAN_PLATFORM=cray-module-nersc
  cd darshan/darshan-test/regression/test-cases
  ./mpi-io-test-dxt.sh

.. note::
  
  Make sure the LD_PRELOAD and all other DARSHAN_LDMS_* related variables are set and at least one of the *_ENABLE_LDMS variable is set. If not, no data will be collected by LDMS.

All Tests
//////////
* If you wish to run all of Darshan's test scripts then please use the ``run-all.sh`` script located in ```darshan/darshan-test/regression``` and run it with the following arguements:
.. code-block:: RST
  
  # run darshan tests
  cd <darshan-prefix>/darshan/darshan-test/regression/

  #set output directory
  DTDIR=darshan-ldms-output/
  rm -r $DTDIR
  ./run-all.sh <path-to-darshan-install> $DTDIR cray-module-nersc

.. note::

  Make sure the LD_PRELOAD and all other DARSHAN_LDMS_* related variables are set and at least one of the *_ENAbLE_LDMS variable is set. If not, no data will be collected by LDMS.

Check Results
-------------
LDMS Output
This section provides the expected output of an application run with the data published to LDMS streams daemon with a CSV storage plugin (see section `Run An LDMS Streams Daemon`_. 

* If you are publishing to a local streams daemon (compute or login nodes) to collect the Darshan data then please compare the generated csv file to the one shown below in this section. 

* If you are publishing to a system daemon that aggregates the data and stores to a Scalable Object Store (SOS), please skip this section and go to `sos-quickstart`_ for more information about viewing and accessing data from this database.

LDMS Log File
/////////////
*   Once the application has completed, run ``cat /tmp/hello_stream_store.log`` in the terminal window where the ldmsd is running (compute node). You should see a similar output to the one below.

.. code-block:: RST
  
  > cat /tmp/hello_stream_store.log
  Fri Feb 18 11:35:23 2022: INFO  : stream_type: JSON, msg: "{ "job_id":53023,"rank":3,"ProducerName":"nid00052","file":"darshan-output/mpi-io-test.tmp.dat","record_id":1601543006480890062,"module":"POSIX","type":"MET","max_byte":-1,"switches":-1,"flushes":-1,"cnt":1,"op":"opens_segment","seg":[{"data_set":"N/A","pt_sel":-1,"irreg_hslab":-1,"reg_hslab":-1,"ndims":-1,"npoints":-1,"off":-1,"len":-1,"dur":0.00,"timestamp":1645209323.082951}]}", msg_len: 401, entity: 0x155544084aa0

  Fri Feb 18 11:35:23 2022: INFO  : stream_type: JSON, msg: "{ "job_id":53023,"rank":3,"ProducerName":"nid00052","file":"N/A","record_id":1601543006480890062,"module":"POSIX","type":"MOD","max_byte":-1,"switches":-1,"flushes":-1,"cnt":1,"op":"closes_segment","seg":[{"data_set":"N/A","pt_sel":-1,"irreg_hslab":-1,"reg_hslab":-1,"ndims":-1,"npoints":-1,"off":-1,"len":-1,"dur":0.00,"timestamp":1645209323.083581}]}", msg_len: 353, entity: 0x155544083f60
  ...

CSV File
////////
* To view the data stored in the generated CSV file from the streams store plugin, kill the ldmsd daemon first by running: ``killall ldmsd``
* Then ``cat`` the file in which the CSV file is located. Below is the stored DXT module data from LDMS's streams\_csv_\_store plugin for the ``mpi-io-test-dxt.sh`` test case.

.. code-block:: RST

  #module,uid,ProducerName,switches,file,rank,flushes,record_id,exe,max_byte,type,job_id,op,cnt,seg:off,seg:pt_sel,seg:dur,seg:len,seg:ndims,seg:reg_hslab,seg:irreg_hslab,seg:data_set,seg:npoints,seg:timestamp,seg:total,seg:start    
  POSIX,99066,n9,-1,darshan-ldms-output/mpi-io-test_lC.tmp.out,278,-1,9.22337E+18,darshan-ldms-output/mpi-io-test,-1,MET,10697754,open,1,-1,-1,0.007415,-1,-1,-1,-1,N/A,-1,1662576527,0.007415,0.298313
  MPIIO,99066,n9,-1,/lustre/spwalto/darshan-ldms-output/mpi-io-test_lC.tmp.out,278,-1,9.22337E+18,/lustre/spwalto/darshan-ldms-output/mpi-io-test,-1,MET,10697754,open,1,-1,-1,0.100397,-1,-1,-1,-1,N/A,-1,1662576527,0.100397,0.209427
  POSIX,99066,n11,-1,/lustre/spwalto/darshan-ldms-output/mpi-io-test_lC.tmp.out,339,-1,9.22337E+18,/lustre/spwalto/darshan-ldms-output/mpi-io-test,-1,MET,10697754,open,1,-1,-1,0.00742,-1,-1,-1,-1,N/A,-1,1662576527,0.00742,0.297529
  POSIX,99066,n6,-1,/lustre/spwalto/darshan-ldms-output/mpi-io-test_lC.tmp.out,184,-1,9.22337E+18,/lustre/spwalto/darshan-ldms-output/mpi-io-test,-1,MET,10697754,open,1,-1,-1,0.007375,-1,-1,-1,-1,N/A,-1,1662576527,0.007375,0.295111
  POSIX,99066,n14,-1,/lustre/spwalto/darshan-ldms-output/mpi-io-test_lC.tmp.out,437,-1,9.22337E+18,/lustre/spwalto/darshan-ldms-output/mpi-io-test,-1,MET,10697754,open,1,-1,-1,0.007418,-1,-1,-1,-1,N/A,-1,1662576527,0.007418,0.296812
  POSIX,99066,n7,-1,/lustre/spwalto/darshan-ldms-output/mpi-io-test_lC.tmp.out,192,-1,9.22337E+18,/lustre/spwalto/darshan-ldms-output/mpi-io-test,-1,MET,10697754,open,1,-1,-1,0.007435,-1,-1,-1,-1,N/A,-1,1662576527,0.007435,0.294776
  MPIIO,99066,n7,-1,/lustre/spwalto/darshan-ldms-output/mpi-io-test_lC.tmp.out,192,-1,9.22337E+18,/lustre/spwalto/darshan-ldms-output/mpi-io-test,-1,MET,10697754,open,1,-1,-1,0.033042,-1,-1,-1,-1,N/A,-1,1662576527,0.033042,0.273251
  ...

Kokkos
***********************
* Appropriate Kokkos function calls must be included in the application code. Add the following environmental variables to your run script to push Kokkos data from the application to stream for collection.

.. code-block:: RST

  export KOKKOS_LDMS_HOST="localhost" 
  export KOKKOS_LDMS_PORT="412" 
  export KOKKOS_PROFILE_LIBRARY="<insert install directory>/ovis/kokkosConnector/src/kp_sampler.so;<insert install directory>/ovis/kokkosConnector/src/kp_kernel_ldms.so"
  export KOKKOS_SAMPLER_RATE=101
  export KOKKOS_LDMS_VERBOSE=0
  export KOKKOS_LDMS_AUTH="munge"
  export KOKKOS_LDMS_XPRT="sock"
  
* The KOKKOS_SAMPLER_RATE variable determines the rate of messages pushed to streams and collected. Please note that it is in best practice to set this to a prime number to avoid collecting information from the same kernels.
* The KOKKOS_LDMS_VERBOSE variable can be set to 1 for debug purposes which prints all collected kernel data to the console.

How to make a data connector
***********************
Defining a format
***********************
