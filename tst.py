import time


def blink(text):
    bls = "\033[5m"
    ble = "\033[0m"
    return f"{bls}{text}{ble}"


def tst():
    bls = "\033[5m"
    ble = "\033[0m"

    for i in range(3):
        print(f"Running {i} Files[{blink('RUNNING ')}] - Rest[        ]", end="\r")
        time.sleep(3)
        print(f"Running {i} Files[FINISHED] - Rest[{blink('RUNNING ')}]", end="\r")
        time.sleep(3)
        print(f"Running {i} Files[FINISHED] - Rest[FINISHED]")


if __name__ == "__main__":
    tst()
