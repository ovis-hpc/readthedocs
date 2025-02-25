About the OVIS Project
================================
OVIS is composed of multiple subprojects, each designed to address specific aspects of HPC system monitoring and data management. These subprojects work together seamlessly to form a comprehensive ecosystem for efficient performance analysis and optimization.

LDMS (Lightweight Distributed Metric Service)
---------------------------------------------
LDMS is a lightweight framework for collecting, aggregating, and transporting system metrics in HPC environments. It gathers data from diverse sources like hardware counters and system logs, enabling real-time monitoring with low overhead and scalability for large systems.

SOS (Scalable Object Store)
---------------------------
SOS stores and queries observability data, acting as a repository for metrics and logs collected by LDMS. It supports advanced indexing and retrieval, enabling efficient exploration of large-scale datasets.

ASF (AppSysFusion)
------------------
AppSysFusion provides analysis and visualization capabilities aimed at serving insights from HPC monitoring data gathered with LDMS, though could be generalized outside of that scope.
It combines a Grafana front-end with a Django back-end to perform in-query analyses on raw data and return transformed information back to the end user.

LDMS Containers
---------------
The LDMS Containers provides Docker recipes and scripts for building images of various LDMS related components such as:

- **ldms-dev**: Development environment with dependencies for building OVIS binaries and developing LDMS plugins.

- **ldms-samp**: Runtime image containing `ldmsd` and sampler plugins for data collection.

- **ldms-agg**: Includes `ldmsd`, sampler plugins, and storage plugins (e.g., SOS) for data aggregation and storage.

- **ldms-maestro**: Contains Maestro and Etcd for managing distributed LDMS deployments.

- **ldms-ui**: Provides an HTTP-based UI backend for LDMS data access using uwsgi, Django, and SOSDB.

- **ldms-grafana**: Includes Grafana with the SOS data source plugin for visualizing LDMS data.


Maestro
-------
Maestro manages data flow within the OVIS ecosystem, ensuring efficient transport, storage, and access. It integrates seamlessly with various data sources and sinks, maintaining high performance and low latency.

Baler
-----
Baler analyzes and compresses logs, extracting patterns and anomalies while reducing storage needs. It transforms raw logs into actionable insights, aiding trend detection and forensic analysis.
