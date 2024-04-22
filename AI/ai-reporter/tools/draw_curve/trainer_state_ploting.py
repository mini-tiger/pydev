import json
import math
import os
import argparse
from typing import List, Optional

TRAINER_STATE_NAME = "trainer_state.json"

import matplotlib.pyplot as plt


def smooth(scalars: List[float]) -> List[float]:
    r"""
    EMA implementation according to TensorBoard.
    """
    last = scalars[0]
    smoothed = list()
    weight = 1.8 * (1 / (1 + math.exp(-0.05 * len(scalars))) - 0.5)  # a sigmoid function
    for next_val in scalars:
        smoothed_val = last * weight + (1 - weight) * next_val
        smoothed.append(smoothed_val)
        last = smoothed_val
    return smoothed


def plot_loss(save_dictionaries: List[os.PathLike], key: Optional[str] = "loss") -> None:
    plt.figure()
    for save_dictionary in save_dictionaries:
        with open(os.path.join(save_dictionary, TRAINER_STATE_NAME), "r", encoding="utf-8") as f:
            data = json.load(f)

        steps, metrics = [], []
        for i in range(len(data["log_history"])):
            if key in data["log_history"][i]:
                steps.append(data["log_history"][i]["step"])
                metrics.append(data["log_history"][i][key])

        if len(metrics) == 0:
            continue
        
        dirname = os.path.basename(save_dictionary)
        # plt.plot(steps, metrics, alpha=0.4, label="{}_original".format(save_dictionary))
        # plt.plot(steps, smooth(metrics), label="{}_smoothed".format(dirname))
        plt.plot(steps, smooth(metrics), label="{}".format(dirname))
    plt.title("training {} curve".format(key))
    plt.xlabel("step")
    plt.ylabel(key)
    plt.legend()
    plt.savefig("training_{}.png".format(key), format="png", dpi=100)
    print("Figure saved:", "training_{}.png".format(key))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="the tool for drawing multiple loss lines")
    parser.add_argument('--dir', metavar="DIR", required=True, help='a dirtionary of loss data')
    args = parser.parse_args()
    save_dir = args.dir
    print("analysis the loss data in {}".format(save_dir))
    dirs = []
    files = os.listdir(save_dir)
    for f in files:
        full_path = os.path.join(save_dir, f)
        if os.path.isdir(full_path):
            dirs.append(full_path)
    plot_loss(dirs)
