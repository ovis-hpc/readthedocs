AppSysFusion Quick Start
==================================================================

Dashboard Development
----------------------

Creating a New Dashboard
////////////////////////

The Grafana interface can be accessed at <URL>. To create a new dashboard, click on the + sign on the left side of the home page and hit dashboard. This will create a blank dashboard with an empty panel in it. Panels can be thought of as a visualization of a single query. Hit the add query button on the panel to begin configuring the query to be sent to an analysis module. 

Configuring the Query and Visualization
///////////////////////////////////////
<add image here>

Once you hit either add query on a panel or right click on the panel title and hit edit, the panel settings will appear. The first tab is for configuring the query. There are 10 fields in the query field defined below:

* Format - The type of visualization to be used on the dataset (time_series or table). Is used by Grafana Formatter to properly json-ify the data returned from the analysis module. 
* Container - The name of the container to be used. This path will also be used in the analysis module later on to query the correct container.
* (Optional) Schema - What LDMS schema will be passed into the analysis module
* (Optional) Job ID - Pass a slurm job ID into the query. If don't you want to pass a value, input 0
* (Optional) Comp ID - Pass a component ID into the query. If don't you want to pass a value, input 0
* (Optional) User Name - Pass a user name into the query
* (Optional) Metric - Pass a metric, or a comma separated list (without spaces) of metrics, into the analysis module
* Query Type - type of query to perform. The most commonly used in "analysis" which calls an analysis module. "Metrics" is used to return raw data without any analysis module. Others are unused currently. 
* Analysis - required if you choose analysis query type. Specifies the python script and class name to call to get data. 
* (Optional) Extra Params - Pass in an arbitrary string into the analysis module

The second tab in the panel settings is for visualization. Graph, Table, and Heatmap are the available visualizations for a query output. Text, which uses Markdown language, could also be used for Dashboard descriptions or details. If you use a graph visualization, the query Format should be time_series. If you use a table visualization, the query Format should be table.

Graphs have multiple draw modes: bars, lines, and points. You can any or all of these draw modes on. You can also stack multiple time_series using the stack toggle button. 

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



