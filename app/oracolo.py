from pandas import read_csv
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import ColumnTransformer
from datetime import datetime
import sys

csvFile = 'data/estrazioni-lotto.csv'
ruota = {'BA': 1, 'CA': 2, 'FI': 3, 'GE': 4, 'MI': 5, 'NA': 6, 'PA': 7, 'RO': 8, 'TO': 9, 'VE': 10, 'NZ': 11}

v1 = sys.argv[1]
v2 = ruota[sys.argv[2].upper()]

custom_date_parser = lambda x: datetime.strptime(x, "%d/%m/%Y")
estrazioni = read_csv(csvFile, delimiter=';', keep_default_na=False, parse_dates=['data'],date_parser=custom_date_parser)

estrazioni.ruota = [ruota[item] for item in estrazioni.ruota]
estrazioni['data'] = estrazioni['data'].dt.strftime('%d%m%Y')

X = estrazioni.drop(columns=['n1','n2','n3','n4','n5'])
y = estrazioni.drop(columns=['data', 'ruota'])

model = DecisionTreeClassifier()
model.fit(X.values, y.values)

predictNumbers = model.predict([[v1,v2]])

print(predictNumbers[0])