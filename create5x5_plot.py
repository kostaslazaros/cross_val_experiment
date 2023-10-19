import pickle
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from notify import notify
import warnings

warnings.filterwarnings("ignore")


def main(pickle_path):
    pickle_names = os.listdir(pickle_path)
    pickle_names.sort()
    dataset_names = []
    datas = []
    for pname in pickle_names:
        title, *_ = pname.split("_")
        dataset_names.append(title)

    pickle_paths = [os.path.join(pickle_path, i) for i in pickle_names]

    for i, p_path in enumerate(pickle_paths):
        with open(p_path, "rb") as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            datas.append(pickle.load(f))

    cm = plt.cm.get_cmap("tab20c")
    fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(20, 20))
    arrs = [
        [0, 1, 2, 3, 4],
        [5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14],
        [15, 16, 17, 18, 19],
        [20, 21, 22, 23, 24],
    ]
    method_names = datas[0]["method_names"]
    x = datas[0]["range"]
    for i, val in enumerate(arrs):
        for j, val2 in enumerate(val):
            fis = datas[val2]["f1_scores"]
            for k, mname in enumerate(method_names):
                y = [sum(lst) / len(lst) for lst in fis[k]]
                axes[i, j].plot(x, y, color=cm.colors[k], label=f"{mname}")
                axes[i, j].set_facecolor("whitesmoke")
                axes[i, j].set_ylim(0.50, 1)
                axes[i, j].set_title(f"{dataset_names[val2]}")

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=6)

    plt.savefig("./testing2.png", dpi=300)

    # kplot_all_lines(data, "f1", dataset_names[i], figure_dir)
    # kplot_all_lines(data, "accuracy", dataset_names[i], figure_dir)


if __name__ == "__main__":
    main("./data/pickle_knn/")
