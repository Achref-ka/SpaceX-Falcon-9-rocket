# Space X Falcon 9 First Stage Landing Prediction

# Objectives
# Perform exploratory Data Analysis and determine Training Labels:

# - create a column for the class
# - Standardize the data
# - Split into training data and test data


# Find best Hyperparameter for SVM, Classification Trees and Logistic Regression:
# - Find the method performs best using test data


# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, 
# along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. 
# We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
# Seaborn is a Python data visualization library based on matplotlib. 
# It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standarsize our data
from sklearn import preprocessing
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
from sklearn.neighbors import KNeighborsClassifier


# This function is to plot the confusion matrix.

def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed']) 
    plt.show()
    
    
# Load the dataframe

url_1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"

data = pd.read_csv(url_1)

print(data.head(6))

url_2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv'

X = pd.read_csv(url_2)

print(X.head(10))

# TASK 1 - Create a NumPy array from the column Class in data, by applying the method to_numpy() then assign it to the variable Y,make sure 
# the output is a Pandas series (only one bracket df['name of column']).



# TASK 1 - Create a NumPy array from the column Class in data, by applying the method to_numpy() then assign it to the variable Y,
# make sure the output is a Pandas series (only one bracket df['name of column']).

# Create a NumPy array from the "Class" column in data
Y = data['Class'].to_numpy()

# Make sure the output is a Pandas series
print(type(Y))  # It should output: <class 'numpy.ndarray'>

# TASK 2 - Standardize the data in X then reassign it to the variable X using the transform provided below.

# Initialize the StandardScaler
transform = preprocessing.StandardScaler()

# Standardize the data in X and reassign it to the variable X
X = transform.fit_transform(X)

# Display the first 5 rows of the standardized data
print(pd.DataFrame(X).head())


# We split the data into training and testing data using the function train_test_split. 
# The training data is divided into validation data, a second set used for training data; 
# then the models are trained and hyperparameters are selected using the function GridSearchCV.


# TASK 3 - Use the function train_test_split to split the data X and Y into training and test data. Set the parameter test_size to 0.2 and random_state to 2. 
# The training data and test data should be assigned to the following labels:  X_train, X_test, Y_train, Y_test

# Split the data into training and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# Display the shape of the resulting sets to verify the split
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("Y_train shape:", Y_train.shape)
print("Y_test shape:", Y_test.shape)


# TASK 4 - Create a logistic regression object then create a GridSearchCV object logreg_cv with cv = 10. Fit the object to find the best parameters from the dictionary parameters.

# Create a logistic regression object
logreg = LogisticRegression(solver='lbfgs')  # Specify the solver that supports 'l2' penalty

# Define the parameter grid

parameters ={'C':[0.01,0.1,1],
             'penalty':['l2'],
             'solver':['lbfgs']}


# Create a GridSearchCV object
logreg_cv = GridSearchCV(logreg, parameters, cv=10)

# Fit the GridSearchCV object to the data
logreg_cv.fit(X_train, Y_train)

# Display the best parameters and corresponding accuracy score
print("Best Parameters: ", logreg_cv.best_params_)
print("Best Accuracy Score: {:.2f}".format(logreg_cv.best_score_))


# TASK 5 - Calculate the accuracy on the test data using the method score

# Use the best-fitted model to make predictions on the test data
Y_pred = logreg_cv.predict(X_test)

# Calculate the accuracy on the test data
accuracy = logreg_cv.score(X_test, Y_test)

# Display the accuracy
print("Accuracy on Test Data: {:.2f}".format(accuracy))

# Lets look at the confusion matrix:

yhat=logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# Examining the confusion matrix, we see that logistic regression can distinguish between the different classes. We see that the major problem is false positives.


# TASK 6 - Create a support vector machine object then create a GridSearchCV object svm_cv with cv - 10. Fit the object to find the best parameters from the dictionary parameters.

# Create a Support Vector Machine (SVM) object
svm = SVC()

# Define the parameter grid
parameters = {'kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
              'C': np.logspace(-3, 3, 5),
              'gamma': np.logspace(-3, 3, 5)}

# Create a GridSearchCV object
svm_cv = GridSearchCV(svm, parameters, cv=10)

# Fit the GridSearchCV object to the data
svm_cv.fit(X_train, Y_train)

# Display the best parameters and corresponding accuracy score
print("Best Parameters: ", svm_cv.best_params_)
print("Best Accuracy Score: {:.2f}".format(svm_cv.best_score_))


