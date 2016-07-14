# You want to make sure your version produces better error rates than this :)
#!/usr/bin/env python -W ignore::DeprecationWarning
import sys
import KNNPredictor as knn
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

filename = sys.argv[0]
filename="test01.txt"
test_lines=[]
with open(filename) as fp:
    for line in fp:
        x,y=line.split(',')
        test_lines.append((x,y))
#x, y = open(filename, 'r').readlines()[0].split(',')
#print x,y
fp.close()
pred=knn.KNNPredictor(6)
norm_lines=pred.normalize(test_lines)
pred.process(norm_lines)
res=[]
for i in range(60):
    result=pred.KNN_predict(len(test_lines),len(test_lines)+1+i)
    res.append(result)

with open('prediction.txt', 'w') as f:
    for i in range(60):
        x=str(res[i][0])
        y=str(res[i][1])
        print >> f, '%s,%s' % (x.strip(), y.strip())

f.close()
