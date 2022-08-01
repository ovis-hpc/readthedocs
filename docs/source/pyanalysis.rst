Python Analysis Creation
========================

Analysis I/O
-----------
An analysis module is a python script and has a general template. There is a class, which must be called the same name as the python script itself for the backend Django application to import it, and two class functions: __init__ and get_data. The module is first initialized and then get_data is called which should return a pandas DataFrame. Below are the variables passed from the Grafana interface to these class functions.

__init__

* cont: A Sos.Container object which contains the path information to the SOS container specified in the Grafana query
* start: The beginning of the time range of the Grafana query (in epoch time)
* end: The end of the time range of the Grafana query (in epoch time)
* schema: The LDMS schema specified by the Grafana query
    * E.g. meminfo
* maxDataPoints: the maximum number of points that Grafana can display on the user's screen

get_data

* metrics: a python list of LDMS metrics 
    * E.g. ['Active','MemFree']
* filters: a python list of filter strings for the DSOS query
	* E.g. ['job_id == 30','component_id < 604']
* params: a string of the extra parameters for the module to use as desired
	* E.g. 'threshold = 10'
	
Example Analysis Module
-------------------------------------

Below is a basic analysis that simply queries the database and returns the DataFrame of the metrics passed in along with the timestamp, component_id, and job_id for each metric. 

.. code-block :: python
    import os, sys, traceback
    import datetime as dt
    from graf_analysis.grafanaAnalysis import Analysis
    from sosdb import Sos
    import pandas as pd
    import numpy as np
    class dsosTemplate(Analysis):
        def __init__(self, cont, start, end, schema='job_id', maxDataPoints=4096):
            super().__init__(cont, start, end, schema, 1000000)
    
        def get_data(self, metrics, filters=[],params=None):
            try:
                sel = f'select {",".join(metrics)} from {self.schema}'
                where_clause = self.get_where(filters)
                order = 'time_job_comp'
                orderby='order_by ' + order
                self.query.select(f'{sel} {where_clause} {orderby}')
                res = self.get_all_data(self.query)
                # Fun stuff here!
                print(res.head)
                return res
            except Exception as e:
                a, b, c = sys.exc_info()
                print(str(e)+' '+str(c.tb_lineno))

In the __init__ function, most things are set to be self variables to access them later in the get_data using the super() function. The super() function also sets up a variable called self.query which is a Sos.SqlQuery object. The 1000000 in the super() function sets the block size for this self.query object. An optimal block size is dependent on the query, however 1 million has been sufficiently performant to this point.  

In the get_data function we create a select clause for the DSOS query by joining the metrics and schema variables. The self.get_where is a graf_analysis class function which takes filter parameters and makes an SQL-like where clause string with self.start and self.end as timestamp boundaries. There is also the orderby variable which we are setting as 'time_job_comp' here. This refers to what index we should use when querying the database. Our SOS databases are setup to use permutations of timestamps, job IDs, and component IDs as multi-indices. Depending on your filter, you may want to use a different multi-index. 

With the example parameters specified in the last section, our select statement here would be 'select Active,MemFree from meminfo where timestamp > start and timestamp < end and job_id == 30 and component_id < 604 order_by time_job_comp'. 

The self.get_all_data takes the Sos.SqlQuery object, self.query, and calls self.query.next. This returns a block size number of records that match the query from database defined by the cont variable. If there are more than a block size number of records, it continues calling self.query.next and appending the results to a pandas DataFrame until all data is returned. 

Additional analysis can be added where the "Fun stuff here!" comment is. 

Testing an Analysis Module
--------------------------

You do not need to query from the Grafana interface to test your module. Below is a simple code which mimics the Grafana pipeline and prints the JSON returned to Grafana. 

To run the test module, you will first need to set your path and pythonpath environment variables by running:

.. code-block :: bash
    export PYTHONPATH=/usr/bin/python:/<INSTALL_PATH>/lib/python<PYTHON_VERSION>/site-packages/
    export PATH=/usr/bin:/<INSTALL_PATH>/bin:/<INSTALL_PATH>/sbin::$PATH

Then you can imitate the Grafana query to call your analysis module using a python script such as:

.. code-block :: python

    #!/usr/bin/python3
    
    import time,sys
    from sosdb import Sos
    from grafanaFormatter import DataFormatter
    from table_formatter import table_formatter
    from time_series_formatter import time_series_formatter
    from dsosTemplate import dsosTemplate
    
    sess = Sos.Session("/<DSOS_CONFIG_PATH>/config/dsos.conf")
    cont = '<PATH_TO_DATABASE>'
    cont = sess.open(cont)
    
    model = dsosTemplate(cont, time.time()-300, time.time(), schema='meminfo', maxDataPoints=4096)
    
    x = model.get_data(['Active'])
    
    #fmt = table_formatter(x)
    fmt = time_series_formatter(x)
    x = fmt.ret_json()
    print(x)


