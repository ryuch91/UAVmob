from numpy import random
from src.models.map import Map
from numpy import random
import numpy as np

if __name__ == '__main__':

    a = {'1': 1000, '2':2000, '3':3000}
    b = a.copy()

    print(a)
    print(b)

    a['1'] = 4000

    print(a)
    print(b)

    b['3']=9000

    print(a)
    print(b)