DSOS Quickstart
####################

Introduction
***************

The Distributed Scalable Object Store (DSOS) (pronounced "dee-sôs") is a layer on top of SOS to enable distributed, parallel ingests and queries. DSOS is intended to be used to use SOS databases across multiple devices as a unified database. Users setup a file, referred to as the cluster configuration file in this context, which names all of the nodes where a SOS database is expected. Using python API or the command line interface dsosql, users can query these SOS databases for data in the same schema. DSOS interfaces are installed alongside SOS, starting with SOS v4, with no additional enable arguments required.

Dsosql
********

For demonstration purposes, let's assume we have two nodes, node1 ande node2, with a SOS database at /storage/sos/database. 
Our cluster configuration file, let's call it dsos.conf, would simply be

.. code-block:: console

  node1
  node2

Dsosql expects the path to this dsos.conf and the database path for correct functionality. These can be entered as options in to dsosql using the -a and -o options, respectively. They can also be entered after dropping into the dsosql shell, like ldmsd_controller, commands to dsosql can be entered after going into a shell or by echo'ing them into the utility. 

.. code-block:: console

  >dsosql -a dsos.conf -o /storage/sos/database
  Attaching to cluster dsos.conf ... OK
  Opening the container /storage/sos/database ... OK
  dsosql: show_part regex .*
  Name                     Description                                   UID      GID Permission
  ------------------------ ---------------------------------------- -------- -------- -------------
  default                  default                                  33       33       -rw-rw---

  #or

  >dsosql
  dsosql: attach path dsos.conf
  Attaching to cluster dsos.conf ... OK
  dsosql: open path /storage/sos/database
  Opening the container /storage/sos/database ... OK
  dsosql: show_part regex .*
  Name                     Description                                   UID      GID Permission
  ------------------------ ---------------------------------------- -------- -------- -------------
  default                  default                                  33       33       -rw-rw---


  >echo "show_part regex .*" | dsosql -a dsos.conf -o /storage/sos/database
  Attaching to cluster dsos.conf ... OK
  Opening the container /storage/sos/database ... OK
  Name                     Description                                   UID      GID Permission
  ------------------------ ---------------------------------------- -------- -------- -------------
  default                  default                                  33       33       -rw-rw---

Commands available in dsosql are attach, create_part, create_schema, help, import, open, select, set, show, show_part, and show_schema. 


Python API
**********

Like dsosql, python expects a dsos.conf path and a database path. A Sos.Session object is initialized, opened, and then a query setup to begin querying data out of the database. The query initialization expects a max rows returned value for the resultant data object, which will be a pandas DataFrame with columns consisting of the metrics queried and the metrics comprising the index queried. The max rows, or query block size, can typically be set at 1024*1024 though changing block sizes will affect performance.

.. code-block:: python

    import pandas as pd
    from sosdb import Sos
    sess = Sos.Session("dsos.conf")
    cont = sess.open("/storage/sos/database")
    query = cont.query(1024*1024)
    query.select('select Active from meminfo') 
