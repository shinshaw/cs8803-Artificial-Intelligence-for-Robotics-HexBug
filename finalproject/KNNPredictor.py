__author__ = 'shinshaw'
import math
import random
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

class KNNPredictor(object):
    def __init__(self,K):
        self.K=K
    """Return a KNN prediction based on the dx and dy of K most similar points to src point"""
    def KNN_predict(self,src,dest,knn_X,knn_Y,norm_lines,delta_X,min_X,delta_Y,min_Y):
        knn_orig = np.array(norm_lines)[0:len(norm_lines) - 60, 0:4]
        neigh_x = KNeighborsRegressor(n_neighbors=self.K,algorithm='kd_tree')
        neigh_y = KNeighborsRegressor(n_neighbors=self.K,algorithm='kd_tree')
        orig_X=knn_orig
        orig_Y = knn_orig
        X_pre= knn_X[dest-src]
        Y_pre= knn_Y[dest-src]
        neigh_x.fit(orig_X, X_pre)
        neigh_y.fit(orig_Y, Y_pre)
        pred_X=neigh_x.predict(norm_lines[src-1])[0]
        pred_Y=neigh_y.predict(norm_lines[src-1])[0]
        result=self.denorm((norm_lines[src-1][0]+pred_X,norm_lines[src-1][1]+pred_Y),delta_X,min_X,delta_Y,min_Y)
        return result

    """ Normalize all points to the range ([0,1],[0,1]),then add the corresponding angles and velocity based on each point's previous point
        format: [norm_x,norm_y,velocity,angle]"""
    def normalize_line(self,test_lines,min_X,delta_X,min_Y,delta_Y):
        norm_lines=[]
        for i in range(len(test_lines)):
            new_norm_lines=[((float(test_lines[i][0])-min_X)/delta_X),( (float(test_lines[i][1])-min_Y )/delta_Y),-1,-1]
            if i>0  :
                    new_norm_lines[2]=math.sqrt((new_norm_lines[0]-norm_lines[-1][0])**2+(new_norm_lines[1]-norm_lines[-1][1])**2)
                    new_norm_lines[3]=math.atan2(-1*(new_norm_lines[1]-norm_lines[-1][1]),(new_norm_lines[0]-norm_lines[-1][0]))
            norm_lines.append(new_norm_lines)
        return norm_lines

    """Convert a normalized point to a normal point"""
    def denorm(self,point,delta_X,min_X,delta_Y,min_Y):
        new_X=point[0]*delta_X+min_X
        new_Y=point[1]*delta_Y+min_Y
        return (new_X,new_Y)


    def knn_X(self,norm_lines):
        knn_X=[]
        for i in range(61):
            knn_X.append(np.array(norm_lines)[i:len(norm_lines)-60+i,0]-np.array(norm_lines)[0:len(norm_lines)-60,0])
        return knn_X
    def knn_Y(self, norm_lines):
        knn_Y = []
        for i in range(61):
            knn_Y.append(np.array(norm_lines)[i:len(norm_lines) - 60 + i, 1] - np.array(norm_lines)[0:len(norm_lines) - 60, 1])
        return knn_Y
