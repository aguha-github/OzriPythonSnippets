Asynchronous Requests
=====================

This example shows how we can use the **Twisted** library to perform asynchronous operations.

The example is fairly simplistic, it sends a request to http://host_name:6080/arcgis/rest/info?f=json for each of the hosts listed in the **servers** list.

The **test_site** function uses the map function to produce a list of the urls that will be requested, based on each of the hosts being applied to the url.

The requests are executed with Twisted's **getPage** function, with the result being a *deferred* represting an object that will hold the response when it has been received.

Each of the deferred's are added to a **DeferredList**, and a callback is defined to execute when all requests are received back.

In this way, none of the calls to *getPage* are blocking calls, but we continue execution once all responses have been recieved, calling into our **listCallback** function, which extracts a particular value from the json in each of the responses.  Our **finish** function then executes to end the Twisted reactor, to end the program.

This is a trivial example, but shows how multiple requests can be executed concurrently, and illustrates a way that ArcGIS Server machines could be contacted periodically to check uptime.