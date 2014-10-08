import datetime
import pinject

# function to add numbers
class Greeting(object):
    def __init__(self, clock):
        self.clock = clock

    def say_hello(self, name):
        time = self.clock.get_time()
        
        if time.hour > 12 and time.hour < 18:
            return "Good afternoon " + name
        elif time.hour > 17 and time.hour < 24:
            return "Good evening " + name
        else:
            return "Good morning " + name


class Clock(object):
    def get_time(self):
        return datetime.datetime.now().time()


def main():
    obj_graph = pinject.new_object_graph()
    greeting = obj_graph.provide(Greeting)
    print greeting.say_hello("Todd")


if __name__ == '__main__':
    main()