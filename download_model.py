from sklearn import svm
from sklearn import datasets

from servingml.frameworks.sklearn import save_model

# Load training data set
iris = datasets.load_iris()
X, y = iris.data, iris.target

# Train the model
clf = svm.SVC(gamma='scale')
clf.fit(X, y)

# Save model to the local Model Store
saved_model = save_model("iris_clf", clf)