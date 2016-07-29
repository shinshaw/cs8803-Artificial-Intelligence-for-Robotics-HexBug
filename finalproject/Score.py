import KNNPredictor as knn
import math
import sys
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Score:

    """ Generating scores for a predictor (vs. actual data)."""
    def __init__(self,predictor):
        self.pred=predictor.KNNPredictor(6)

    """Calculate and return the predicting error from the src point """
    def error(self,src,test_lines,pred_lines):
        total=0
        for i in range(60):
            err=self.L2_error(pred_lines[i],test_lines[i+src])
            total += err
        sum=math.sqrt(total)
        return sum

    """Calculate and return the average error per point from the src point to dest point.
    	For each point, sum the 60 predicting points error."""
    def train_err(self,src,dest,test_lines,knn_X,knn_Y,norm_lines,delta_X,min_X,delta_Y,min_Y):
        total=0
        count=0
        for i in range(src,dest):
            sum=0
            count += 1
            for j in range(60):
                err = self.L2_error(self.pred.KNN_predict(i, i + j,knn_X,knn_Y,norm_lines,delta_X,min_X,delta_Y,min_Y), test_lines[i + j])
                sum+=err
            total+=math.sqrt(sum)
        res=total/(count)
        print res
        return res

    def L2_error (self,p1,p2):
        return (float(p1[0])-float(p2[0]))**2 + (float(p1[1])-float(p2[1]))**2


def test_run():
    if len(sys.argv) < 2:
        print 'No action specified.'
        sys.exit()
    else:
        algoname = sys.argv[0]
        filename = sys.argv[1]
    s = Score(knn)
    test_lines_td = []
    with open(filename) as ft:
        for line in ft:
            x, y = line.split(',')
            test_lines_td.append((x, y))
    ft.close()
    rows = len(test_lines_td)
    max_X = -1
    min_X = sys.maxint
    max_Y = -1
    min_Y = sys.maxint
    for i in range(rows):
        max_X = max(float(test_lines_td[i][0]), max_X)
        max_Y = max(float(test_lines_td[i][1]), max_Y)
        min_X = min(float(test_lines_td[i][0]), min_X)
        min_Y = min(float(test_lines_td[i][1]), min_Y)

    delta_X = max_X - min_X
    delta_Y = max_Y - min_Y
    pred = knn.KNNPredictor(6)
    norm_lines = pred.normalize_line(test_lines_td, min_X, delta_X, min_Y, delta_Y)
    knn_X = pred.knn_X(norm_lines)
    knn_Y = pred.knn_Y(norm_lines)
    start_time = time.time()
    s.train_err(1700,1701,test_lines_td,knn_X,knn_Y,norm_lines,delta_X,min_X,delta_Y,min_Y)
    print("--- %s running time ---" % (time.time() - start_time))
    # 10 test cases result: test01: 529.683894203 0.271251916885 test02:534.088345792  0.218225955963 test03:1325.61257328 0.220170974731 test04:1119.88226068 0.224828004837
    # test05:157.836149218  0.214833021164 test06:177.508763477 0.212402105331 test07:72.6154253585  0.216380119324 test08:445.952725447 0.252189874649 test09:73.5755469644  0.208832979202 test10:167.501575449 0.210287094116
    # average of 10 test cases:472.0326639

    #10 test cases result: test01: 510.363737478 test02:403.253432749 test03:874.212896922 test04:539.112848478
    # test05:435.942745896 test06:343.701659854 test07:264.494790413 test08:752.905623142 test09:180.450844658 test10:415.888059239
    #average of 10 test cases:472.0326639

    #s.train_err(1740, 1741, test_lines_td, knn_X, knn_Y, norm_lines, delta_X, min_X, delta_Y, min_Y)
    # 10 test cases result: test01: 605.211011087 test02:533.657651481 test03:627.116411066 test04:398.923183761
    # test05:469.581403076 test06:363.854479735 test07:222.5388496 test08:420.888618075 test09:565.11669618 test10:548.166432887
    # average of 10 test cases:475.5054737


    #s.train_err(34900,35000,test_lines_td,knn_X,knn_Y,norm_lines,delta_X,min_X,delta_Y,min_Y)
    # result: 526.472262123
    #s.train_err(34800,35000,test_lines_td,knn_X,knn_Y,norm_lines,delta_X,min_X,delta_Y,min_Y)
    #result: 512.312690559


if __name__=="__main__":
    test_run()