"""Set your classifiers here"""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from parameters import SELECTED_CLASSIFIERS

all_classifiers = {
    "knn": {"function": KNeighborsClassifier, "parameters": {"n_neighbors": 10}},
    "mnb": {"function": MultinomialNB, "parameters": {}},
    "dtc": {"function": DecisionTreeClassifier, "parameters": {"random_state": 0}},
    "lrc": {"function": LogisticRegression, "parameters": {"multi_class": "auto"}},
    "svm": {"function": SVC, "parameters": {"kernel": "linear"}},
}

CLASSIFIERS = {cname: all_classifiers[cname] for cname in SELECTED_CLASSIFIERS}
