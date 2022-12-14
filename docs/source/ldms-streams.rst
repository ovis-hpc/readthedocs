Streams-enabled Application Data Collectors
###########################

Caliper
***********************

DARSHAN
***********************
This section covers basics steps on how to compile, build and use the Darshan-LDMS Integration code (i.e. darshanConnector). The following application tests are part of the Darshan program and can be found under ``<darshan-prefix>/darshan/darshan-test/regression/test-cases/src/``. 

.. note::
  
  LDMS must already be installed on the system or locally. If it is not, then please following ``Getting The Source`` and ``Building The Source`` in the `LDMS Quickstart Guide <ldms-quickstart.rst>`_.

Compile and Build with LDMS
---------------------------
* Run the following to build Darshan and link against an existing LDMS library on the system.
  
.. code-block:: RST
  
  git clone https://github.com/darshan-hpc/darshan.git
  module swap PrgEnv-intel/6.0.9 PrgEnv-gnu # depending on the system. 
  cd <darshan-prefix>/darshan/ && mkdir build/
  ./prepare.sh && cd build/
  ../configure --with-log-path=<darshan-prefix>/darshan/build/logs --prefix=<darshan-prefix>/darshan/build/install --with-jobid-env=PBS_JOBID CC=cc --with-ldms=<path_to_ldms_install> 
  make && make install
.. note::
  
  This configuration is specific to the system (i.e. in this case we compile with cc instead of mpicc). For more information on how to install and build the code across various platforms, please visit `Darshan's Runtime Installation Page <https://www.mcs.anl.gov/research/projects/darshan/docs/darshan-runtime.html>`_ 
  
* To build HDF5 module for darshan, you must first load the module with ``module load cray-hdf5-parallel`` then run configure as follows: 
.. code-block:: RST

  ../configure --with-log-path=<darshan-prefix>/darshan/build/logs --prefix=<darshan-prefix>/darshan/build/install --with-jobid-env=PBS_JOBID CC=cc --with-ldms=/projects/ovis/darshanConnector/ovis/LDMS_install --enable-hdf5-mod --with-hdf5=<path-to-hdf5-install>  
  make && make install

If you do not have HDF5 installed on your system, install this with:

.. code-block:: RST
  
  sudo apt-get install -y hdf5-tools libhdf5-openmpi-dev openmpi-bin
  # we need to build h5py with the system HDF5 lib backend
  export HDF5_MPI="ON"
  CC=cc python -m pip install --no-binary=h5py h5py

.. note::
  
  If the HDF5 library is installed this way, you do not need to include the ``--with-hdf5`` flag during configuration. For more information on other methods and HDF5 versions to install, please visit `Darshan's Runtime Installation Page <https://www.mcs.anl.gov/research/projects/darshan/docs/darshan-runtime.html>`_.
  
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

* Once on the compute node (interactive session), set up the environment for starting an LDMS daemon:
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
  
  LDMS must already be installed on the system or locally. If it is not, then please following ``Getting The Source`` and ``Building The Source`` in the `LDMS Quickstart Guide <ldms-quickstart.rst>`_. 

* Next, create a file called **"darshan\_stream\_store.conf"** and add the following content to it:

.. code-block:: RST
  
  load name=hello_sampler
  config name=hello_sampler producer=${HOSTNAME} instance=${HOSTNAME}/hello_sampler stream=darshanConnector component_id=${COMPONENT_ID}
  start name=hello_sampler interval=${SAMPLE_INTERVAL} offset=${SAMPLE_OFFSET}
  
  load name=stream_csv_store
  config name=stream_csv_store path=./streams/store container=csv stream=darshanConnector rolltype=3 rollover=500000  

*   Next, run the LDSM Streams daemon with the following command:
.. code-block:: RST

  ldmsd -x sock:10444 -c darshan_stream_store.conf -l /tmp/darshan_stream_store.log -v DEBUG -r ldmsd.pid

.. note::
  
  To check that the ldmsd daemon is connected running please run ``ps auwx | grep ldmsd | grep -v grep``, ``ldms_ls -h <host-name> -x sock -p <port-number> -a none -v`` or ``cat /tmp/darshan_stream_store.log``. Where <host-name> is the node where the LDMS daemon exists and <port-number> is the port it is listening on.

Execute The Test Script(s)
--------------------------
This section gives a step by step on executing a simple Darshan test script with the LDMS Darshan Integration code (e.g. darshanConnector).

