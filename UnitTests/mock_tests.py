import unittest
from mock import Mock
import datetime
import greeting as grt


class MyMockedTests(unittest.TestCase):

    # test the greeting in the morning
    def test_morning(self):

        # mock the clock such that get_time passes back the time 9:52
        clock = grt.Clock()
        clock.get_time = Mock(return_value=datetime.datetime(2014, 10, 3, 9, 52))

        # inject the mocked clock as a dependency 
        greeting = grt.Greeting(clock)

        # assert that the greeting is correct
        result = greeting.say_hello("Todd")
        self.assertEqual("Good morning Todd", result)


    # test the greeting in the afternoon
    def test_afternoon(self):

        # mock the clock such that get_time passes back the time 13:23
        clock = grt.Clock()
        clock.get_time = Mock(return_value=datetime.datetime(2014, 10, 3, 13, 23))

        # inject the mocked clock as a dependency
        greeting = grt.Greeting(clock)

        # assert that the greeting is correct
        result = greeting.say_hello("Todd")
        self.assertEqual("Good afternoon Todd", result)

    # test the greeting in the evening
    def test_evening(self):

        # mock the clock such that get_time passes back the time 19:12
        clock = grt.Clock()
        clock.get_time = Mock(return_value=datetime.datetime(2014, 10, 3, 19, 12))

        # inject the mocked clock as a dependency
        greeting = grt.Greeting(clock)

        # assert that the greeting is correct
        result = greeting.say_hello("Todd")
        self.assertEqual("Good evening Todd", result)


if __name__ == '__main__':
    unittest.main()