AppSysFusion Quick Start
==================================================================

Create A Simple Analysis
------------------------
To start, please create a folder called ``graf_analysis`` in your home directory and copy the following contents to a python file called ``queryMeminfo.py``:

* This is a python analysis that queries the DSOS database and returns a DataFrame of all the "meminfo" metrics along with the ``timestamp``, ``component_id`` and ``job_id``. 

queryMeminfo.py:

.. code-block :: python

    import os, sys, traceback
    import datetime as dt
    from graf_analysis.grafanaAnalysis import Analysis
    from sosdb import Sos
    import pandas as pd
    import numpy as np
    class dsosTemplate(Analysis):
        def __init__(self, cont, start, end, schema='meminfo', maxDataPoints=4096):
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

.. note:: 
  
  If you want to use this analysis module in a Grafana dashboard, you will need to ask your administrator to copy your new analysis module(s) into the directory that Grafana points to. This is because Grafana is setup to look at a specific path directory to query from. 

Test Analysis via Terminal Window
----------------------------------
You do not need to query from the Grafana interface to test your module. Below is a simple code which mimics the Grafana pipeline and prints the JSON returned to Grafana. 
If you wish to find a username based on another metric listed in the schema "jobid", just include "job_id=<job_id number>" to the get_data function. 

First, you will need to set your path and pythonpath environment variables with the following:

.. code-block :: bash

    export PYTHONPATH=/usr/bin/python:/<INSTALL_PATH>/lib/python<PYTHON_VERSION>/site-packages/
    export PATH=/usr/bin:/<INSTALL_PATH>/bin:/<INSTALL_PATH>/sbin::$PATH

* Then create the following file in the same directory as your python analysis (i.e. ``/user/home/graf_analysis/``) and label it ``testModule.py``. This python script imitates the Grafana query that calls your analysis module and will output the DataFrame described earlier.

.. note::

  You will need to provide the path to the DSOS container and Sos.Session() configuration file in order to run this python script. Please see the :doc:`pyanalysis.rst` for more details.

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

* Next, run the python module:

.. code-block :: bash

  python3 testModule.py

  All imports are python scripts that need to reside in the same directory as the test analysis module in order for it to run successfully.  

Then, run the python script with the current python verion installed. In this case it would be ``python3 <analysisTemplate.py>``

Test Analysis via Grafana Dashboard
-----------------------------------

Create A New Dashboard
//////////////////////
The Grafana interface can be accessed at <URL>. To create a new dashboard, click on the + sign on the left side of the home page and hit dashboard. This will create a blank dashboard with an empty panel in it. Panels can be thought of as a visualization of a single query. Hit the add query button on the panel to begin configuring the query to be sent to an analysis module. 

.. note::
  
  For more information on how to navigate around the Grafana dashboard and what the variables and advanced settings do, please see :doc:`Grafana Panel <grafanapanel>` and :doc:`Grafana Usage <grafanause>`

Expected Results & Output
-------------------------
Terminal Window
/////////////////////////////
The following is an example test of an analysis module that queries the schema "job_id" and outputs the

Grafana Dashboard
/////////////////////////////////


