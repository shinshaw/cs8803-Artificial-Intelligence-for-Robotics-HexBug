======================================================
CS 8803 Final Project - Summer 2016
Xin Xiao,Robert Houck,Quansheng Yang,Anthony Lee
======================================================
The HEXBUG Nano micro robot predictor is based on K-Nearest Neighbor prediction method(K=7). In the KNN, the training set is used to predict the value of variables of interest for each member of a target data set. 

The prediction process of the KNN predictor:
- Normalize x,y coordinate of each training data to the range([0,1],[0,1]).
- Calculate the velocity and angle from each point to the previous point.
- Build a new 4D training data(x coordinate,y coordinate,velocity and angle). 
- Set up 60 vectors(dx,dy) up to 60 time steps from each known coordinate.
- From the given starting point, find 7 most similar points in the training data.
- Calculate the mean dx and dy of these 7 points. 
- Add the mean dx and dy to the starting point.
- Return 60 denormalized predicting x,y coordinates.


======================================================
Required Libraries
======================================================
python 2.7.10
numpy 1.10.1
scipy 0.16.1
scikit-learn 0.17b1

The easiest way to install scikit-learn is using pip:
pip install -U scikit-learn


======================================================
Command line arguments
======================================================
$ python finalproject.py input_file 


======================================================
Prediction Results
======================================================
L2 error
—Prediction to each of the next 60 points from each of ten test cases (1700,1740)
test01:605.211011087
test02:533.657651481
test03:627.116411066
test04:398.923183761
test05:469.581403076
test06:363.854479735
test07:222.5388496
test08:420.888618075
test09:565.11669618
test10:548.166432887
## Average error:475.5054737
## std_dev: 125.5396639 

-Prediction to each of the next 60 points from each of the training_data (34800,35000)
## Average error:512.312690559


======================================================
Included files
======================================================
finalproject.zip
——-­­­­­­​finalproject   ——-inputs ­­­­­ ­    ——-​test01.txt  ­­­ ​   ——-test02.txt  ­­­­­­    ——-​...

   ——-finalproject.py 
   Outputs prediction.txt.

   ——-KNNPredictor.py
   Includes a core KNN predictor.

   ——-Score.py
   Calculates average L2 error from all training data in a designated range.

   ­——-members.txt   ­­­­——-readme.txt
   ­­­­——-report.pdf


