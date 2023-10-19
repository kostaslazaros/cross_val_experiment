import os
from collections import Counter
import pandas as pd


DATA_PATH = "/media/kostas/My Passport/projects/petros_review_data_evaluation/data/ResultsPaplomatas"
LABEL_PATH = (
    "/media/kostas/My Passport/projects/petros_review_data_evaluation/data/Labels"
)


def get_paths(dpath, lpath, h5_path):
    datasets = list(os.listdir(dpath))
    hdf5_existing = [i[:-3] for i in list(os.listdir(h5_path))]
    datasets.sort()
    labelsp = []
    datasp = []
    for dataset in datasets:
        label_file = f"{dataset}_Labels.csv"
        labelsp.append(os.path.join(lpath, label_file))
        data_file = f"{dataset}.csv"
        datasp.append(os.path.join(dpath, dataset, data_file))
    return datasets, labelsp, datasp, hdf5_existing


def list_to_text(alist):
    return " ".join([str(i) for i in alist])


def text_to_list(atxt):
    return [round(float(i), 2) for i in atxt.split()]


def data_stats(dpath, lpath):
    dnames, labelsp, datap, h5_path = get_paths(dpath, lpath, "")
    dfname = []
    cells = []
    genes = []
    class_no = []
    class_ps = []

    for i, dname in enumerate(dnames):
        # if i > 1:
        #     break

        dfname.append(dname)
        df = pd.read_csv(datap[i]).T
        # print(f"{dname} shape: {df.shape}")
        df_shape = df.shape
        cells.append(df_shape[0])
        genes.append(df.shape[1])
        dl = pd.read_csv(labelsp[i])
        counter = Counter(dl.x.values)
        class_names = counter.keys()
        class_size = len(class_names)
        class_no.append(class_size)
        total_size = sum(counter.values())

        class_percent = [round(i / total_size * 100, 2) for i in counter.values()]
        text_percent = list_to_text(class_percent)
        class_ps.append(text_percent)
        # pcn = text_to_list(text_percent)
        # print(
        #     dname, df_shape[0], df_shape[1], class_size, total_size, text_percent, pcn
        # )
    final_df = pd.DataFrame(
        {
            "Name": dfname,
            "Cells": cells,
            "Genes": genes,
            "Class no.": class_no,
            "Class %": class_ps,
        }
    )
    return final_df


def save2h5(dpath, lpath, h5_path):
    dnames, labelsp, datap, h5_existing = get_paths(dpath, lpath, h5_path)
    for i, dname in enumerate(dnames):
        h5_name = f"{dname}.h5"
        if dname in h5_existing:
            print(f"{h5_name} exists")
            continue

        final_h5_path = os.path.join(h5_path, h5_name)

        print(f"{h5_name} data[..] labels[  ]", end="\r")

        df = pd.read_csv(datap[i]).T
        df.to_hdf(final_h5_path, key="data", complevel=9)

        print(f"{h5_name} data[ok] labels[..]", end="\r")

        df = pd.read_csv(labelsp[i])
        df.to_hdf(final_h5_path, key="labels", complevel=9)

        print(f"{h5_name} data[ok] labels[ok]")

    print("Conversion complete ;-)")


if __name__ == "__main__":
    # final_df = data_stats(DATA_PATH, LABEL_PATH)
    # final_df.to_csv("./dataset_stats.csv", index=False)
    save2h5(DATA_PATH, LABEL_PATH, "./h5")