* Once the test scripts have been checked and the LDMS daemon is running and connected, **open another terminal window (login node)** and make sure the environment variables listed and set the following environment variables before running an application test with the darshanConnector code:
.. code-block:: RST

  export LD_PRELOAD=<darshan-prefix>/darshan/build/install/lib/libdarshan.so
  export LD_LIBRARY_PATH=<darshan-prefix>/darshan/build/install/lib/
  export HDF5_LIB=<path-to-hdf5-shared-libary-file>/libhdf5.so
  export DXT_ENABLE_IO_TRACE=1 # optional
  
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
  
  The ``<host-name>`` is set to the node name the LDMS Streams daemon is running on (e.g. the node we previous ssh'd into).
  
Single Test
///////////
* Run Darshan's example "mpi-io-test" program within ``/test-cases/src/`` by setting the following environment variables, go to ``darshan/darshan-test/regression/test-cases`` and execute this script.
.. code-block:: RST
  
  export DARSHAN_PATH=<darshan-prefix>/darshan/build/install
  export DARSHAN_TMP=/tmp/darshan-ldms-output/
  export DARSHAN_PLATFORM=cray-module-nersc
  cd darshan/darshan-test/regression/test-cases
  ./mpi-io-test-dxt.sh

.. note::
  
  Make sure the LD_PRELOAD and all other DARSHAN_LDMS_* related variables are set and at least one of the *_ENABLE_LDMS variable is set. If not, no data will be collected by LDMS. 
  **(Optional)** To collect the correct job_id by Darshan and LDMS, please export the environment variable ``PBS_JOBID`` to $SLURM_JOB_ID in ``<darshan-prefix>/darshan-test/regression/cray-module-nersc/slurm-submit.sl``. If this is not set, the job_id field will be set to the first PID.   

All Tests
//////////
* If you wish to run all of Darshan's test scripts then please use the ``run-all.sh`` script located in ``darshan/darshan-test/regression`` and run it with the following arguements:
.. code-block:: RST
  
  # run darshan tests
  cd <darshan-prefix>/darshan/darshan-test/regression/

  #set output directory
  DTDIR=darshan-ldms-output/
  rm -r $DTDIR
  ./run-all.sh <path-to-darshan-install> $DTDIR cray-module-nersc

.. note::

  Make sure the LD_PRELOAD and all other DARSHAN_LDMS_* related variables are set and at least one of the *_ENABLE_LDMS variable is set. If not, no data will be collected by LDMS.
  
Run Single Test On Login Node 
------------------------------
If you are not installing the darshanConnector code on cluster, please run the following commands to do run a single Darshan test case on the login node.

1. Set Environment Variables for Darshan, LDMS and Darshan-LDMS Integrated code (i.e. darshanConnector).

.. code-block:: RST
  
  # Darshan
  export DARSHAN_PATH=<darshan-prefix>/darshan/build/install
  export LD_PRELOAD=$DARSHAN_PATH/lib/libdarshan.so
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DARSHAN_PATH/lib
  export HDF5_LIB=<path-to-hdf5-shared-library>/libhdf5.so
  export DXT_ENABLE_IO_TRACE=1 #optional
  
  # LDMS
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
  
  # darshanConnector
  export DARSHAN_LDMS_STREAM=darshanConnector
  export DARSHAN_LDMS_XPRT=sock
  export DARSHAN_LDMS_HOST=<host-name>
  export DARSHAN_LDMS_PORT=10444
  export DARSHAN_LDMS_AUTH=none
  # determine which modules we want to publish to ldms streams 
  export DXT_ENABLE_LDMS= # posix and mpiio data will be collected
  #export MPIIO_ENABLE_LDMS= 
  #export POSIX_ENABLE_LDMS=  
  #export STDIO_ENABLE_LDMS=
  #export HDF5_ENABLE_LDMS= 

2. Generate the LDMSD Configuration File and Start the Daemon

.. code-block:: RST  

  cat > darshan_stream_store.conf << EOF
  load name=hello_sampler
  config name=hello_sampler producer=${HOSTNAME} instance=${HOSTNAME}/hello_sampler stream=darshanConnector component_id=${COMPONENT_ID}
  start name=hello_sampler interval=${SAMPLE_INTERVAL} offset=${SAMPLE_OFFSET}
  
  load name=stream_csv_store
  config name=stream_csv_store path=./streams/store container=csv stream=darshanConnector rolltype=3 rollover=500000
  EOF

  ldmsd -x sock:10444 -c darshan_stream_store.conf -l /tmp/darshan_stream_store.log -v DEBUG
  # check daemon is running
  ldms_ls -p 10444 -h localhost -v
  
3. Set Up Test Case Variables

.. code-block:: RST 

  export PROG=mpi-io-test
  export DARSHAN_TMP=/tmp/darshan-ldms-output/
  export DARSHAN_TESTDIR=$PWD/darshan/darshan-test/regression
  export DARSHAN_LOGFILE=$DARSHAN_TMP/${PROG}.darshan
 
4. **(Optional)** Generate TMP Path if it doesn't exist

.. code-block:: RST 

  if [ ! -d $DARSHAN_TMP ]; then
       mkdir -p $DARSHAN_TMP
  fi
  
5. Run Darshan's mpi-io-test.c program

.. code-block:: RST 

  cc $DARSHAN_TESTDIR/test-cases/src/${PROG}.c -o $DARSHAN_TMP/${PROG}
  cd $DARSHAN_TMP
  ./${PROG} -f $DARSHAN_TMP/${PROG}.tmp.dat

6. **(Optional)** Parse the Darshan binary file using Darshans standard and DXT (only if DXT_ENABLE_IO_TRACE is enabled) parsers.

.. code-block:: RST 

  $DARSHAN_PATH/bin/darshan-parser --all $DARSHAN_LOGFILE > $DARSHAN_TMP/${PROG}.darshan.txt
  $DARSHAN_PATH/bin/darshan-dxt-parser --show-incomplete $DARSHAN_LOGFILE > $DARSHAN_TMP/${PROG}-dxt.darshan.txt      
  
Check Results
-------------
LDMS Output
////////////
This section provides the expected output of an application run with the data published to LDMS streams daemon with a CSV storage plugin (see section `Run An LDMS Streams Daemon`_). 

* If you are publishing to a local streams daemon (compute or login nodes) to collect the Darshan data then please compare the generated csv file to the one shown below in this section. 

* If you are publishing to a system daemon that aggregates the data and stores to a Scalable Object Store (SOS), please skip this section and go to the `SOS Quickstart Guide <sos-quickstart.rst>`_ for more information about viewing and accessing data from this database.

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

Compare With Darshan Log File(s)
////////////////////////////////
If you decided to parse Darshan's binary file from ``step 6`` in _`Run Test On Login Node`_ section, you can view the log(s) with ``cat $DARSHAN_TMP/${PROG}.darshan.txt`` or ``cat $DARSHAN_TMP/${PROG}-dxt.darshan.txt`` and compare them to the data collected by LDMS. 

If the data is correct, the producerName, file path and record_id for each Module (i.e. POSIX, MPIIO, etc.) will be the same.


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

How To Make A Data Connector
*****************************
In order to create a data connector with LDMS to collect runtime timeseries application data, you will need to utilize LDMS's Streams Functionality. This section will provide the necessary functions and Streams API required to make the data connector.

The example (code) below is pulled from the Darshan-LDMS Integration code.  

.. note::
  
  The LDMS Streams functionality uses a push-based method to reduce memory consumed and data loss on the node.

Initialize All Necessary Variables
-----------------------------------

* First, the following variables will need to be initialized globally or accessible by the Streams API Functions described in the next section:

.. code-block:: RST 

  #define SLURM_NOTIFY_TIMEOUT 5
  ldms_t ldms_g;
  pthread_mutex_t ln_lock;
  int conn_status, to;
  ldms_t ldms_darsh;
  sem_t conn_sem;
  sem_t recv_sem;


Copy "Hello Sampler" Streams API Functions
------------------------------------------
Next, copy the ``ldms_t setup_connection`` and ``static void event_cb`` functions listed below. These functions originated from the `ldmsd_stream_subscribe.c <https://github.com/ovis-hpc/ovis/blob/OVIS-4/ldms/src/ldmsd/test/ldmsd_stream_subscribe.c>`_ code. 

The ``setup_connection`` contains LDMS API calls that connects to the LDMS daemon and the  ``static void event_cb`` is a callback function to check the connection status of the LDMS Daemon.

.. code-block:: RST

  static void event_cb(ldms_t x, ldms_xprt_event_t e, void *cb_arg)
  {
          switch (e->type) {
          case LDMS_XPRT_EVENT_CONNECTED:
                  sem_post(&conn_sem);
                  conn_status = 0;
                  break;
          case LDMS_XPRT_EVENT_REJECTED:
                  ldms_xprt_put(x);
                  conn_status = ECONNREFUSED;
                  break;
          case LDMS_XPRT_EVENT_DISCONNECTED:
                  ldms_xprt_put(x);
                  conn_status = ENOTCONN;
                  break;
          case LDMS_XPRT_EVENT_ERROR:
                  conn_status = ECONNREFUSED;
                  break;
          case LDMS_XPRT_EVENT_RECV:
                  sem_post(&dC.recv_sem);
                  break;
          case LDMS_XPRT_EVENT_SEND_COMPLETE:
                  break;
          default:
                  printf("Received invalid event type %d\n", e->type);
          }
  }

  ldms_t setup_connection(const char *xprt, const char *host,
                          const char *port, const char *auth)
  {
          char hostname[PATH_MAX];
          const char *timeout = "5";
          int rc;
          struct timespec ts;

          if (!host) {
                  if (0 == gethostname(hostname, sizeof(hostname)))
                          host = hostname;
          }
          if (!timeout) {
                  ts.tv_sec = time(NULL) + 5;
                  ts.tv_nsec = 0;
          } else {
                  int to = atoi(timeout);
                  if (to <= 0)
                          to = 5;
                  ts.tv_sec = time(NULL) + to;
                  ts.tv_nsec = 0;
          }

          ldms_g = ldms_xprt_new_with_auth(xprt, NULL, auth, NULL);
          if (!ldms_g) {
                  printf("Error %d creating the '%s' transport\n",
                         errno, xprt);
                  return NULL;
          }

          sem_init(recv_sem, 1, 0);
          sem_init(conn_sem, 1, 0);

          rc = ldms_xprt_connect_by_name(ldms_g, host, port, event_cb, NULL);
          if (rc) {
                  printf("Error %d connecting to %s:%s\n",
                         rc, host, port);
                  return NULL;
          }
          sem_timedwait(conn_sem, &ts);
          if (conn_status)
                  return NULL;
          return ldms_g;
  }

Initialize and Connect to LDMSD
------------------------------------------
Once the above functions have been copied, the ``setup_connection`` will need to be called in order to establish a connection an LDMS Streams Daemon.

.. note::
  
  The LDMS Daemon is configured with the  `Streams Plugin <https://github.com/ovis-hpc/ovis/blob/OVIS-4/ldms/src/sampler/hello_stream/Plugin_hello_sampler.man>`_ and should already be running on the node. The host is set to the node the daemon is running on and port is set to the port the daemon is listening to. 

.. code-block:: RST

  void darshan_ldms_connector_initialize()
  {
      const char* env_ldms_stream =  getenv("DARSHAN_LDMS_STREAM");
      const char* env_ldms_xprt    = getenv("DARSHAN_LDMS_XPRT");
      const char* env_ldms_host    = getenv("DARSHAN_LDMS_HOST");
      const char* env_ldms_port    = getenv("DARSHAN_LDMS_PORT");
      const char* env_ldms_auth    = getenv("DARSHAN_LDMS_AUTH");

      /* Check/set LDMS transport type */
      if (!env_ldms_xprt || !env_ldms_host || !env_ldms_port || !env_ldms_auth || env_ldms_stream){
          printf("Either the transport, host, port or authentication is not given\n");
          return;
      }

      pthread_mutex_lock(ln_lock);
      ldms_darsh = setup_connection(env_ldms_xprt, env_ldms_host, env_ldms_port, env_ldms_auth);
          if (conn_status != 0) {
              printf("Error setting up connection to LDMS streams daemon: %i -- exiting\n", conn_status);
              pthread_mutex_unlock(ln_lock);
              return;
          }
          else if (ldms_darsh->disconnected){
              printf("Disconnected from LDMS streams daemon -- exiting\n");
              pthread_mutex_unlock(ln_lock);
              return;
          }
      pthread_mutex_unlock(ln_lock);
      return;
  }
  
The environment variables ``DARSHAN_LDMS_X`` are used to define the stream name (configured in the daemon), transport type (sock, ugni, etc.), host, port and authentication of the LDMSD. In this specific example, the stream name is set to "darshanConnector" so the environment variable, ``DARSHAN_LDMS_STREAM`` is exported as follows: ``export DARSHAN_LDMS_STREAM=darshanConnector``

.. note::
   The environment variables are not required. The stream, transport, host, port and authentication can be initialized and set within in the code.

Publish Event Data to LDMSD
-------------------------------------
Now we will create a function that will collect all relevent application events and publish to the LDMS Streams Daemon. In the Darshan-LDMS Integration, the following Darshan's I/O traces for each I/O event (i.e. open, close, read, write) are collected along with the absolute timestamp (for timeseries data) for each I/O event:

.. code-block:: RST

  void darshan_ldms_connector_send(int64_t record_count, char *rwo, int64_t offset, int64_t length, int64_t max_byte, int64_t rw_switch, int64_t flushes,  double start_time, double end_time, struct timespec tspec_start, struct timespec tspec_end, double total_time, char *mod_name, char *data_type)
  {
      char jb11[1024];
      int rc, ret, i, size, exists;
      env_ldms_stream  = getenv("DARSHAN_LDMS_STREAM");

      pthread_mutex_lock(ln_lock);
      if (ldms_darsh != NULL)
          exists = 1;
      else
          exists = 0;
      pthread_mutex_unlock(ln_lock);

      if (!exists){
          return;
      }

      sprintf(jb11,"{ \"uid\":%ld, \"exe\":\"%s\",\"job_id\":%ld,\"rank\":%ld,\"ProducerName\":\"%s\",\"file\":\"%s\",\"record_id\":%"PRIu64",\"module\":\"%s\",\"type\":\"%s\",\"max_byte\":%ld,\"switches\":%ld,\"flushes\":%ld,\"cnt\":%ld,\"op\":\"%s\",\"seg\":[{\"data_set\":\"%s\",\"pt_sel\":%ld,\"irreg_hslab\":%ld,\"reg_hslab\":%ld,\"ndims\":%ld,\"npoints\":%ld,\"off\":%ld,\"len\":%ld,\"start\":%0.6f,\"dur\":%0.6f,\"total\":%.6f,\"timestamp\":%lu.%.6lu}]}", dC.uid, dC.exename, dC.jobid, dC.rank, dC.hname, dC.filename, dC.record_id, mod_name, data_type, max_byte, rw_switch, flushes, record_count, rwo, dC.data_set, dC.hdf5_data[0], dC.hdf5_data[1], dC.hdf5_data[2], dC.hdf5_data[3], dC.hdf5_data[4], offset, length, start_time, end_time-start_time, total_time, tspec_end.tv_sec, micro_s);

      rc = ldmsd_stream_publish(ldms_darsh, env_ldms_stream, LDMSD_STREAM_JSON, jb11, strlen(jb11) + 1);
      if (rc)
          printf("Error %d publishing data.\n", rc);

   out_1:
      return;
  }
  
.. note::

  For more information about the various Darshan I/O traces and metrics collected, please visit `Darshan's Runtime Installation Page <https://www.mcs.anl.gov/research/projects/darshan/docs/darshan-runtime.html>`_ and `Darshan LDMS Metrics Collected <https://github.com/Snell1224/darshan/wiki/Darshan-LDMS---Metric-Definitions>`_ pages.

Once this function is called, it initializes a connection to the LDMS Streams Daemon, attempts reconnection if the connection is not established, then formats the given arguements/variables into a JSON message format and finally publishes to the LDMS Streams Deamon.

There are various types of formats that can be used to publish the data (i.e. JSON, string, etc.) so please review the `Defining A Format`_ section for more information.

Collect Event Data 
/////////////////////////

To collect the application data in real time (and using the example given in this section), the ``void darshan_ldms_connector_send(arg1, arg2, arg3,....)`` will be placed in all sections of the code where we want to publish a message. From the Darshan-LDMS Integration code we would have:

.. code-block:: RST

  darshan_ldms_connector_send(rec_ref->file_rec->counters[MPIIO_COLL_OPENS] + rec_ref->file_rec->counters[MPIIO_INDEP_OPENS], "open", -1, -1, -1, -1, -1, __tm1, __tm2, __ts1, __ts2, rec_ref->file_rec->fcounters[MPIIO_F_META_TIME], "MPIIO", "MET");
  
This line of code is placed within multiple macros (`MPIIO_RECORD_OPEN/READ/WRITE <https://github.com/darshan-hpc/darshan/blob/main/darshan-runtime/lib/darshan-mpiio.c>`_) in Darshan's MPIIO module. 

* Doing this will call the function everytime Darshan detects an I/O event from the application (i.e. read, write, open, close). Once called, the arguements will be passed to the function, added to the JSON formatted message and pushed to the LDMS daemon.

.. note:: 
  
  For more information about how to store the published data from and LDMS Streams Daemon, please see the `Stream CSV Store plugin man pages <https://github.com/ovis-hpc/ovis/blob/OVIS-4/ldms/src/store/stream/Plugin_stream_csv_store.man>`_




Defining A Format
***********************
