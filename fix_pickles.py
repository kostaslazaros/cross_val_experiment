import pickle
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from notify import notify
import warnings

warnings.filterwarnings("ignore")


def create_list_1_top(*, value=1000, split_every=5):
    """Create a list of the form [1, v1, v2, ..., top]
    increasing values every split_every
    """
    res = list(range(0, value, split_every))
    res[0] = 1
    if res[-1] != value:
        res[-1] = value
    return res


def main(pickle_path, new_pickle_path):
    x = create_list_1_top(value=1000, split_every=5)
    pickle_names = os.listdir(pickle_path)
    pickle_paths = [os.path.join(pickle_path, i) for i in pickle_names]

    for i, p_path in enumerate(pickle_paths):
        with open(p_path, "rb") as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            data = pickle.load(f)
        data["range"] = x
        with open(os.path.join(new_pickle_path, pickle_names[i]), "wb") as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main("./data/pickle/", "./data/pickle2")
