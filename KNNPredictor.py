__author__ = 'shinshaw'
import math
import random
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
class KNNPredictor(object):
    def __init__(self,K):
        self.K=K
    lines=[]
    norm_line=[]
    knn_orig=[]
    knn_final_x=[]
    knn_final_y=[]
    filename="test01.txt"
    with open(filename) as fp:
            for line in fp:
                x,y=line.split(',')
                lines.append((x,y))
    fp.close()
    count=len(lines)
    maxX=-1
    minX=1000000000
    maxY=-1
    minY=1000000000
    for i in range(count):
        maxX=max(float(lines[i][0]),maxX)
        maxY=max(float(lines[i][1]),maxY)
        minX=min(float(lines[i][0]),minX)
        minY=min(float(lines[i][1]),minY)
    delta_x=maxX-minX
    delta_y=maxY-minY

    def KNN_predict(self,src,dest):
        neigh_x = KNeighborsRegressor(n_neighbors=6,algorithm='kd_tree')
        neigh_y = KNeighborsRegressor(n_neighbors=6,algorithm='kd_tree')
        Xorig=self.knn_orig
        Xfinal=  self.knn_final_x[dest-src]
        Yorig= self.knn_orig
        Yfinal=  self.knn_final_y[dest-src]
        neigh_x.fit(Xorig, Xfinal)
        neigh_y.fit(Yorig, Yfinal)
        predX=neigh_x.predict(self.norm_lines[src-1])[0]
        predY=neigh_y.predict(self.norm_lines[src-1])[0]
        result=self.denorm((self.norm_lines[src-1][0]+predX,self.norm_lines[src-1][1]+predY))
        return result

    def addData(self,maxX,maxY,minX,minY,delta_x,delta_y):
        self.maxX=maxX
        self.maxY=maxY
        self.minX=minX
        self.minY=minY
        self.delta_x=delta_x
        self.delta_y=delta_y

    def normalize(self,lines):
        norm_lines=[]
        for i in range(len(lines)):
            new_norm_lines=[((float(lines[i][0])-self.minX)/self.delta_x),( (float(lines[i][1])-self.minY )/self.delta_y),-1,-1]
            if i>0  :
                    new_norm_lines[2]=math.sqrt((new_norm_lines[0]-norm_lines[-1][0])**2+(new_norm_lines[1]-norm_lines[-1][1])**2)
                    new_norm_lines[3]=math.atan2(-1*(new_norm_lines[1]-norm_lines[-1][1]),(new_norm_lines[0]-norm_lines[-1][0]))
            norm_lines.append(new_norm_lines)
        return norm_lines

    def denorm(self,point):
        new_x=point[0]*self.delta_x+self.minX
        new_y=point[1]*self.delta_y+self.minY
        return (new_x,new_y)
    def process(self,norm_lines):
        self.norm_lines=norm_lines
        self.knn_orig=np.array(self.norm_lines)[0:len(self.norm_lines)-60,0:4]
        for i in range(61):
            self.knn_final_x.append(np.array(self.norm_lines)[i:len(self.norm_lines)-60+i,0]-np.array(self.norm_lines)[0:len(self.norm_lines)-60,0])
            self.knn_final_y.append(np.array(self.norm_lines)[i:len(self.norm_lines)-60+i,1]-np.array(self.norm_lines)[0:len(self.norm_lines)-60,1])

def test_run():
    import KNNPredictor as knn
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    p=knn.KNNPredictor(6)
    lines=p.lines
    norm_lines=p.normalize(lines)
    p.process(norm_lines)
    result=[]
    for i in range(60):
        result.append(p.KNN_predict(len(lines),len(lines)+1+i))
    print len(result)
    #print p.norm_lines
if __name__=="__main__":
    test_run()