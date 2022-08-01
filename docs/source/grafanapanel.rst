Grafana Panel Creation with DSOS Plugin
======================================

To create a new dashboard, click on the + sign on the left side of the Grafana home page and select dashboard.
This will create a blank dashboard with an empty panel in it. Panels can be thought of as a visualization of a single query. select the add query button on the panel to begin configuring the query to be sent to an analysis module.

Configuring the Query and Visualization
---------------------------------------
.. image:: images/grafanapanel.png

Once you right click on the panel title and select edit, the panel settings will appear. The first tab is for configuring the query. There are 10 fields in the query field defined below:

* Query Type - type of query to perform. The most commonly used in "analysis" which calls an analysis module. "metrics" is used to return raw data without any analysis module. 
* Query Format - the type of visualization to be used on the dataset. It is used by Grafana Formatter to properly JSON-ify the data returned from the analysis module. Can be either time_series, table, or heatmap.
* Analysis - required if you choose analysis query type. Specifies the python module to call to transofrm the data.
* Container - the name of the container to be used. This can be either the full path to the container or the Django backend get_container function can be changed to customize for site settings.
* Schema - What LDMS schema will be passed into the analysis module
* Metric - Pass a metric, or a comma separated list (without spaces) of metrics, into the analysis module
* Extra Params - (Optional) pass in an arbitrary string into the analysis module
* Filters - (Optional) include a no-sql like syntax for filtering your query, can be a comma separated list of filters i.e. component_id == 5,job_id > 0

The second tab in the panel settings is for visualization. Graph, Table, and Heatmap are the available visualizations for a query output. Text, which uses Markdown language, could also be used for Dashboard descriptions or details. If you use a graph visualization, the query Format should be time_series. If you use a table visualization, the query Format should be table.

Graphs have multiple draw modes: bars, lines, and points. You can any or all of these draw modes on. You can also stack multiple time_series using the stack toggle button.
