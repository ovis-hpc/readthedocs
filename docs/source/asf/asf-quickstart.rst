AppSysFusion Quick Start
==================================================================

Dashboard Development
----------------------

Creating a New Dashboard
////////////////////////

The Grafana interface can be accessed at <URL>. To create a new dashboard, click on the + sign on the left side of the home page and hit dashboard. This will create a blank dashboard with an empty panel in it. Panels can be thought of as a visualization of a single query. Hit the add query button on the panel to begin configuring the query to be sent to an analysis module. 

Dashboard Variables and Advanced Settings
/////////////////////////////////////////

<image here>

To edit the Grafana dashboard variables (listed at the top of the dashboard), you will need to refernce them with $ in front of each variable name. 

For example, to switch SOS containers you will need to create a variable called ``container`` and then putting ``$container`` in the ``container field`` of the query. 

To create variables, go to the dashboard settings (gear button at the top right) and go to variables. Here you can create new variables, change the dashboard name and folder location and load previously saved versions. Common variable types are text boxes, queries or a pre-populated list of options. Below are the queryable metrics information to put in the query field. 

* Container - select the custom option in the Type field and add the name of the container being used to query from in the custom options field.
* Schema - query=schema&container=<cont_name>
* Index - query=index&container=<cont_name>&schema=<schema_name>
* Metrics - query=metrics&container=<cont_name>&schema=<schema_name>
* Component IDs - query=components&container=<cont_name>&schema=<schema_name>
* Jobs - query=jobs&container=<cont_name>&schema=<schema_name>

You can put variables in queries as well. For example, if you already have a $container variable, you can set the schema variable query to be ``query=schema&container=$container``. Then the ``$schema`` variable can be used in other queries. 

.. note::
  
  Other than the container variable, all other variables bulleted above are set to query in the ``Type`` field.

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

Testing An Analysis Module
//////////////////////////
This section goes over how to test your python analysis module as a user. 

**If Grafana and SOS are already installed on your system then please skip the `Required Scripts`_ section** and ask your system administrator where these scripts reside on the system (usually under a "graf_analysis" folder). 

  * This way, you can copy all the necessary python scripts and modules located in this directory to your home directory (/home/<username>/<grafana_analysis>), delete any unnecessary scripts or folders, edit/modify your own set of scripts and create new ones.

If these python scripts or modules **do not exist on your system and you have no way of accessing them** then please continue to the `Required Scripts`_ section.

Required Scripts
=================
The following scripts are needed to run the python analysis module. If you are just starting out and do not have access to these existing scripts then please create them in the same directory as your python analysis module. 

.. note::
  
  If Grafana and SOS are installed on your system then please ask your system administator where these files reside on the system so that you can copy them to your home directory.

grafanaFormatter:

.. code:: RST
  
  from sosdb import Sos
  from sosdb.DataSet import DataSet
  import numpy as np
  import pandas as pd
  import copy
  
  class RowIter(object):
      def __init__(self, dataSet):
          self.dset = dataSet
          self.limit = dataSet.get_series_size()
          self.row_no = 0
  
      def __iter__(self):
          return self
  
      def cvt(self, value):
          if type(value) == np.datetime64:
              return [ value.astype(np.int64) / 1000 ]
          return value
  
      def __next__(self):
          if self.row_no >= self.limit:
              raise StopIteration
          res = [ self.cvt(self.dset[[col, self.row_no]]) for col in range(0, self.dset.series_count) ]
          self.row_no += 1
          return res
  
  class DataFormatter(object):
      def __init__(self, data):
           self.result = []
           self.data = data
           self.fmt = type(self.data).__module__
           self.fmt_data = {
               'sosdb.DataSet' : self.fmt_dataset,
               'pandas.core.frame' : self.fmt_dataframe,
               'builtins' : self.fmt_builtins
           }
  
      def ret_json(self):
           return self.fmt_data[self.fmt]()
  
      def fmt_dataset(self):
          pass
  
      def fmt_dataframe(self):
          pass
  
      def fmt_builtins(self):
          pass

table_formatter:

..code:: RST

  from graf_analysis.grafanaFormatter import DataFormatter, RowIter
  from sosdb.DataSet import DataSet
  from sosdb import Sos
  import numpy as np
  import pandas as pd
  import copy
  
  class table_formatter(DataFormatter):
      def fmt_dataset(self):
          # Format data from sosdb DataSet object
          if self.data is None:
              return {"columns" : [{ "text" : "No papi jobs in time range" }] }
  
          self.result = { "type" : "table" }
          self.result["columns"] = [ { "text" : colName } for colName in self.data.series ]
          rows = []
          for row in RowIter(self.data):
              rows.append(row)
          self.result["rows"] = rows
          return self.result
  
      def fmt_dataframe(self):
          if self.data is None:
              return {"columns" : [{ "text" : "No papi jobs in time range" }] }
  
          self.result = { "type" : "table" }
          self.result["columns"] = [ { "text" : colName } for colName in self.data.columns ]
          self.result["rows"] = self.data.to_numpy()
          return self.result
  
      def fmt_builtins(self):
          if self.data is None:
              return { "columns" : [], "rows" : [], "type" : "table" }
          else:
              return self.data

time_series_formatter:

..code:: RST
  
  from graf_analysis.grafanaFormatter import DataFormatter
  from sosdb.DataSet import DataSet
  from sosdb import Sos
  import numpy as np
  import pandas as pd
  import copy
  
  class time_series_formatter(DataFormatter):
      def fmt_dataset(self):
          # timestamp is always last series
          if self.data is None:
              return [ { "target" : "", "datapoints" : [] } ]
  
          for series in self.data.series:
              if series == 'timestamp':
                  continue
              ds = DataSet()
              ds.append_series(self.data, series_list=[series, 'timestamp'])
              plt_dict = { "target" : series }
              plt_dict['datapoints'] = ds.tolist()
              self.result.append(plt_dict)
              del ds
          return self.result
  
      def fmt_dataframe(self):
          if self.data is None:
              return [ { "target" : "", "datapoints" : [] } ]
  
          for series in self.data.columns:
              if series == 'timestamp':
                  continue
              plt_dict = { "target" : series }
              plt_dict['datapoints'] = self.fmt_datapoints([series, 'timestamp'])
              self.result.append(plt_dict)
          return self.result
  
      def fmt_datapoints(self, series):
          ''' Format dataframe to output expected by grafana '''
          aSet = []
          for row_no in range(0, len(self.data)):
              aRow = []
              for col in series:
                  v = self.data[col].values[row_no]
                  typ = type(v)
                  if typ.__module__ == 'builtins':
                      pass
                  elif typ == np.ndarray or typ == np.string_ or typ == np.str_:
                      v = str(v)
                  elif typ == np.float32 or typ == np.float64:
                      v = float(v)
                  elif typ == np.int64 or typ == np.uint64:
                      v = int(v)
                  elif typ == np.int32 or typ == np.uint32:
                      v = int(v)
                  elif typ == np.int16 or typ == np.uint16:
                      v = int(v)
                  elif typ == np.datetime64:
                      # convert to milliseconds from microseconds
                      v = v.astype(np.int64) / int(1e6)
                  else:
                      raise ValueError("Unrecognized numpy type {0}".format(typ))
                  aRow.append(v)
              aSet.append(aRow)
          return aSet
  
      def fmt_builtins(self):
          if self.data is None:
              return [ { "target" : "", "datapoints" : [] } ]
          else:
              return self.data

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



