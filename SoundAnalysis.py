import os
import numpy
import pandas
import matplotlib.pyplot as plt
# answer(패딩없음)
csv_data = pandas.read_csv("_d.csv")
header = list(csv_data.columns)
row_count = len(csv_data)

plt.plot(csv_data)
plt.xlim(0, 7000)
plt.ylim(-12000, 15000)
plt.show()
