"""Set your classifiers here"""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier


CLASSIFIERS = {
    "knn": {"function": KNeighborsClassifier, "parameters": {"n_neighbors": 10}},
    "lrc": {"function": LogisticRegression, "parameters": {"multi_class": "auto"}},
    "svm": {"function": SVC, "parameters": {"kernel": "linear"}},
    "mnb": {"function": MultinomialNB, "parameters": {}},
    "dtc": {"function": DecisionTreeClassifier, "parameters": {"random_state": 0}},
}
