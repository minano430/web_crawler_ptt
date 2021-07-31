# -*- coding: utf-8 -*-

import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import matplotlib.pyplot as plt
import numpy as np
import random
import string


def multithreading(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)


def multiprocessing(func, args, workers):
    with ProcessPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)


def cpu_heavy(x):
    print('I am', x)
    start = time.time()
    count = 0
    for i in range(10**8):
        count += i
    stop = time.time()
    return start, stop

def io_heavy(text):
    start = time.time()
    f = open('output.txt', 'wt', encoding='utf-8')
    f.write(text)
    f.close()
    stop = time.time()
    return start,stop

def visualize_runtimes(results, title):
    start, stop = np.array(results).T
    plt.barh(range(len(start)), stop - start)
    plt.grid(axis='x')
    plt.ylabel("Tasks")
    plt.xlabel("Seconds")
    plt.xlim(0, 0.1)
    ytks = range(len(results))
    plt.yticks(ytks, ['job {}'.format(exp) for exp in ytks])
    plt.title(title)
    return stop[-1] - start[0]

if __name__ == '__main__': 
    N=12
    TEXT = ''.join(random.choice(string.ascii_lowercase) for i in range(10**7*5))
    plt.subplot(1, 2, 1)
    # visualize_runtimes(multithreading(cpu_heavy, range(4), 4), "Multithreading")
    visualize_runtimes(multithreading(io_heavy, [TEXT for i in range(N)], 1),"Single Thread")
    plt.subplot(1, 2, 2)
    # visualize_runtimes(multiprocessing(cpu_heavy, range(4), 4), "Multiprocessing")
    visualize_runtimes(multiprocessing(io_heavy, [TEXT for i in range(N)], 1),"Single Process")
    plt.show()