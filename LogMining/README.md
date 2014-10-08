Log Mining
==========

This example analyses the logs in ArcGIS for Server to determine the distribution of map service requests, and the performance of those requests.  The results of this analysis are then graphed using **MatPlotLib**.

Note that this example requires that ArcGIS for Server is logging to the level of **FINE**.

The **main** function uses a custom class called **AgsAdmin** which retains the token for making requests to the admin rest interface of ArcGIS for Server.

The AgsAdmin class has a method called **query_logs** which acquires the log records.  Note the use of the **httplib**, **urllib**, **json** libraries for accessing the ArcGIS for Server admin rest endpoints and manipulating the results.

The main method then collates the raw log records into statistics which are then graphed using MatPlotLib.  The first sub plot creates a pie chart of the request distribution.  The second plot depicts the performance time as a boxplot, showing the median as a red line, the 25%-75% percentile as a green box, and the whiskers representing 1.5 times the inter-quartile range, i.e. the outliers - around 93 percentile. 