Streams-enabled Application Data Collectors
######################
Caliper
***********
DARSHAN
**************
Kokkos
**************  
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
****************
Defining a format
*****************