# TASK 7 - Calculate the accuracy on the test data using the method score:


# Use the best-fitted SVM model to make predictions on the test data
Y_pred_svm = svm_cv.predict(X_test)

# Calculate the accuracy on the test data
accuracy_svm = svm_cv.score(X_test, Y_test)

# Display the accuracy
print("Accuracy on Test Data (SVM): {:.2f}".format(accuracy_svm))


# We can plot the confusion matrix

yhat=svm_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# TASK 8 - Create a decision tree classifier object then create a GridSearchCV object tree_cv with cv = 10. Fit the object to find the best parameters from the dictionary parameters.

# Create a Decision Tree Classifier object
tree = DecisionTreeClassifier()

# Define the parameter grid
parameters = {'criterion': ['gini', 'entropy'],
              'splitter': ['best', 'random'],
              'max_depth': [2 * n for n in range(1, 10)],
              'max_features': ['auto', 'sqrt'],
              'min_samples_leaf': [1, 2, 4],
              'min_samples_split': [2, 5, 10]}

# Create a GridSearchCV object
tree_cv = GridSearchCV(tree, parameters, cv=10)

# Fit the GridSearchCV object to the data
tree_cv.fit(X_train, Y_train)

# Display the best parameters and corresponding accuracy score
print("Best Parameters: ", tree_cv.best_params_)
print("Best Accuracy Score: {:.2f}".format(tree_cv.best_score_))

# TASK 9 - Calculate the accuracy of tree_cv on the test data using the method score:

# Use the best-fitted Decision Tree model to make predictions on the test data
Y_pred_tree = tree_cv.predict(X_test)

# Calculate the accuracy on the test data
accuracy_tree = tree_cv.score(X_test, Y_test)

# Display the accuracy
print("Accuracy on Test Data (Decision Tree): {:.2f}".format(accuracy_tree))

# We can plot the confusion matrix

yhat = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# TASK 10 - Create a k nearest neighbors object then create a GridSearchCV object knn_cv with cv = 10. Fit the object to find the best parameters from the dictionary parameters.

# Create a k-Nearest Neighbors (KNN) Classifier object
KNN = KNeighborsClassifier()

# Define the parameter grid
parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1, 2]}

# Create a GridSearchCV object
knn_cv = GridSearchCV(KNN, parameters, cv=10)

# Fit the GridSearchCV object to the data
knn_cv.fit(X_train, Y_train)

# Display the best parameters and corresponding accuracy score
print("Best Parameters: ", knn_cv.best_params_)
print("Best Accuracy Score: {:.2f}".format(knn_cv.best_score_))


# TASK 11 - Calculate the accuracy of knn_cv on the test data using the method score

# Use the best-fitted k-Nearest Neighbors model to make predictions on the test data
Y_pred_knn = knn_cv.predict(X_test)

# Calculate the accuracy on the test data
accuracy_knn = knn_cv.score(X_test, Y_test)

# Display the accuracy
print("Accuracy on Test Data (k-Nearest Neighbors): {:.2f}".format(accuracy_knn))


# We can plot the confusion matrix

yhat = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# TASK 12 - Find the method performs best:

# To find the method that performs best among Logistic Regression, Support Vector Machine (SVM), Decision Tree, and k-Nearest Neighbors (KNN), 
# you can compare their accuracy scores on the test data. After fitting each model using grid search and obtaining the best parameters, 
# you calculated the accuracy for each model on the test set.

# Now, you can compare the accuracy scores and determine which model performed the best. Here's an example of how you can compare the accuracy scores:

# Display the accuracy scores for each model
print("Accuracy on Test Data (Logistic Regression): {:.2f}".format(accuracy))
print("Accuracy on Test Data (SVM): {:.2f}".format(accuracy_svm))
print("Accuracy on Test Data (Decision Tree): {:.2f}".format(accuracy_tree))
print("Accuracy on Test Data (k-Nearest Neighbors): {:.2f}".format(accuracy_knn))


# In this example, the model with the highest accuracy score on the test data is considered the best-performing model. 
# You can make a decision based on these accuracy scores. 
# Keep in mind that the best-performing model might vary depending on the specific characteristics of your dataset and the problem you are trying to solve.


# Display the best parameters for the SVM model
print("Best Parameters for SVM: ", svm_cv.best_params_)