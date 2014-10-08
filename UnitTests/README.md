Unit Testing
============

The examples in this directory illustrate some basics of unit testing.

The **simple_tests.py** script shows a basic unit test for testing a function that adds two numbers together.  This is a very trivial example to illustrate the concept of an automated test.  Note the use of the **unittest** library (sometimes referred to as **PyUnit**) to give us functionality for setting up and tearing down expectations in our test suite, as well as asserting the result is as we expect it to be.

This simple test is testing a function which is deterministic, i.e. for each set of inputs there is an expected output.  Code that is deterministic is able to be tested easily in this manner.

In some cases if we create classes that internally use other objects in their business logic, we need to be able to supply those dependencies from the outside such that we can make the logic deterministic and therefore testable.  This concept is called dependency injection, and is related the SOLID principles of software design.

In the **greeting.py** file we have a **Greeting** class which will return a greeting based on the time of day.  The class uses the **Clock** class to determine the time of day.  If our greeting class determines the time of day internally from the datetime class in Python, then the class is not deterministic - we can't write a test to assert the business logic because it would be dependent on when the test is executed.

To get around this our Greeting class is supplied an instance of the Clock in its constructor.  In the **mock_tests.py** script, our tests mock the return value of the **get_time** method of the Clock class such that the time satisfies the test we are doing, i.e. a time in the morning, afternoon, or evening, for which we can assert the result.  For this we utilise the **Mock** library.

At runtime we don't want to have to supply all the dependencies of our classes as we create new instances, so we can use a library called **Pinject** to perform dependency injection for us based on naming conventions, as illustrated by the main method in the greeting.py file.  