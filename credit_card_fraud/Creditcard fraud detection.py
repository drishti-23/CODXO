import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, recall_score, precision_score, precision_recall_curve
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

output_file_path1="./dataSet/creditcard1.csv"
output_file_path2="./dataSet/creditcard2.csv"
output_file_path_combined = "./dataSet/combinedcreditcard.csv"

def consolidateFile(output_file_path_combined) :
    with open(output_file_path_combined, 'w') as combined_file:
        with open(output_file_path1, 'r') as file1:
            for line in file1:
                combined_file.write(line)
                
        with open(output_file_path2, 'r') as file2:
            for line in file2:
                combined_file.write(line)
consolidateFile(output_file_path_combined)

"""#**Reading Dataset**"""

dataset = pd.read_csv(output_file_path_combined)
dataset

# getting top five data

dataset.head()

dataset.describe()

dataset.info()

dataset.isnull().values.any()

dataset.shape

"""## **Visualizations**"""

dataset.plot(figsize=(20, 8))
plt.show()

# visualizing the fraudulant credit card through Countplot

sns.countplot(x = "Class", data = dataset)
dataset.loc[:, 'Class'].value_counts()

# Visualizing the amount of Fraud and Non Fraud transactions in the form of piechart

labels = 'Not Fraud', 'Fraud'

# Calculate the count of Fraud and Non Fraud transactions in the dataset
sizes = [dataset.Class[dataset['Class']==0].count(), dataset.Class[dataset['Class']==1].count()]

# Create a new figure and axis for the pie chart
fig1, ax1 = plt.subplots(figsize=(10, 6))

ax1.pie(sizes, labels=labels, autopct='%1.2f%%', shadow=False, startangle=120)

ax1.axis('equal')

title = "The Percentage of Fraud and Non Fraud transactions"
plt.title(title, size=16, pad=20)

plt.show()

V_col = dataset[['V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','V12','V13','V14','V15','V16','V17','V18','V19','V20','V21','V22','V23','V24','V25','V26','V27','V28']]
V_col.head()

V_col.hist(figsize=(30, 20))
plt.show()

Normal_transcations = len(dataset[dataset['Class']==1])
Fraud_transcations = len(dataset[dataset['Class']==0])
print("No. of normal transactions:",Normal_transcations)
print("NO. of fraud transcations:", Fraud_transcations)

"""#**Modeling**"""

X = dataset.iloc[:, 1:29].values
Y = dataset.iloc[:, 30].values

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.25, random_state = 0)
print ("X train: ", len(X_train))
print("X test: ", len(X_test))
print("Y train: ", len(Y_train))
print("Y test: ", len(Y_test))

"""## ***Logistic Regression***"""

logreg = LogisticRegression(random_state = 0)
logreg.fit(X_train, Y_train)

y_lr = logreg.predict(X_test)
logreg.score(X_test, Y_test)
print('accuracy of training set: {:.4f}'.format(logreg.score(X_train,Y_train)))
print('accuaracy of test set: {:.4f}'.format(logreg.score(X_test, Y_test)))

acc =  accuracy_score(Y_test, y_lr)
prec =  precision_score(Y_test, y_lr)
rec =  recall_score(Y_test, y_lr)
pre_rec = precision_recall_curve(Y_test, y_lr)
f1 = f1_score(Y_test, y_lr)

results = pd.DataFrame([['LogisticRegression', acc, prec, rec, pre_rec, f1]],
                       columns = ["Model", "accuracy", "precision", "recall", "precision_recall", "f1_score"])

results

conf_mat = conf =  confusion_matrix(Y_test, y_lr)
print (conf_mat)
plt.figure(figsize=(10, 8))
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Reds')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

log = LogisticRegression(random_state = 1000, C =100)
log.fit(X_train, Y_train)

y_pred = log.predict(X_test)

log.score(X_test, Y_test)
print('accuracy of training set: {:.4f}'.format(log.score(X_train,Y_train)))
print('accuaracy of test set: {:.4f}'.format(log.score(X_test, Y_test)))

"""## ***Random Forest***"""

classifier_rm = RandomForestClassifier(random_state=0)
classifier_rm.fit(X_train, Y_train)

y_pred = classifier_rm.predict(X_test)

acc = accuracy_score(Y_test, y_pred)
f1 = f1_score(Y_test, y_pred)
prec = precision_score(Y_test, y_pred)
rec = recall_score(Y_test, y_pred)

model_results = pd.DataFrame([['Random Forest', acc, f1, prec, rec]],
                       columns = ["Model", "accuracy", "f1", "precision", "recall"])

results = pd.concat([results, model_results], ignore_index=True)

results

cm = confusion_matrix(Y_test, y_pred)
print(cm)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

"""### ***KNN Classifier***"""

knc = KNeighborsClassifier(n_neighbors = 17)
X,y = dataset.loc[:,dataset.columns != 'Class'], dataset.loc[:,'Class']
knc.fit(X_train,Y_train)
y_knc = knc.predict(X_test)
print('accuracy of training set: {:.4f}'.format(knc.score(X_train,Y_train)))
print('accuracy of test set: {:.4f}'.format(knc.score(X_test, Y_test)))

acc = accuracy_score(Y_test, y_knc)
f1 = f1_score(Y_test, y_knc)
prec = precision_score(Y_test, y_knc)
rec = recall_score(Y_test, y_knc)

results = pd.DataFrame([['KNeighboursClassifier', acc, prec, rec, pre_rec, f1]],
                       columns = ["Model", "accuracy", "precision", "recall", "precision_recall", "f1_score"])

results

con_ma = confusion_matrix(Y_test, y_knc)
print (con_ma)

plt.figure(figsize=(10, 8))
sns.heatmap(con_ma, annot=True, fmt='d', cmap='Greens')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

"""## ***Decision Tree***"""

classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(X_train, Y_train)

y_dtc = classifier.predict(X_test)

classifier.score(X_test, Y_test)
print('accuracy of training set: {:.4f}'.format(classifier.score(X_train,Y_train)))
print('accuaracy of test set: {:.4f}'.format(classifier.score(X_test, Y_test)))

classifier = DecisionTreeClassifier(max_depth = 4, random_state = 42)
classifier.fit(X_train,Y_train)
print('accuracy of training set: {:.4f}'.format(classifier.score(X_train,Y_train)))
print('accuaracy of test set: {:.4f}'.format(classifier.score(X_test, Y_test)))

acc = accuracy_score(y_dtc, Y_test)
f1 = f1_score(y_dtc, Y_test)
prec = precision_score(y_dtc, Y_test)
rec = recall_score(y_dtc, Y_test)

results = pd.DataFrame([['KNeighboursClassifier', acc, prec, rec, pre_rec, f1]],
                       columns = ["Model", "accuracy", "precision", "recall", "precision_recall", "f1_score"])

results

co_ma = confusion_matrix(y_dtc, Y_test)
print(co_ma)

plt.figure(figsize=(10, 8))
sns.heatmap(co_ma, annot=True, fmt='d')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()
