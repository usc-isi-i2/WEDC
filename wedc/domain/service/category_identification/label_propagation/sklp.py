from sklearn import datasets
from sklearn.semi_supervised import LabelPropagation
import numpy as np


label_prop_model = LabelPropagation()
iris = datasets.load_iris()
random_unlabeled_points = np.where(np.random.random_integers(0, 1,
size=len(iris.target)))
labels = np.copy(iris.target)
labels[random_unlabeled_points] = -1
lp = label_prop_model.fit(iris.data, labels)

print iris.target
print labels
# print lp.predict(iris.data[60:150])