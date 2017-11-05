import sched, time
from datetime import date
import datetime

s = sched.scheduler(time.time, time.sleep)

def print_time(a='default'):
    #d = date.fromtimestamp(time.time())
    d = datetime.datetime.now()
    print("From print_time", d.strftime("%Y%m%d_%H%M%S"), a)

def print_some_times():
    print(time.time())
    print(datetime.datetime.now().strftime("%Y%m%d %H%M%S :"))
    s.enter(10, 1, print_time)
    s.enter(5, 2, print_time, argument=('positional',))
    s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
    s.enter(15, 1, print_time)
    s.run()
    print(time.time())

print_some_times()