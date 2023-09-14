"""Run multi dimensional experiments"""
import pickle
import os
import warnings
from collections import namedtuple

# from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
import numpy as np
import parameters as prm
from classifiers import CLASSIFIERS
from utils import msg, show_parameters

NamePath = namedtuple("NamePath", "name path")
DataPaths = namedtuple("DataPaths", "name data labels posidx")
LabelDfDic = namedtuple("LabelDfDic", "labels label2idx idx2label")
CrossRes = namedtuple(
    "CrossRes", "algorithm prediction ground_truth idx2lbl f1_score accuracy"
)
warnings.filterwarnings("ignore")


def get_datasets_paths(data_path: str):
    """Get dataset paths"""
    dataset_paths = os.listdir(data_path)
    dataset_paths.sort()
    return [NamePath(i, os.path.join(data_path, i)) for i in dataset_paths]


def get_files_from_path(namepath: NamePath):
    """Get files from path"""
    data = os.path.join(namepath.path, f"{namepath.name}.csv")
    labels = os.path.join(namepath.path, f"{namepath.name}_Labels.csv")
    posidx = os.path.join(namepath.path, f"PositionIndex_{namepath.name}.csv")
    return DataPaths(namepath.name, data, labels, posidx)


def create_save_path(data_path: str, dataset_name: str, no_of_repeats: int):
    """Save file as: <dataset_name>_<classifier_name>_<no_of_repeats>.pickle"""
    save_name = f"{dataset_name}_{no_of_repeats}.pickle"
    path = os.path.join(data_path, save_name)
    return NamePath(save_name, path)


def dataframe_from_csv_preproc(*, csv_path: str, transpose: bool):
    """Read dataframe from csv file and preprocess it"""
    dfr = pd.read_csv(csv_path)
    if transpose:
        dfr = dfr.T
    dfr.reset_index(drop=True, inplace=True)
    return dfr


def labels_from_csv_preproc(csv_path: str):
    """Read labels from csv file and preprocess them"""
    labels = pd.read_csv(csv_path)
    labels_unique_lst = list(labels["x"].unique())
    label2index = {name: i for i, name in enumerate(labels_unique_lst)}
    index2label = {j: i for i, j in label2index.items()}
    labels.replace(label2index, inplace=True)
    labels = labels.rename(columns={"x": "labels"})
    # print(list(labels["labels"]))
    return LabelDfDic(labels, label2index, index2label)


def feature_index_from_csv(*, path: str, keep_first: int = 0):
    """Read feature index
    if keep_first == 0 then keep all features
    fs_dic["full"] is a special case using all available features
    """
    feature_index = pd.read_csv(path)
    column_names = list(feature_index.columns)
    fs_dic = {"full": []}  # {method_name: [2048, 1035, 2442, 45324, ...]}
    for name in column_names:
        gene_index = pd.DataFrame(feature_index[name])
        gene_index.dropna(inplace=True)
        gene_index[name] = gene_index[name].astype("Int64")
        gene_index_lst = gene_index[name].tolist()
        if prm.R_COMPATIBILITY:
            gene_index_lst = [el - 1 for el in gene_index_lst]
        fs_dic[name] = gene_index_lst
        if keep_first > 0:
            fs_dic[name] = gene_index_lst[:keep_first]
    return fs_dic


def classifier_crossval(*, data, labels: LabelDfDic, alg_name="knn"):
    """Perform cross validation experiment"""
    class_labels = labels.labels

    # print(f"Dataset shape: {data.shape}")
    if isinstance(data, pd.DataFrame):
        data = data.values

    if isinstance(class_labels, pd.DataFrame) or isinstance(class_labels, pd.Series):
        class_labels = class_labels.values

    # Initialize array to store predicted class labels
    predictions = np.zeros(len(class_labels))

    # Create k-fold cross-validation object
    # kfold = KFold(n_splits=prm.FOLDS, shuffle=True)
    skfold = StratifiedKFold(n_splits=prm.FOLDS, shuffle=True)

    # Loop through each fold
    for train_index, test_index in skfold.split(data, class_labels):
        # Split data into training and test sets
        d_tr, d_ts = data[train_index], data[test_index]
        c_tr = class_labels[train_index]
        clf = CLASSIFIERS[alg_name]["function"](**CLASSIFIERS[alg_name]["parameters"])
        clf.fit(d_tr, c_tr)

        # Make predictions
        predictions[test_index] = clf.predict(d_ts)

    f1s = round(
        f1_score(class_labels, predictions, average=prm.F1_AVERAGE), prm.ROUND_DECIMALS
    )
    acc = round(accuracy_score(class_labels, predictions), prm.ROUND_DECIMALS)

    return CrossRes(
        alg_name,
        [int(i) for i in list(predictions)],
        list(labels.labels["labels"]),
        labels.idx2label,
        f1s,
        acc,
    )


def save2pickle(data: dict, pickle_path: str):
    """Save everything to pickle"""
    msg(f"Saving pickle to file: {pickle_path}")
    with open(pickle_path, "wb") as fil:
        pickle.dump(data, fil, pickle.HIGHEST_PROTOCOL)


def filter_features(dfr: pd.DataFrame, flist: list):
    """Filter dataset columns according to feature selection method"""
    if flist == []:
        return dfr
    return dfr.loc[:, flist]


def workflow(data_paths: list, repeats=prm.REPEATS):
    """Main workflow"""

    for dpath in data_paths:
        msg(f"Reading dataset: {dpath.name}")
        dfr = dataframe_from_csv_preproc(csv_path=dpath.data, transpose=True)
        labels = labels_from_csv_preproc(dpath.labels)
        feature_indices = feature_index_from_csv(
            path=dpath.posidx, keep_first=prm.KEEP_FIRST_FEATURES
        )

        results = {}
        for algorithm in CLASSIFIERS:
            msg(f"{dpath.name} {algorithm}")
            results[algorithm] = {}
            for findex, vals in feature_indices.items():
                results[algorithm][findex] = []
                filtered_df = filter_features(dfr, vals)
                msg(
                    f"{dpath.name} {algorithm} {findex} (features: {filtered_df.shape[1]})"
                )

                for i in range(repeats):
                    msg(f"{dpath.name} {algorithm} {findex} r{i + 1}")
                    res1 = classifier_crossval(
                        data=filtered_df, labels=labels, alg_name=algorithm
                    )
                    results[algorithm][findex].append(dict(res1._asdict()))
        data_res = {
            "name": dpath.name,
            "results": results,
            "no_of_features": prm.KEEP_FIRST_FEATURES,
        }
        save_path = create_save_path(prm.SAVE_PATH, dpath.name, prm.REPEATS)
        save2pickle(data_res, save_path.path)


def main():
    """Main function"""
    msg(f"Starting experiment with parameters:\n{show_parameters()}", toall=True)
    data_paths = [get_files_from_path(i) for i in get_datasets_paths(prm.DATA_PATH)]
    workflow(data_paths)
    msg("Experiment finished ok", toall=True)


if __name__ == "__main__":
    main()
