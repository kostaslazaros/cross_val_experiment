import pickle
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from notify import notify
import warnings

warnings.filterwarnings("ignore")


def kplot_all_lines(data, score, dataset_name, save_dir):
    """Plot one diagram with all lines"""
    x = data["range"]

    if score == "accuracy":
        fis = data["accuracy_scores"]
    elif score == "f1":
        fis = data["f1_scores"]
    else:
        raise ValueError("score ca be 'accuracy' or 'f1'")

    method_names = data["method_names"]

    ylabel = {"accuracy": "accuracy", "f1": "F1 score"}

    fig, ax = plt.subplots(figsize=(20, 12))
    cm = plt.cm.get_cmap("tab20c")
    for i, mname in enumerate(method_names):
        y = [sum(lst) / len(lst) for lst in fis[i]]
        ax.plot(x, y, color=cm.colors[i], label=f"{mname}")
    ax.legend(loc="lower right", ncol=2)
    ax.set_facecolor("whitesmoke")
    plt.title(f"Dataset {dataset_name}")
    ax.set_ylabel(ylabel[score])
    ax.set_xlabel("Feature Number")
    # ax.set_ylim(0.50, 1)
    # plt.show()
    save_path = os.path.join(save_dir, f"{dataset_name}_{score}")
    plt.savefig(save_path, dpi=300)


def main(pickle_path, figure_dir="./figures_lrc"):
    pickle_names = os.listdir(pickle_path)
    dataset_names = []
    for pname in pickle_names:
        title, *_ = pname.split("_")
        dataset_names.append(title)

    pickle_paths = [os.path.join(pickle_path, i) for i in pickle_names]

    for i, p_path in enumerate(pickle_paths):
        with open(p_path, "rb") as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            data = pickle.load(f)
        kplot_all_lines(data, "f1", dataset_names[i], figure_dir)
        # kplot_all_lines(data, "accuracy", dataset_names[i], figure_dir)


if __name__ == "__main__":
    main("./data/pickle_lrc/")
