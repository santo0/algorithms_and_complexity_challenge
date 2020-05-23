'''
    Title: dec_timer.py
    Author: Guillem Camats Felip, Adria Juve Sanchez, Marti La Rosa Ramos, Xavier Nadal Reales
    Date: 25-5-2020
    Code version: 1.0.0
    Availability: https://github.com/santo0/algorithms_and_complexity_challenge
'''

import functools
import time

def timer(func):
    '''Print the runtime of the wrapped function'''
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.time()
        value = func(*args, **kwargs)
        end_time = time.time() - start_time
        print('Finished {} in {:.2f} secs'.format(func.__name__, end_time))
        return value
    return wrapper_timer
