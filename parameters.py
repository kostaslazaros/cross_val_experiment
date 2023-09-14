"""Set your parameters here before running the experiment"""
DATA_PATH = "./data"
SAVE_PATH = "./pickle2"
KEEP_FIRST_FEATURES = 100
REPEATS = 3
FOLDS = 10
ROUND_DECIMALS = 3
F1_AVERAGE = "weighted"
NOTIFY_CHANNEL = "lamia-box"
# If indexed list comes from R (one-based)
# then 1 has to be subtracted to have python
# compatibility (zero-based)
R_COMPATIBILITY = True
