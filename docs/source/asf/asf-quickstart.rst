AppSysFusion Quick Start
==================================================================

Dashboard Development
----------------------

Creating a New Dashboard
////////////////////////

The Grafana interface can be accessed at <URL>. To create a new dashboard, click on the + sign on the left side of the home page and hit dashboard. This will create a blank dashboard with an empty panel in it. Panels can be thought of as a visualization of a single query. Hit the add query button on the panel to begin configuring the query to be sent to an analysis module. 

.. note::
  
  For more information on how to navigate around the Grafana dashboard and what the variables and advanced settings do, please see :doc:`Grafana Panel <grafanapanel>` and :doc:`Grafana Usage <grafanause>`

Analysis Development
----------------------
Analysis I/O 
////////////////////////
An analysis module is a python script and has a general template. There is a class, which must be called the same name as the python script itself, and two class functions: ``__init__`` and ``get_data``. The module is first initialized and then ``get_data`` is called. This should return a pandas DataFrame or a NumSOS DataSet (preferably the former if you are using python3). Below are the variables passed from the Grafana interface to these class functions. 

``__init__``
  * ``cont`` - A Sos.Container object which contains the path information to the SOS container specified in the Grafana query
  * ``start`` - The beginning of the time range of the Grafana query (in epoch time).
  * ``end`` - The end of the time range of the Grafana query (in epoch time).
  * ``schema`` - The LDMS schema specified by the Grafana query.
  * ``maxDataPoints`` - the maximum number of points that Grafana can display on the user's screen. 

``get_data``
  * ``metrics`` - a python list of metrics specified by the Grafana query.
  * ``job_id`` - a string of the job_id specified by the Grafana query. 
  * ``user_name`` - a string of the user name specified by the Grafana query.
  * ``params`` - a string of the extra parameters specified by the Grafana query.

Querying The Database
///////////////////////
This section goes over how to query from the database as a user. Below is a basic analysis that simply queries the database and returns the DataFrame of the metrics passed in along with the timestamp for each metric. If a job ID or user name is specified, those are used to filter the query further. The standard query looks for data between the Grafana start and end timestamps. 

.. note::

  ``job_id`` and ``user_name`` must exist in the schema passed in for this code to work. 

In the ``__init__`` function, we simply set most things to be self variables to access them later in the get_data. Importantly, we setup a variable called self.src which is a SosDataSource python object (coming from numsos). We config self.src to point to our container and will later use it to query and return data from the database.

In the ``get_data`` function we create variables that will be used for the ``self.src`` query. These variables consist of:

* ``where_`` - An array of lists, which acts as the query filter. You can also append additional filters to the ``where_ array`` based on if ``job_id`` or ``user_name`` are set. 
* ``orderby`` - This defines the index that will be used when querying the database. The standard setting is 'time_job_comp' and shown in the example below. 

.. note:: 

  Our SOS databases are setup to use permutations of timestamps, job IDs, and component IDs as multi-indices. Depending on your filter, you may want to use a different multi-index (e.g. ``time_comp_job``, ``comp_time_job``, etc.). The standard index setting is ``time_job_comp``.

analysisTemplate.py:

.. code:: RST

  import os, sys, traceback
  import datetime as dt
  from graf_analysis.grafanaAnalysis import Analysis
  from numsos.DataSource import SosDataSource
  from numsos.Transform import Transform
  from sosdb.DataSet import DataSet
  from sosdb import Sos
  import pandas as pd
  import numpy as np
   
  class analysisTemplate(Analysis):
      def __init__(self, cont, start, end, schema='job_id', maxDataPoints=4096):
          self.schema = schema
          self.src = SosDataSource()
          self.src.config(cont=cont)
          self.start = start
          self.end = end
          self.maxDataPoints = maxDataPoints
   
      def get_data(self, metrics, job_id=0, user_name=None, params=None):
          where_ = [ [ 'timestamp', Sos.COND_GE, self.start ],
                     [ 'timestamp', Sos.COND_LE, self.end ]
              ]
          if job_id != 0:
              where_.append([ 'job_id', Sos.COND_EQ, job_id])
          if self.user_name != None:
              where_.append([ 'user_name', Sos.COND_EQ, user_name])
          orderby = 'time_job_comp'
          try:
              self.src.select(metrics + ['timestamp'],
                         from_ = [ self.schema ],
                         where = where_,
                         order_by = orderby
                  )
              df = self.src.get_df()
              return df
          except Exception as e:
              a, b, c = sys.exc_info()
              print(str(e)+' '+str(c.tb_lineno))

.. note:: 
  
  If you want to use this analysis module in a Grafana dashboard, you will need to ask your administrator to copy your new analysis module(s) into the directory that Grafana points to. This is because Grafana is setup to look at a specific path directory to query from. 

You do not need to query from the Grafana interface to test your module. Below is a simple code which mimics the Grafana pipeline and prints the JSON returned to Grafana. 
If you wish to find a username based on another metric listed in the schema "jobid", just include "job_id=<job_id number>" to the get_data function. 

First, you will need to set your path and pythonpath environment variables with the following:

.. code::

  #!/usr/bin/python
   
  import time,sys
  from sosdb import Sos
  from grafanaFormatter import DataFormatter
  from table_formatter import table_formatter
  from time_series_formatter import time_series_formatter
  from analysisTemplate import analysisTemplate
   
  cont = Sos.Container('<path-to-container>')
  model = analysisTemplate(cont, time.time()- 3600, time.time(), schema='jobid')
  data = model.get_data(['username'])
  #fmt = time_series_formatter(data)
  # Use time_series or table formatter based on desired grafana display.
  # Time_series data must have timestamp as the first column in the df
  fmt = table_formatter(data)
  data = fmt.ret_json()
  print(data)

.. note::

  To make things easier, you can always populate an .sh file with this content and will only need to run ``source <pythonsetup.sh>``
  All imports are python scripts that need to reside in the same directory as the test analysis module in order for it to run successfully.  

Then, run the python script with the current python verion installed. In this case it would be ``python3 <analysisTemplate.py>``

Expected Results & Output
==========================
The following is an example test of an analysis module that queries the schema "job_id" and outputs the



