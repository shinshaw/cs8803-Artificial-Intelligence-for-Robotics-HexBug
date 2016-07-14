__author__ = 'shinshaw'
import math
import random
class KNNPredictor(object):
    test_lines=[]
    filename="test01.txt"
    def __init__(self,K):
        self.K=K
    with open(filename) as fp:
            for line in fp:
                test_lines.append(line)

    print test_lines