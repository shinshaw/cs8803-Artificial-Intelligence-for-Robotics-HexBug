import turtle
import sys
import time
import math
import KNNPredictor as knn
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Visualizer:
    """A class that displays actual and predicted data (from a predictor) in a window."""
    WINDOW_WIDTH=1024

    def __init__(self,predictor):
        self.pred=predictor.KNNPredictor(12)
        self.setup = False

    def visualize(self,src,delta_y,delta_x,minX,minY,test_lines,norm_lines,knn_X, knn_Y,count,old_points,num_visualizations, skip_between_visualizations):

        for i in range(num_visualizations):
            self.visual(src+(i*skip_between_visualizations),delta_y,delta_x,minX,minY,test_lines,norm_lines,knn_X, knn_Y,count,old_points,True,False)
        self.window.exitonclick()

    def visual(self,src,delta_x,delta_y,minX,minY,test_lines,norm_lines,knn_X, knn_Y,count, old_points, wait_after_visualize=True, expect_robot_data=False):
        p=self.pred
        if not self.setup:
            self.setup=True
            self.window=turtle.Screen()
            self.window.setup(self.WINDOW_WIDTH, self.WINDOW_WIDTH * delta_y / delta_x)
            self.window.setworldcoordinates(minX, minY + delta_y, minX + delta_x, minY)
            self.window.bgcolor('black')

        real_data = test_lines
        old_turtle = turtle.Turtle()
        old_turtle.shape('triangle')
        old_turtle.color('green')
        old_turtle.penup()
        old_turtle.shapesize(0.3, 0.3, 0.3)

        predict_turtle = turtle.Turtle()
        predict_turtle.shape('triangle')
        predict_turtle.color('red')
        predict_turtle.penup()
        predict_turtle.shapesize(0.3, 0.3, 0.3)

        particle_turtle = turtle.Turtle()
        particle_turtle.shape('circle')
        particle_turtle.color('purple')
        particle_turtle.penup()
        particle_turtle.shapesize(0.3, 0.3, 0.3)


        actual_turtle = turtle.Turtle()
        actual_turtle.shape('circle')
        actual_turtle.color('blue')
        actual_turtle.penup()
        actual_turtle.shapesize(0.3, 0.3, 0.3)

        old_points = min(old_points, src - 1)
        old_turtle.speed('slow')
        particle_turtle.speed('fastest')
        last_point = [0.0, 0.0]
        for i in range(old_points):
            point = real_data[src - old_points + i]
            old_turtle.goto(int(point[0]), int(point[1]))
            if len(point) >= 4 and point[3]:
                old_turtle.setheading(point[3] * 180.0 / math.pi)
            if len(point) >= 6 and point[5] == True:
                old_turtle.color('red')
            old_turtle.stamp()
            old_turtle.color('green')
            last_point=point
            old_turtle.speed('fast')
            old_turtle.pendown()
            if expect_robot_data:
                robot_data = real_data[src - old_points + i]
                if robot_data[0] != -1.0:
                    particle_turtle.goto(robot_data[0], robot_data[1])
                    particle_turtle.stamp()

        predict_turtle.speed('fastest')
        actual_turtle.speed('fastest')

        actual_turtle.goto(old_turtle.xcor(), old_turtle.ycor())
        actual_turtle.pendown()

        last_point = [0.0, 0.0]
        last_prediction = [0.0, 0.0]
        for i in range(count):
            index=src+i
            print index
            if index < len(real_data):
                point = real_data[index]
                actual_turtle.goto(int(point[0]), int(point[1]))
                if len(point) >= 4 and point[3]:
                    actual_turtle.setheading(point[3] * 180.0 / math.pi)
                actual_turtle.stamp()
                last_point = point

            prediction = p.KNN_predict(src - 1, src + i, knn_X, knn_Y, norm_lines, delta_x, minX, delta_y, minY)
            predict_turtle.goto(prediction[0], prediction[1])
            predict_turtle.stamp()
            last_prediction = prediction
            predict_turtle.speed('slow')
            actual_turtle.speed('slow')
        #if wait_after_visualize:
            #self.window.exitonclick()

if __name__ == "__main__":
    vis=Visualizer(knn)
    test_lines = []
    filename="test01.txt"
    with open(filename) as ft:
        for line in ft:
            x, y = line.split(',')
            test_lines.append((x, y))
    ft.close()
    rows = len(test_lines)
    max_X = -1
    min_X = sys.maxint
    max_Y = -1
    min_Y = sys.maxint
    for i in range(rows):
        max_X = max(float(test_lines[i][0]), max_X)
        max_Y = max(float(test_lines[i][1]), max_Y)
        min_X = min(float(test_lines[i][0]), min_X)
        min_Y = min(float(test_lines[i][1]), min_Y)
    delta_X = max_X - min_X
    delta_Y = max_Y - min_Y
    pred = knn.KNNPredictor(12)
    norm_lines = pred.normalize_line(test_lines, min_X, delta_X, min_Y, delta_Y)
    knn_X = pred.knn_X(norm_lines)
    knn_Y = pred.knn_Y(norm_lines)
    src=1700
    vis.visualize(src,delta_X,delta_Y,min_X,min_Y,test_lines,norm_lines,knn_X, knn_Y,60,60,1, 1)

