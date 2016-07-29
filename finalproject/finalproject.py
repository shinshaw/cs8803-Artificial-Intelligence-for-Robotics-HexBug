__author__ = 'shinshaw'
import sys
import KNNPredictor as knn
import warnings
import numpy as np
warnings.filterwarnings("ignore", category=DeprecationWarning)


"""Read the training data from file filename"""
if len(sys.argv) < 2:
    print 'No action specified.'
    sys.exit()
else:
    algoname = sys.argv[0]
    filename=sys.argv[1]
test_lines=[]
with open(filename) as fp:
    for line in fp:
        x,y=line.split(',')
        test_lines.append((x,y))
fp.close()

rows=len(test_lines)
"""Get The maximum value of x and The maximum value of y from the training data"""
max_X=-1
min_X=sys.maxint
max_Y=-1
min_Y=sys.maxint
for i in range(rows):
    max_X = max(float(test_lines[i][0]), max_X)
    max_Y = max(float(test_lines[i][1]), max_Y)
    min_X = min(float(test_lines[i][0]), min_X)
    min_Y = min(float(test_lines[i][1]), min_Y)

delta_X = max_X - min_X
delta_Y = max_Y - min_Y

pred=knn.KNNPredictor(7)
norm_lines=pred.normalize_line(test_lines,min_X,delta_X,min_Y,delta_Y)
knn_X=pred.knn_X(norm_lines)
knn_Y=pred.knn_Y(norm_lines)

res=[]
for i in range(60):
    result=pred.KNN_predict(rows,rows+1+i,knn_X,knn_Y,norm_lines,delta_X,min_X,delta_Y,min_Y)
    res.append(result)

with open('prediction.txt', 'w') as f:
    for i in range(60):
        x=str(int(round(res[i][0])))
        y=str(int(round(res[i][1])))
        print >> f, '%s,%s' % (x.strip(), y.strip())

f.close()
