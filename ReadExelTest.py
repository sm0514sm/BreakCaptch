import pandas
import csv

X_train = []
Y_train = []

X_test = []
Y_test = []

csv_data = pandas.read_csv('test.csv')
header = list(csv_data.columns)
for i in header:
    Y_test.append(i[2:3])
row_count = len(csv_data)
column_count = len(Y_test)
csv_array = csv_data.values
for j in range(len(Y_test)):
    temp_X = []
    for i in range(row_count):
        temp_X.append(csv_array[i][j])
    X_test.append(temp_X)

print(X_test)
